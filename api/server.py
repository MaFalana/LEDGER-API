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


@app.get('/MangaDex/{id}') # get a manga by id (manga, author, artist, tag), return parameters should be a list
async def find(id: str, limit: int = 10, offset: int = 0):

    list = MD.getManga2(id, limit, offset)

    data = {
        "Message": "Successfully retrieved a specific manga from MangaDex",
        'data': list,
        'total': len(list)
    }

    return data


@app.get('/MangaDex/Get/') # Index Route
async def getDex(limit: int = 10, offset: int = 0):
    list = MD.getManga(limit, offset)
    data = {
        "Message": "Successfully retrieved a list of manga from MangaDex",
        'Manga': list,
        'Chapter': [],
        'Pages': [],
        'total': len(list)
    }

    return data


@app.get('/MangaDex/') # Search Route
async def searchDex(query: str, limit: int = 10, offset: int = 0):
    list = MD.searchManga(query, limit, offset)
    data = {
        'Message': f"Search results for {query}",
        'Manga': list,
        'total': len(list)
    }

    return data


@app.get('/MangaDex/{id}/Chapter') # Gets chapters for manga
async def searchChapters(id: str):
    data = {
        'data': MD.getChapter(id)
    }

    return data

@app.get('/MangaDex/{id}/Read') # Gets pages for manga chapter
async def searchPages(id: str):
    data = {
        'data': MD.getPages(id)
    }

    return data

@app.get('/MangaDex/{type}/{id}/') # Search for either manga, author, artist, or tag
async def searchChapters(type: str, id: str, limit: int = 10, offset: int = 0):
    list = MD.searchExtra(type, id, limit, offset)

    data = {
        "Message": "Successfully retrieved a specific manga from MangaDex",
        'Manga': list,
        'Chapter': [],
        'Pages': [],
        'limit': limit,
        'offset': offset,
        'total': len(list)
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
    
