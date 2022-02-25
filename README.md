# A REST-API FOR SHARE MACHINE LEARNING MODELS

## Project Overview

This project permit to construct a REST API based on flask to share a previously trained machine learning model. The project contains the code for training the model using a Gradient Boosting Tree aproach over data about sales of tickets for cultural events in a online platform.

The data base consist in a few tables that inform about the customers and sellers that are bullying and selling tickets with information about the day of year for wich the sales occur. To train the models we use this features:

- day of week (with dummy encoding)
- month of year
- id of day.

There are two possibles target variables: the quantity of sales and the monetary value of the sales (known as 
qtysold and pricepaid). Also we consider that pronostic of sales can be computed for each category of event. There are four categories: Musicals, Opera, Plays, Pop. The user can obtain the predictions for seven days after the last day in the dataset for each categorie of event, but the total sales too.

In the process of construction of model, we use GridSearch and Cross validation using skit-learn library for python (model_selection module). We define and search space for this parameters: 

- clf: [GradientBoostingRegressor()]
- n_estimators: [10,15,20,25],
- function of loss: ['squared_error'],
- learning_rate: [0.05,0.1,0.15,0.20],
- random_state : [123] (this in order to achieve reproducibility of the results)
- max_depth': [2,3,5,10]

In consecuence, the dataset was splitted in two sets: Train and Test. You should note that you can add different estimator to the list associated to clf parameter. This is an excellent practice to facilitate iteration and scalability over a wider range of possible models.

# Documentation:

## Use cases:

You can obtain a json file with this format:

### In case of an invalid query to the API

```
data = {

    'status': False,
    'msg': "Los parámetros suministrados no son válidos",
    'list_features': [],
    'target_var': target,
    'categories': categories,
    'forecasts': [],
    'rmse': None,
    'r2': None

}

```

### In case of an valid query to the API

```
data = {

    'status': True,
    'msg': "Los parámetros suministrados no son válidos",
    'list_features': forecast_obj.X_to_predict.columns.tolist(),
    'target_var': target,
    'categories': categories,
    'forecasts': forecast_obj.forecast,
    'rmse': forecast_obj.rmse,
    'r2': forecast_obj.r2

} 

```

When the users ask for a result, they should send a url string like this:

```
url = https://107.22.107.142/targets-var/<var-target>/categories/<category>

```

Where <var_target> can be chosen between two options: qtysold, pricepaid and <categories> can be chosen between five options: Musicals, Opera, Plays, Pop, Todas. Any submission not matching this schema will result in json with empty values. This is one example:

If you need the forecast for monetary value of opera events, you should send the following url:

https://107.22.107.142/targets-var/pricepaid/categories/Opera

And, if you need the forescasts for quantity of sales for all events, you should send the following url:

https://107.22.107.142/targets-var/qtysold/categories/Todas

You can copy and paste this string in the browser and to observe the json file result.

When the query is made for first time with a particular selections of target variable and category, it is neccesary to train a new model for this specific scenario. Therefore the api may take a few minutes to respond the result. And conversely, when the model was previously created, the result is displayed more quickly.

# Files:

The structure for this project is:

- app
   - database-->Tables of Data Base
      - allevents_pipe.txt  # events and their categories
      - allusers_pipe.txt  # users and their ids
      - category_pipe.txt # Categories of events and their names
      - date2008_pipe.txt # date of year with descriptions (day of week, month, holiday)
      - listings_pipe.txt # Groups of tickets for sales
      - sales_tab # register of sales for each day of year
      - venue_pipe.txt # sites when the event ocurr.
   - models-->models of data
      - db.py # Class for to load table to dataframes.
   - modules-->customized functions
      - construct_dataset.py # Class that apply format to dataframes in order to construct a only dataset for the model.
      - encoder.py # Permit convert to a json key one numpy array 
      - predict  # predict seven values for each scenario
      - train model # A class to train Gradients Boosting Tree models.
   - trained_models # Models trained for each scenario.
- main.py--> The core of app
- requirements.txt-->dependencies of the project
 
 # Requirements:

- cffi==1.15.0
- click==8.0.4
- colorama==0.4.4
- dnspython==2.2.0
- eventlet==0.33.0
- Flask==2.0.3
- Flask-Cors==3.0.10
- gevent==21.12.0
- greenlet==1.1.2
- gunicorn==20.1.0
- itsdangerous==2.1.0
- Jinja2==3.0.3
- joblib==1.1.0
- MarkupSafe==2.1.0
- numpy==1.22.2
- pandas==1.4.1
- pycparser==2.21
- python-dateutil==2.8.2
- pytz==2021.3
- scikit-learn==1.0.2
- scipy==1.8.0
- six==1.16.0
- sklearn==0.0
- threadpoolctl==3.1.0
- waitress==2.0.0
- Werkzeug==2.0.3
- zope.event==4.5.0
- zope.interface==5.4.0

 # Final Remarks

The use of pipelines and Dummy Estimator for construct de GridSearch object facilitates the scalability and adaptability of the present rest api for other different uses. On the other hand, as you can see, you can download this repository for tests locally or use the service available at the indicated url, since this api was mounted on an AWS LightSail instance that allows its permanent consumption.

 The steps for run this app in a local environment is are the following:

 1. Download python 3.10 in your computer.
 2. Download pip and virtual enviroment package
 3. Reproduce the enviroment for this project. First you should create a new enviroment, sencod you should activate it. Then to do pip install -r requirements.txt inside that environment.
 4. Execute the file main.py over the root directory of this application. Here you can use this command: waitress-serve --call main:create_app

Finally, all comments to improve this project are appreciated.
