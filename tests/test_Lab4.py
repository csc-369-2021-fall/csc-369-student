import sys
import os
sys.path.append(".")

# Import the student solutions
import Lab4_helper

import pathlib
DIR=pathlib.Path(__file__).parent.absolute()

import joblib 
answers = joblib.load(str(DIR)+"/answers_Lab4.joblib")

from pyspark import SparkContext
from pyspark import SparkConf
from pyspark.context import SparkContext

sc = SparkContext.getOrCreate(SparkConf().setMaster("local[*]"))

def run_exercise_1():
    rdd=sc.parallelize(Lab4_helper.data)
    output = Lab4_helper.word_counts(rdd)
    return set(output)

def run_exercise_2():
    rdd=sc.parallelize(Lab4_helper.data)    
    word_frequencies = Lab4_helper.word_freq(rdd)
    return set(word_frequencies)

def run_exercise_3():
    all_books_rdd = Lab4_helper.load_rdd_all_books(sc,f"file:{DIR}/../data/gutenberg")
    word_frequencies = Lab4_helper.word_freq(rdd)
    return set(word_frequencies)

def run_exercise_4():
    res = Lab4_helper.book_word_counts(sc,f"file:{DIR}/../data/gutenberg")
    return set(res)

def counts2tuple(counts):
    lines = []
    for key in sorted(list(counts.keys())):
        lines.append((key,counts[key]))
    return tuple(lines)

def test_exercise_1():
    assert answers['exercise_1'] == run_exercise_1()

def test_exercise_2():
    assert answers['exercise_2'] == run_exercise_2()

def test_exercise_3():
    assert answers['exercise_3'] == run_exercise_3()

def test_exercise_4():
    assert answers['exercise_3'] == run_exercise_3()