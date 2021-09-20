---
jupyter:
  jupytext:
    encoding: '# -*- coding: utf-8 -*-'
    formats: ipynb,md,py
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.2'
      jupytext_version: 1.8.0
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

<!-- #region slideshow={"slide_type": "slide"} hideCode=false hidePrompt=false -->
# Chapter 3 - When old models of computing fail

## Hadoop and Spark

Paul E. Anderson

Source: https://www.datadoghq.com/blog/hadoop-architecture-overview/
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
## Ice Breaker

Favorite place for ice cream in SLO (wait it's too cold for that)...

Favorite place for pizza in SLO
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
While this text can be viewed as PDF, it is most useful to have a Jupyter environment. I have an environment ready for each of you, but you can get your own local environment going in several ways. One popular way is with Anaconda (<a href="https://www.anaconda.com/">https://www.anaconda.com/</a>. Because of the limited time, you can use my server.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
### Update on lab grades
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
<img src='../labs/grade_summary.png' width=600>
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## What's wrong with our previous approaches?
* Apache Hadoop is a framework for distributed computation and storage of very large data sets on computer clusters
* Hadoop began as a project to implement Google’s MapReduce programming model
* Hadoop has seen widespread adoption by many companies including Facebook, Yahoo!, Adobe, Cisco, eBay, Netflix, and Datadog
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
### That didn't answer the question
Consider our needs?
* We want a programming model that can process data many times the size that can be processed by a single computer
* This level of coordination and abstraction can be difficult to achieve for a general purpose computing language such a Python. 
* Hadoop brings a paradigm shift in the following sense:
    * Simplying our programming constructs (i.e., limit us to Map Reduce)
    * Providing the architecture to support the computing we need
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
### Hadoop Distributed File System
* underlying file system of a Hadoop cluster
* designed with hardware failure in mind
* built for large datasets, with a default block size of 128 MB
* optimized for sequential operations
* rack-aware
* cross-platform and supports heterogeneous clusters
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
* Data in a Hadoop cluster is broken down into smaller units (called blocks) 
* Blocks are distributed throughout the cluster
* Each block is duplicated twice (for a total of three copies) 
* Two replicas stored on two nodes in a rack somewhere else in the cluster
* Highly available and fault-tolerant
* HDFS will automatically re-replicate it elsewhere in the cluster
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
<img src="https://imgix.datadoghq.com/img/blog/hadoop-architecture-overview/hadoop-architecture-diagram3.png?auto=format&fit=max&w=847">
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
### NameNode
* leader
* brokers access to files by clients
* operates entirely in memory
* persisting its state to disk
* One single point of failure for a Hadoop cluster

Clients communicate directly with DataNodes
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
## MapReduce
* Perfect for distributed computing of large data
* three operations: 
    * map an input data set into a collection of <key,value> pairs
    * shuffle the resulting data (transfer data to the reducers)
    * then reduce over all pairs with the same key
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
<img src="https://imgix.datadoghq.com/img/blog/hadoop-architecture-overview/hadoop-architecture-diagram1-3.png?auto=format&fit=max&w=847" width=2000>
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
### YARN (Yet Another Resource Negotiator)
Consists of three components
* ResourceManager (one per cluster)
* ApplicationMaster (one per application)
* NodeManagers (one per node)
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
<img src="https://imgix.datadoghq.com/img/blog/hadoop-architecture-overview/hadoop-architecture-diagram8.png?auto=format&fit=max&w=847">
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
### ResourceManager
* Rack-aware leader node in YARN. 
* Takes inventory of available resources
* Runs Scheduler.


<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
### ApplicationMaster
* Each application running on Hadoop has its own dedicated ApplicationMaster instance. 
* Each application’s ApplicationMaster periodically sends heartbeat messages to the ResourceManager, as well as requests for additional resources, if needed. 
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
### Yarn Flow
1. Client program submits the MapReduce application to the ResourceManager, along with information to launch the application-specific ApplicationMaster.
2. ResourceManager negotiates a container for the ApplicationMaster and launches the ApplicationMaster.
3. ApplicationMaster boots and registers with the ResourceManager, allowing the original calling client to interface directly with the ApplicationMaster.
4. ApplicationMaster negotiates resources (resource containers) for client application.
5. ApplicationMaster gives the container launch specification to the NodeManager, which launches a container for the application.
6. During execution, client polls ApplicationMaster for application status and progress.
7. Upon completion, ApplicationMaster deregisters with the ResourceManager and shuts down, returning its containers to the resource pool.

<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
### So when did Hadoop come out?
Well Google's MapReduce paper came out in 2004 - http://static.googleusercontent.com/media/research.google.com/en//archive/mapreduce-osdi04.pdf

Hadoop and Spark work well together, and such a combination is very common. We will discuss Spark next.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## Introduction to Spark
* Built around speed (in-memory enabled)
* ETL (extract, transform, load)
* Interactive queries (SQL)
* Advanced analytics (e.g., machine learning)
* Streaming over large datasets in a wide range of data stores (e.g., HDFS, Cassandra, HBase, S3)
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
### RDDs
* Resilient Distributed Dataset (RDD)
* Fault tolerant like hadoop
* Allows parallel operations upon itself
* RDDs can be created from Hadoop InputFormats (such as HDFS files) OR
* by transforming other RDDs.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
### Spark SQL
* Designed for processing structured and semi-structured data
* Provides a DataFrame API for data manipulations. 
* DataFrame is conceptually similar to a table in relational database.
* Represents a distributed collection of data organized into named columns. 
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
### MLLib
<a href="https://spark.apache.org/mllib/">https://spark.apache.org/mllib/</a>
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
### Streaming
<a href="https://spark.apache.org/docs/latest/streaming-programming-guide.html">https://spark.apache.org/docs/latest/streaming-programming-guide.html</a>
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
### GraphX
<a href="https://spark.apache.org/graphx/">https://spark.apache.org/graphx/</a>
<!-- #endregion -->

## Questions


### 1. What are the main responsibilities of the NameNode?


#### Your solution here


### 2. In general terms (i.e., don't get into Spark and language details), what is the output of the map stage?


#### Your solution here


### 3. Has Spark replaced Hadoop? Should it replace Hadoop?


#### Your solution here

<!-- #region slideshow={"slide_type": "subslide"} -->
## Conclusion
* Hadoop and Spark make up two pillars of the modern data engineering ecosystem. 
* We won't need to implement these (already done). We do need to understand them and use them.
* We will work our way through these technologies.
<!-- #endregion -->

```python

```
