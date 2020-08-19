# DAIN Data Engineering challenge - Part 1

This document attempts to provide a solution for the part 1 of the data engineering challenge. You will find the graphic for the required system architecture enclosed in the document.


**Requirement for  Architecture** -  We would like you to draw an architecture and write a short description addressing the following tasks (1-3). Imagine you are presenting this to a Product Owner of a client. Detail data pipelines and used methodology & technologies. Imagine we want to personalize a website. To this aim we want to develop a recommender system.


## Graphic for proposed system architecture

<img src='https://raw.githubusercontent.com/rtspeaks360/dain-de-challenge/rec_engine_architecture/images/DAIN-Architecture.jpeg'>

## Task specific comments

### TASK 1: Explain how the data could be captured and where we would store the data.

Since we need to maintain session context and we want to track what sort of products user checks out on the platform. This can be done by maintaining session dictionaries in a document database, that keeps track of the following information.

```
{
  session_id: <session_id>,
  customer_id: <cs_id>,
  is_active: <True/False>
  session_start: <start timestamp>
  last_update: <last_update_ts>
  items_viewed:{
    <list of item ids>
  }
}
```
Once the session has been inactive for a while, a session deadpool process deactivates the session in DynamoDB and moves the session data to the relational database where the user - item information can be combined with the demographic and purchase history data. Depending on the structure of the database, a view can be created that is updated everytime new data comes in from the session deadpool process. The can be designed in such a way that it serves directly as the training set, and as the scale of records increases the view can be converted into a materialized view as well. The view would cointain data about user - item interactions with both explicit and implicit ratings.

### TASK 2: Explain the process of generating the combined training set based on which we can build the recommendation algorithm.
Before talking about creation of the dataset let's first see what sort of recommendation models would be best for our use case. We know there are two basic approaches to recommendation: **Collaborative** and **Content-based**. 

Collaborative models work on just the user item interaction data (both implicit and explicit), not employing any actual user/item information. This interaction data  can directly be served by our view that encapsulates session data and purchase history. One thing to notice here is that while collaborative models can achieve high precision on little data, the **cold start problem still persists**.

The cold start problem can be handled by Content-based models since they **work purely on the available data** about items and users – entirely ignoring interactions between users and items approaching recommendations in a very different light. But now the problem in this case is that these sort of models are much harder to tune and require much more training data.

It would be ideal for us to use a hybrid recommendation model that emoploys both techniques. For the sake of this excercise we would be using LightFM, since it can combine both approaches and overcome a lot of the challenges of each individual approach.

For the LightFM model the training data would consist of the **user-item interaction data** which can be directly served by our view, and the seperate **user and item feature sets** as well. These can be served directly from user and item tables.

For the sake of this excercise I am not diving any deeper into LightFM actually makes recommendations since it is beyond the scope of this task. If you want to find out mode about how exactly recommendations are made, feel free to read the paper [here](https://arxiv.org/pdf/1507.08439.pdf).

One thing to be noted here is that the collaborative component will allow us to fall back on a collaborative filtering algorithm in case there are no features available – or the features aren’t informative. And the content-based component will allow us to get predictions even if we have no interaction data.

To allow for fast predictions in the production environment, we expect the user and item features to fit into memory to allow for a cache. (The redis component of the recommendation system in the architecture.) For caching a strategy like TTL or a different strategy like LRU could be used.

### TASK 3: Explain how you would deploy the recommender and integrate it to an already running website.

Once the LightFM recommendation model has been trained for our use case, it can be easily served over a Flask REST API endpoint that can be integrated in the existing website infrastructure. Further, the model being used by the API application can be re-trained periodically by the TrainedModel Job as new user / interaction data comes in and corresponding feature sets are updated.

*Hope my comments help you get a good understanding of the architecture proposed. Happy to answer any questions you might have during our next call.*



