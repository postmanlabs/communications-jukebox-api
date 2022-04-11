# Infobip Jukebox API

This is an API used for in-person events between Infobip and Postman devrel teams.

This API will allow users to 'vote' for a favorite music genre and era of time, for example Rock music from the 1980's. With the corresponding [jukebox player](https://github.com/iandouglas/jukebox-player) application, voting with influence a fragment of sound being played for the next several seconds.


## Setup

To run this locally you'll need a Python 3 virtual environment set up, with the 'fastapi' and 'redis' libraries installed:

```bash
$ python3 -m venv venv
$ source venv/bin/activate
$ pip3 install -r requirements.txt

# set your redis hostname in a shell environment
$ export REDIS_URL=redis://localhost:6379

# set your shared Postman authentication value in a shell environment
$ export POSTMAN_AUTH="shared api key"

# then run the API locally:
$ python3 -m uvicorn main:app

# if you don't want to export the shell environment setting, you can launch the app this way:
$ POSTMAN_AUTH="shared api key" REDIS_URL=redis://localhost:6379 python3 -m uvicorn main:app
```

If you want to watch changes and reload automatically, you can add a `--reload` flag to the last python3 command after the `main:app` portion. If you need/want to bind to an alternate IP address, you can use `--host=1.2.3.4` to specify an IPv4 address.


## Deployment

A `Procfile` is included for deploying to Heroku, though you will need to manually set Redis as an add-on yourself if you wish to deploy this yourself. You will also need to manually set the POSTMAN_AUTH environment variable in your hosting environment as well.


## API Endpoints

You can view our published documentation [at this link](https://documenter.getpostman.com/view/19408657/UVysvuuw) and run the collection within Postman using the following link:

[Run In Postman](https://elements.getpostman.com/view/import?collection=19408657-08f70aa3-ed8d-4385-acc8-dc2905eda5b8-UVysvuuw)
