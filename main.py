from fastapi import FastAPI, Header
import uvicorn
import asyncio
import os
import redis
import json
from pydantic import BaseModel

auth_token = os.environ.get("POSTMAN_AUTH")

r = redis.from_url(os.environ.get("REDIS_URL"))
app = FastAPI()


class MusicSetup(BaseModel):
    eras: list
    genres: list


'''
todo:
- build a "poll" at infobip
- alter vote endpoint to get poll results from infobip
'''


def get_instructions():
    instructions = {
        "instructions": "use the links below to vote for your favorite genre/era of music"
    }

    votes = json.loads(r.get('votes'))
    for genre_era in votes:
        genre, era = genre_era.split('-')
        instructions[genre_era] = f'/vote/{genre}/{era}'
    return instructions


def api_init(music_input: MusicSetup):
    r.set("eras", json.dumps(music_input.eras))
    r.set("genres", json.dumps(music_input.genres))
    return reset_votes()


def reset_votes():
    votes = {}
    eras = json.loads(r.get("eras"))
    genres = json.loads(r.get("genres"))
    if len(eras) and len(genres):
        for genre in genres:
            if '.extra' in genre: continue
            for era in eras:
                votes[f'{genre}-{era}'] = 0
    r.set('votes', json.dumps(votes))
    return votes


@app.get("/")
async def root():
    data = get_instructions()
    return data


@app.get("/vote/{genre}/{era}")
async def say_hello(genre: str, era: str):
    genre = genre.lower()
    era = era.lower()
    votes = json.loads(r.get('votes'))
    try:
        votes[f'{genre}-{era}'] += 1
        r.set('votes', json.dumps(votes))

        return {
            f'{genre}-{era}': votes[f'{genre}-{era}']
        }
    except KeyError:
        return get_instructions()


@app.get("/results")
async def get_vote_results():
    votes = json.loads(r.get('votes'))
    return votes


@app.post("/reset")
async def reset_results(postman_auth: str = Header(None)):
    if postman_auth == auth_token:
        return reset_votes()
    return {'message': 'auth token not valid'}


@app.post("/init")
async def reset_results(music_input: MusicSetup, postman_auth: str = Header(None)):
    if postman_auth == auth_token:
        return api_init(music_input)
    return {'message': 'auth token not valid'}


@app.get("/current-winner")
async def get_current_winner():
    winner = 'radio'
    votes = json.loads(r.get('votes'))
    if sum(list(votes.values())) > 0:
        tmp_votes = dict(sorted(votes.items(), key=lambda item: item[1], reverse=True))
        try:
            first_genre, first_era = list(tmp_votes.keys())[0].split('-')
            winner = f'{first_genre}-{first_era}'
        except ValueError:
            winner = list(tmp_votes.keys())[0]
    return {'winner': winner}


@app.get('/override-the-vote')
async def overload_the_vote():
    votes = json.loads(r.get('votes'))
    votes['.extra'] = 10000000
    r.set('votes', json.dumps(votes))
    return {}
