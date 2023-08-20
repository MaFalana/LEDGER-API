import sys # for local
sys.path.append('.') #for local

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import uvicorn

from api.MangaManager import MangaDex, MangaSee

MD = MangaDex()
MS = MangaSee()

app = FastAPI(title="LEDGER° API") # Initialize the Flask application
# and enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/') # Index Route
def root():

    data = {
        "Message": "Connected to LEDGER API",
        "Server": "FastApi"
    }

    return data


@app.get('/MangaDex') # Index Route
def dex():

    data = {
        "Message": "Successfully connected to MangaDex route"
    }

    return data


@app.get('/MangaDex/Get') # Index Route
async def getDex(limit: int = 10, offset: int = 0):
    data = {
        "Message": "Successfully retrieved a list of manga from MangaDex",
        'Manga': MD.getManga(limit, offset)
    }

    return data


@app.get('/MangaDex/') # Search Route
async def searchDex(query: str, limit: int = 10, offset: int = 0):
    data = {
        'Manga': MD.searchManga(query, limit, offset)
    }

    return data



@app.get('/MangaSee') # Index Route
def see():

    data = {
        "Message": "Successfully connected to MangaSee route"
    }

    return data


@app.get('/MangaSee/Get') # Index Route
def getSee():

    data = {
        "Message": "Successfully retrieved a list of manga from MangaSee",
        'Manga': MS.getManga()
    }

    return data





# Start the server when the script is run directly
if __name__ == '__main__':
    uvicorn.run(app)
    