from fastapi import FastAPI, WebSocket
import uvicorn
import asyncio
import os
import redis
import json
from pydantic import BaseModel

r = redis.from_url(os.environ.get("REDIS_URL"))
app = FastAPI()


class MusicSetup(BaseModel):
    eras: list
    genres: list


music = None

'''
setup/prep work

# create your folder structure
# don't let your genre have a dash in the name, eg "hip-hop" should just be "hiphop"
$ mkdir songs
$ cd songs
$ mkdir genre-rock genre-pop
$ for i in genre*; do mkdir $i/era-1980 $i/era-1990 $i/era-2000 $i/era-2010; done

# place the "song.mp3" files in their appropriate folders

# this will split each song into 3-second segments
$ find . -name "song.mp3" -exec ffmpeg -i "{}" -f segment -segment_time 3 -c copy "{}-%03d.mp3" \;

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
    return reset_votes(music_input)


def reset_votes(music_input):
    votes = {}
    if len(music_input.eras) and len(music_input.genres):
        for genre in music_input.genres:
            if '.extra' in genre: continue
            for era in music_input.eras:
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


@app.get("/reset")
async def reset_results():
    return reset_votes(music)


@app.post("/init")
async def reset_results(music_input: MusicSetup):
    global music
    music = music_input
    return api_init(music_input)


@app.get("/current-winner")
async def get_current_winner():
    winner = 'radio'
    votes = json.loads(r.get('votes'))
    if sum(list(votes.values())) > 0:
        tmp_votes = dict(sorted(votes.items(), key=lambda item: item[1], reverse=True))
        first_genre, first_era = list(tmp_votes.keys())[0].split('-')
        winner = f'{first_genre}-{first_era}'
    return {'winner': winner}


@app.get('/override-the-vote')
async def overload_the_vote():
    votes = json.loads(r.get('votes'))
    votes['.extra-1980'] = 10000000
    r.set('votes', json.dumps(votes))
    return {}
