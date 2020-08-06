# PyGeo
This repo provides three simple services:

- Get latitute/longtitute of a give address (using google's geocode)
- Get address of given latitute/longtitute (reverse of first one)
- Calculate distance between two given latitute/longtitute

A lot of folders and files for only three simple services! I admit it is overwhelming, but for a scalable project organize code comes first.

Even further, the whole geo specified code could reside in a folder called `geo`, like a django-app, and blueprint can be defined to separate geo urls from rest of the app. This strategy comes handy when we have also other apps, like authentication which can be a separate app of it's own if implemented.

I have used `Flask` for this specific project, `Django` is another leading framework which comes with batteries inlcuded, a lot of features already is installed and is suitable for apps which is more data centric and have database interaction, which in case of our app we have zero. Also `FastAPI` sounds promissing these days, which supports asynchronous.

I suppose this project can be used with a front-end to explore those three serivces, which for sure a sort of authentication should be provided like JWT.

At the moment I assume we don't need any autheticaiton for simplicity and services could be called by anyone.

To prevent a brute force attach, requests from the same ip-address only can be handles per 10 seconds (configurable in settings).

## Before Start
To know about Google's geocode service and how to start using it please renfer to the following links:

https://developers.google.com/maps/documentation/geocoding/intro
 
https://support.google.com/googleapi/answer/6158862?hl=en

## Run project (As standalone via terminal)
- `GOOGLE_API_KEY` should be provided via env vars.
For linux or MacOS do as follows on your terminal before run:

    `export GOOGLE_API_KEY=YOUR_GOOGLE_APP_KEY`

- Install a virutalenv and install project requirements:
    ```
    $ sudo pip3 install virtualenv
    $ mkdir ~/Envs
    $ virtualenv ~/Envs/geo --python=$(python3.8)
    $ source ~/Envs/geo/bin/activate
    $ pip install -r requirments.txt
    ```
- Run `docker run --name georedis -p 6379:6379 -d redis`  to setup a Redis-server, or you can install it locally.
- Run `make dev` to run Flask development server
- browse for: http://localhost:5000

## Run via docker-compose
- create `.secrets.env` file in root of project, and place your `GOOGLE_API_KEY=YOUR_GOOGLE_APP_KEY` inside
- Run `docker-compose up` which will run redis and flask project as two separate containers. Caution if there is already a redis cotainer running on the same port you will get an error.
- browse for: http://localhost:5000
- Flask projec will run on `gunicorn`


## Run tests
- Before running tests, refer to section `Run project (As standalone via terminal)` and met prerequisities.
- Run one of the following command from project root directory:

    `make test` or

    `python -m unittest discover` or

    `python -m unittest tests/tests_geo.py`
- Tests are mocking external services calls.

## Endpoints
Result returns for both geoloc and geocode is a complete record as:
```
{
    "address": "100 W Broadway Suite 100, Glendale, CA 91210, USA",
    "location": {
        "lat": 34.1462627,
        "lng": -118.2567687
    }
}
```

you may search by complete address or just `Glendale Galleria` for geoloc, so it is valueable to have complete record in response.

- To get an address location from lattitute and longtitute:

    `http://localhost:5000/geoloc/<lattitute,longtitute>`

    Example:  

      http://localhost:5000/geoloc/40.714224,-73.961452

- To get lattitute and longtitute for a give address:


    `http://localhost:5000/geocode/<address>`

    Example:

      http://localhost:5000/geocode/100%20W%20Broadway%20Suite%20100,%20Glendale,%20CA%2091210

      http://localhost:5000/geocode/status%20of%20librety

      You don't need to enter `%20`, browser will take care of spaces

- To get distance between two pair of lattitute and longtitute:


    `http://localhost:5000/geodist/<lattitute1,longtitute1>/<lattitute2,longtitute2>`

    Example:

      http://localhost:5000/geodist/34.1446893,-118.2619364/34.1835595,-118.3143886

## Futher improvement
A project is a work in progress, two things that I can suggest when such a project grows:

- All error messages can be organized in a resource file, this way we can easily provide internationalization if needed.
- Every module related to geo, refactored in a distinct package, this way we can add more logic on different categories better organized.
- Proper logging should be added to the solution
- Main function to get the distance support both miles and kilometers, it could be easy to add support for  measurement selection from API.
- A module needed to be implemented and scheduled to remove cached data older than specific amount of time. In our scenario we don't need records older that 10 seconds, but still we don't want run this routine very frequent. Depends on our data volume, maybe we can schedule it for every 10 minutes.
