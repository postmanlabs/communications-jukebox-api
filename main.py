from fastapi import FastAPI, WebSocket
import asyncio
import os


app = FastAPI()


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
    for genre_era in VOTES:
        genre, era = genre_era.split('-')
        instructions[genre_era] = f'http://localhost:8000/vote/{genre}/{era}'
    return instructions

def reset_votes():
    votes = {}
    song_path = './songs/'
    dirs = [os.path.join(song_path, o) for o in os.listdir(song_path) if os.path.isdir(os.path.join(song_path, o))]
    for orig_dir in dirs:
        if 'genre' in orig_dir:
            genre = orig_dir.split('genre-')[-1]
            eras = dirs = [os.path.join(orig_dir, o) for o in os.listdir(orig_dir) if os.path.isdir(os.path.join(orig_dir, o))]
            for era in eras:
                era = era.split('era-')[-1]
                votes[f'{genre}-{era}'] = 0
    return votes


VOTES = reset_votes()


@app.get("/")
async def root():
    data = get_instructions()
    return data


@app.get("/vote/{genre}/{era}")
async def say_hello(genre: str, era: str):
    genre = genre.lower()
    era = era.lower()
    try:
        VOTES[f'{genre}-{era}'] += 1

        return {
            f'{genre}-{era}': VOTES[f'{genre}-{era}']
        }
    except KeyError:
        return get_instructions()

@app.get("/results")
async def get_vote_results():
    return VOTES


@app.get("/reset")
async def reset_results():
    global VOTES
    VOTES = reset_votes()
    return VOTES


@app.get("/current-winner")
async def get_current_winner():
    winner = 'radio'
    if sum(list(VOTES.values())) > 0:
        votes = dict(sorted(VOTES.items(), key=lambda item: item[1], reverse=True))
        first_genre, first_era = list(votes.keys())[0].split('-')
        winner = f'{first_genre}-{first_era}'
    return {'winner': winner}


@app.get('/override-the-vote')
async def overload_the_vote():
    VOTES['.extra-1980'] = 10000000
    return {}

