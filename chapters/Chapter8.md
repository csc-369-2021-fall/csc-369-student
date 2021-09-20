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
# Chapter 7 - Can I have some of my favorite queries and a distributed database?

## MongoDB

Paul E. Anderson
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
## Ice Breaker

Favorite mac and cheese recipe or spin off?
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
## Hu(mongo)us

Used by companies such as Foursquare, bit.ly, and CERN for collecting Large Hadron Collider data.

Document database (JSON) ... though technically data is stored as BSON (binary form of JSON).

Allows data to persist in a nest state

Can query nested data in an ad hoc fashion
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
## What have we lost from relational databases?
We can no longer perform server side joins. 
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
## What's in an ID field?
Each document in a collection gets an automatic ObjectID:
* 12 bytes
* composed of a timestamp + client machine ID + client process ID + a 3-byte incremented counter

Why is this interesting? 
* Autonumbering scheme allows each process on every machine to handle its own ID generation without colliding with other instances.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## Let's have some fun with Mongo

We will use PyMongo, but you can use the native Javascript interface at the command line. We need to connect to our database (``csc-369``), and a collection of daily COVID19 cases as described in the lab.
<!-- #endregion -->

```python slideshow={"slide_type": "subslide"}
from pymongo import MongoClient
client = MongoClient()

db = client["csc-369"]
col = db["daily"]

col
```

<!-- #region slideshow={"slide_type": "subslide"} -->
### Finding one document
<!-- #endregion -->

```python slideshow={"slide_type": "fragment"}
col.find_one()
```

<!-- #region slideshow={"slide_type": "subslide"} -->
### Finding that document again
<!-- #endregion -->

```python slideshow={"slide_type": "fragment"}
list(col.find({"_id": '60392e3656264fee961ca816'}))
```

<!-- #region slideshow={"slide_type": "subslide"} -->
### What happened?
<!-- #endregion -->

```python slideshow={"slide_type": "fragment"}
from bson.objectid import ObjectId
list(col.find({"_id": ObjectId('60392e3656264fee961ca816')}))
```

<!-- #region slideshow={"slide_type": "subslide"} -->
### Ad hoc queries can be simple (above) or complex
<!-- #endregion -->

```python slideshow={"slide_type": "fragment"}
col.count_documents(
    {'state': {"$regex": "^A"},
     'totalTestResults': {"$gt": 6000}
    }
)
```

<!-- #region slideshow={"slide_type": "subslide"} -->
### What about a little OR?
<!-- #endregion -->

```python slideshow={"slide_type": "fragment"}
col.count_documents(
    {
        "$or": [
            {'state': {"$regex": "^A"}},
            {'totalTestResults': {"$gt": 6000}}
        ]
    }
)
```

<!-- #region slideshow={"slide_type": "subslide"} -->
| Command      | Description |
| ------------ | ----------- |
| \$regex       | Match by any PCRE-compliant regular expression string |
| \$ne          | Not equal to        |
| \$lt          | Less than |
| \$lte         | Less than or equal to |
| \$gt          | Greater than |
| \$gte         | Greater than or equal to |
| \$exists      | Check for the existence of a field |
| \$all         | Match all elements in an array |
| \$in          | Match any elements in an array |
| \$nin         | Does not match any elements in an array |
| \$elemMatch    | match all fields in an array of nested documents |
| \$or | or |
| \$nor         | Not or |
| \$size        | Match array of given size |
| \$mod         | Modulus |
| \$type        | Match if field is a given datatype |
| \$not         | Negate the given operator check |
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
### What if we wanted to update a mispelling?
<!-- #endregion -->

```python slideshow={"slide_type": "fragment"}
col.update_one(
    {"_id": ObjectId('60392e3656264fee961ca816')},
    {"$set": {"state":"ARK"}})
```

```python slideshow={"slide_type": "subslide"}
list(col.find({"_id": ObjectId('60392e3656264fee961ca816')}))
```

```python slideshow={"slide_type": "subslide"}
col.update_one(
    {"_id": ObjectId('60392e3656264fee961ca816')},
    {"$set": {"state":"AK"}})
```

```python slideshow={"slide_type": "subslide"}
list(col.find({"_id": ObjectId('60392e3656264fee961ca816')}))
```

<!-- #region slideshow={"slide_type": "subslide"} -->
| Command      | Description |
| ------------ | ----------- |
| \$set | Sets the given field with the given value |
| \$unset | Removes the field |
| \$inc | Adds the given field by the given number |
| \$pop | Removes the last (or first) element from an array |
| \$push | Adds the value to an array |
| \$pushAll | Adds all values to an array |
| \$addToSet | Similar to push, but won’t duplicate values |
| \$pull | Removes matching value from an array |
| \$pullAll | Removes all matching values from an array |
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
### Warning

Mongo will let you do what you want. Even the following:
<!-- #endregion -->

```python slideshow={"slide_type": "fragment"}
col.update_one(
    {"_id": ObjectId('60392e3656264fee961ca816')},
    {"$set": {"state":123}})
```

```python slideshow={"slide_type": "subslide"}
list(col.find({"_id": ObjectId('60392e3656264fee961ca816')}))
```

```python slideshow={"slide_type": "subslide"}
col.update_one(
    {"_id": ObjectId('60392e3656264fee961ca816')},
    {"$set": {"state":"AK"}})
```

<!-- #region slideshow={"slide_type": "slide"} -->
## Plug for more database classes
By default PyMongo creates an index to help you search for specific documents by ID, but it does not do so on other fields. You can create an
index for faster queries using ``ensureIndex``. This can change your queries from minutes to seconds or even milliseconds.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## Aggregation in MongoDB

The aggregate functionality in Mongo is extensive (https://docs.mongodb.com/manual/reference/operator/aggregation-pipeline/). We will cover some of the most common functionality such as matching and grouping.
<!-- #endregion -->

```python slideshow={"slide_type": "fragment"}
result = col.aggregate([
    # Match the documents possible
    { "$match": { "totalTestResults": { "$gt": 6000 } } },

    # Group the documents and "count" via $sum on the values
    { "$group": {
        "_id": { # key
            "state": "$state"
        },
        "count": { "$sum": 1 } # action
    }}
])
import pprint
pprint.pprint(list((result)))
```

<!-- #region slideshow={"slide_type": "slide"} -->
## MapReduce MongoDB
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
In order to do this, we will need some Javascript. It's pretty simple if you know languages such as Python, Java, C. We will perform the same aggregation as we did above.
<!-- #endregion -->

```python slideshow={"slide_type": "subslide"}
from bson.code import Code
map_func = Code(
"""
function () {
    if (this.totalTestResults > 6000) {
        return emit(this.state, 1);
    }
}
"""
)

reduce_func = Code(
"""
function(key,values) {
    var total = 0;
    for (var i = 0; i < values.length; i++) {
        total += values[i];
    }
    return total;
}
"""
)

result = col.map_reduce(map_func, reduce_func, "myresults")
for doc in result.find():
    print(doc)
```

<!-- #region slideshow={"slide_type": "subslide"} -->
## Wrap-up
We have introduced advanced functionality of Mongo including aggregation, filtering, counting, and map-reduce.
<!-- #endregion -->
