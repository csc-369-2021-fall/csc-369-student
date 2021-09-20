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
# Chapter 6 - Why NoSQL 

## MongoDB

Paul E. Anderson
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
## Ice Breaker

Detroit style pizza versus new york versus chicago?
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
## Overview
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
## NoSQL
> NoSQL databases (aka "not only SQL") are non tabular, and store data differently than relational tables. NoSQL databases come in a variety of types based on their data model. The main types are document, key-value, wide-column, and graph. They provide flexible schemas and scale easily with large amounts of data and high user loads. Source: https://www.mongodb.com/nosql-explained
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
## What is NoSQL?
<img src="https://www.kdnuggets.com/wp-content/uploads/sql-nosql-dbs.jpg" width=700>
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
### Pros and Cons
<img src="https://www.clariontech.com/hs-fs/hubfs/SQL-NOSQL.png?width=813&name=SQL-NOSQL.png" width=700>
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
### What performance considerations? Why is this desired in some applications?
<img src="https://www.guru99.com/images/1/101818_0537_NoSQLTutori2.png">
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
<img src="https://miro.medium.com/max/5418/1*73e3UUYS_SsBYZfLvdOcfQ.png">
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
## What is a key-value database?
First point, a key-value is a map:
<img src="https://www.onlinemath4all.com/images/identifyingfunctionsfrommapping3.png">
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
Put another way:
<img src="https://www.educative.io/api/edpresso/shot/6707099755085824/image/5783885981941760">
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
## What are the tradeoffs?
<img src="https://cdn.educba.com/academy/wp-content/uploads/2020/01/CAP-Theorem-last.jpg">
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
### What is partition tolerance?
> A partition is a communications break within a distributed system—a lost or temporarily delayed connection between two nodes. Partition tolerance means that the cluster must continue to work despite any number of communication breakdowns between nodes in the system.

Source: https://www.ibm.com/cloud/learn/cap-theorem#:~:text=request%2C%20without%20exception.-,Partition%20tolerance,between%20nodes%20in%20the%20system.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
## What is distributed for performance gains?
<img src="https://i2.wp.com/www.kenwalger.com/blog/wp-content/uploads/2017/06/ShardingExample.png?resize=600%2C366">
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
<img src="https://devops.com/wp-content/uploads/2017/02/cap-theorem.jpg" width=600>
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
## Don't forget about the 8 fallacies...
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
<img src="http://www.mypassionfor.net/wp-content/uploads/2020/03/8-fallacies-of-distributed-computing-1024x714.png">
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
**The rest of this chapter is covered in**
<a href="https://beginnersbook.com/2017/09/introduction-to-nosql/">https://beginnersbook.com/2017/09/introduction-to-nosql/</a>
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
## Wrap-up
We have introduced NoSQL databases and discussed their overall features, pros, cons, design considerations, and functionality.
<!-- #endregion -->

```python

```
