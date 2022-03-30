# Infobip Jukebox API

This is an API used for in-person events between Infobip and Postman devrel teams.

This API will allow users to 'vote' for a favorite music genre and era of time, for example Rock music from the 1980's. With the corresponding [jukebox player](https://github.com/iandouglas/jukebox-player) application, voting with influence a fragment of sound being played for the next several seconds.


## Setup

To run this locally you'll need a Python 3 virtual environment set up, with the 'fastapi' and 'redis' libraries installed:

```bash
$ virtualenv venv
$ source venv/bin/activate
$ pip3 install -r requirements.txt

# then run the API locally:
$ python3 -m uvicorn main:app
```

If you want to watch changes and reload automatically you can add a `--reload` flag to the last python3 command after the `main:app` portion. If you need/want to bind to an alternate IP address, you can use `--host=1.2.3.4` to specify an IPv4 address.


## Deployment

A `Procfile` is included for deploying to Heroku, though you will need to manually set Redis as an add-on yourself if you wish to deploy this yourself.

## API Endpoints

### POST /init

Body:
```json
{
    "eras": [1980,1990,2000,2010],
    "genres": ["pop", "rock"]
}
```

This will initialize the API with "pop" and "rock" genres, and eras spanning the 1980-2010 decades. These values should come from the jukebox-player application automatically when it starts up, based on its local song structure.

### GET /

This will retrieve instructions for voting, along with URI paths of available genres and eras to vote.

### GET /reset

In case something goes a little sideways at an event, you can reset voting to 0 values by hitting this endpoint, which should tell the jukebox-player to resume the 'radio tuning' sound effect.

### GET /current-winner

This will retrieve the current winning vote. In case of a tie, the winner will be the lowest-alphabetical and oldest era. For example, "blues" would win over "waltz" because 'b' comes before 'w' in the alphabet, and 'pop 1980' would win over 'pop 2010' because 1980 is an older era.

### GET /results

Retrieves a full results list of all votes so far

### GET /vote/{genre}/{era}

By sending a specific genre and era in the URL path as string values, you can cast a single vote for that combination of genre and era. The returned payload will show you the current vote tally for that combination since the last reset.

