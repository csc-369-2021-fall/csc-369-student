# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,md,py
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.8.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# + [markdown] slideshow={"slide_type": "slide"} hideCode=false hidePrompt=false
# # Chapter 7.3 - Spark Streaming
#
# Paul E. Anderson

# + [markdown] slideshow={"slide_type": "subslide"}
# ## Ice Breaker
#
# Best breakfast burrito in town?

# + [markdown] slideshow={"slide_type": "slide"}
# ## Problem Statement:
# * You are approached by a company who has a machine learning pipeline that is trained and tested on historical data. 
# * This pipeline is used by the company to sort tweets into one of three categories which also have a corresponding numerical label in parentheses.
#     * Negative (0)
#     * Positive (1)
#     * Neutral (2)
#     
# The company has heard about your amazing skills as a Spark streaming expert. They would like you to take their pre-trained classifier and update it with new incoming data processed via Spark streaming.
# -

# ## Detours
#
# In order to implement our streaming approach, we need to take a couple of brief detours into machine learning. We need to answer the following questions:
# * How do we represent text as a vector of numbers such that a machine can mathematically learn from data?
# * How to use and evaluate an algorithm to predict numeric data into three categories (negative, positive, and neutral)? 

# + [markdown] colab_type="text" id="YbTiSkqNb75B"
# ### Representing text as a vector using `scikit-learn`
#
# scikit-learn is a popular package for machine learning.
#
# We will use a class called `CountVectorizer` in `scikit-learn` to obtain what is called the term-frequency matrix. 
# -

# A couple famous book openings:
#
# > The story so far: in the beginning, the universe was created. This has made a lot of people very angry and been widely regarded as a bad move - The Restaurant at the End of the Universe by Douglas Adams (1980)
#
# > Whether I shall turn out to be the hero of my own life, or whether that station will be held by anybody else, these pages must show. — Charles Dickens, David Copperfield (1850)
#
# How will a computer understand these sentences when computers can only add/mult/compare numbers?

# + colab={} colab_type="code" id="Fhl2Kwb5b75C"
from sklearn.feature_extraction.text import CountVectorizer

famous_book_openings = [
    "The story so far: in the beginning, the universe was created. This has made a lot of people very angry and been widely regarded as a bad move",
    "Whether I shall turn out to be the hero of my own life, or whether that station will be held by anybody else, these pages must show."
]

vec = CountVectorizer()
vec.fit(famous_book_openings) # This determines the vocabulary.
tf_sparse = vec.transform(famous_book_openings)
tf_sparse
# -

# ## Printing in a readable format

# +
import pandas as pd

pd.DataFrame(
    tf_sparse.todense(),
    columns=vec.get_feature_names()
)
# -

# ## Applying this process to our twitter data



# + [markdown] slideshow={"slide_type": "subslide"}
# ### The usual SparkContext

# + slideshow={"slide_type": "fragment"}
from pyspark import SparkConf
from pyspark.context import SparkContext

sc = SparkContext.getOrCreate(SparkConf().setMaster("local[*]"))

# + [markdown] slideshow={"slide_type": "subslide"}
# ### Grab a streaming context

# + slideshow={"slide_type": "fragment"}
from pyspark.streaming import StreamingContext

ssc = StreamingContext(sc, 1)
# -

# ### After a context is defined:
# * Define the input sources by creating input DStreams.
# * Define the streaming computations by applying transformation and output operations to DStreams.
# * Start receiving data and processing it using streamingContext.start().
# * Wait for the processing to be stopped (manually or due to any error) using streamingContext.awaitTermination().
# * The processing can be manually stopped using streamingContext.stop().

# ### Points to remember:
# * Once a context has been started, no new streaming computations can be set up or added to it.
# * Once a context has been stopped, it cannot be restarted.
# * Only one StreamingContext can be active in a JVM at the same time.
# * A SparkContext can be re-used to create multiple StreamingContexts, as long as the previous StreamingContext is stopped (without stopping the SparkContext) before the next StreamingContext is created.

# + slideshow={"slide_type": "subslide"}
PORT=9999 # Change this to a unique port before running individually
HOST="localhost"

# + slideshow={"slide_type": "subslide"}
print("Run this command at the terminal and type in words and hit enter periodically:")
print(f"nc -lk {PORT}")
# -

# ### Discretized Streams (DStreams)
# * DStream is the basic abstraction provided by Spark Streaming
# * Continuous stream of data, either the input data stream received from source, or the processed data stream generated by transforming the input stream. 
# * Internally, a DStream is represented by a continuous series of RDDs
# * Each RDD in a DStream contains data from a certain interval, as shown in the following figure.

# <img src="https://spark.apache.org/docs/latest/img/streaming-dstream.png">

# * Any operation applied on a DStream translates to operations on the underlying RDDs. 
# * In our example of converting a stream of lines to words, the flatMap operation is applied on each RDD in the lines DStream to generate the RDDs of the words DStream. 
# * This is shown in the following figure:
# <img src="https://spark.apache.org/docs/latest/img/streaming-dstream-ops.png">

# + slideshow={"slide_type": "subslide"}
lines = ssc.socketTextStream(HOST, PORT)
counts = lines.flatMap(lambda line: line.split(" "))\
              .map(lambda word: (word, 1))\
              .reduceByKey(lambda a, b: a+b)
counts.pprint()

ssc.start()
import time; time.sleep(10)
#ssc.awaitTerminationOrTimeout(60) # wait 60 seconds
ssc.stop(stopSparkContext=False)
# -

# **Stop and think:** What is missing in our previous example? 

# One thing is a lack of state. We process the lines in an RDD/DStream and print the results. What if we wanted to accumulate the word counts?

# +
ssc = StreamingContext(sc, 1)
ssc.checkpoint("checkpoint")

# RDD with initial state (key, value) pairs

def updateFunc(new_values, last_sum):
    return sum(new_values) + (last_sum or 0)

lines = ssc.socketTextStream(HOST,PORT)
running_counts = lines.flatMap(lambda line: line.split(" "))\
                      .map(lambda word: (word, 1))\
                      .updateStateByKey(updateFunc, initialRDD=initialStateRDD)

running_counts.pprint()

ssc.start()
import time; time.sleep(5)
#ssc.awaitTerminationOrTimeout(60) # wait 60 seconds
ssc.stop(stopSparkContext=False)
# -

# ## Monitoring a directory
#
# You can monitor a directory and apply the same processing.

# +
data_dir = "/tmp/add_books_here"

ssc = StreamingContext(sc, 1)
ssc.checkpoint("checkpoint")

# RDD with initial state (key, value) pairs

def updateFunc(new_values, last_sum):
    return sum(new_values) + (last_sum or 0)

lines = ssc.textFileStream(data_dir)

running_counts = lines.flatMap(lambda line: line.split(" "))\
                      .map(lambda word: (word, 1))\
                      .updateStateByKey(updateFunc)

running_counts.pprint()

ssc.start()
import time; time.sleep(30)
#ssc.awaitTerminationOrTimeout(60) # wait 60 seconds
ssc.stop(stopSparkContext=False)


# -

# ### Bridging Streaming and Spark SQL

# +
data_dir = "/tmp/add_books_here"


from pyspark.sql import SparkSession
from pyspark.sql import Row
import traceback

# Lazily instantiated global instance of SparkSession
def getSparkSessionInstance(sparkConf):
    if ("sparkSessionSingletonInstance" not in globals()):
        globals()["sparkSessionSingletonInstance"] = SparkSession \
            .builder \
            .config(conf=sparkConf) \
            .getOrCreate()
    return globals()["sparkSessionSingletonInstance"]

ssc = StreamingContext(sc, 1)
ssc.checkpoint("checkpoint")

lines = ssc.textFileStream(data_dir)

def process(time, rdd):
    print("========= %s =========" % str(time))
    if rdd.isEmpty():
        return
    # Get the singleton instance of SparkSession
    try:
        spark = getSparkSessionInstance(rdd.context.getConf())
        # Convert RDD[String] to RDD[Row] to DataFrame
        words = rdd.flatMap(lambda line: line.split(" ")).map(lambda word: word)
        rowRdd = words.map(lambda w: Row(word=w))
        wordsDataFrame = spark.createDataFrame(rowRdd)

        # Creates a temporary view using the DataFrame
        wordsDataFrame.createOrReplaceTempView("words")

        # Do word count on table using SQL and print it
        wordCountsDataFrame = spark.sql("select word, count(*) as total from words group by word")
        print(wordCountsDataFrame.show())
    except Exception:
        print(traceback.format_exc())

lines.foreachRDD(process)

ssc.start()
import time; time.sleep(30)
#ssc.awaitTerminationOrTimeout(60) # wait 60 seconds
ssc.stop(stopSparkContext=False)
# -


