import sys # for local
sys.path.append('.') #for local

from fastapi import FastAPI, APIRouter # Import the FastAPI class from fastapi
from fastapi.middleware.cors import CORSMiddleware

import uvicorn

#from api.routers import router, router2 # Import routers
from api.MangaManager import MangaDex, MangaKomi # Import classes from MangaManager.py
MD = MangaDex()
MK = MangaKomi()


# MANGADEX ROUTER

router = APIRouter(
    prefix="/MangaDex", # Set the prefix of the router
    tags=["MangaDex"], # Set the tag of the router
    responses={404: {"description": "Not found"}}, # Set the 404 response
) # Initialize the router


@router.get('/') # Index Route
async def getDex(limit: int = 10, offset: int = 0):
    list = MD.getManga(limit, offset)
    data = {
        "Message": "Successfully retrieved a list of manga from MangaDex",
        'Manga': list,
        'Chapter': [],
        'Pages': [],
        'limit': limit,
        'offset': offset,
        'total': len(list)
    }

    return data

@router.get('/{id}') # get a manga by id (manga, author, artist, tag), return parameters should be a list
async def find(id: str, limit: int = 10, offset: int = 0):

    list = MD.getManga2(id, limit, offset)

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

@router.get('/') # Search Route
async def searchDex(query: str, limit: int = 10, offset: int = 0):
    list = MD.searchManga(query, limit, offset)
    data = {
        'Message': f"Search results for {query}",
        'Manga': list,
        'Chapter': [],
        'Pages': [],
        'total': len(list)
    }

    return data

@router.get('/{id}/Chapter') # Gets chapters for manga
async def searchChapters(id: str):
    list = MD.getChapter(id)
    data = {
        'Message': f"Search results for {id}",
        'Manga': [],
        'Chapter': list,
        'Pages': [],
        'total': len(list)
        
    }

    return data

@router.get('/{id}/Read') # Gets pages for manga chapter
async def searchPages(id: str):
    data = {
        'Pages': MD.getPages(id)
    }

    return data

@router.get('/{type}/{id}/') # Search for either manga, author, artist, or tag
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




# MANGAKOMI ROUTER

router2 = APIRouter(prefix="/MangaKomi", tags=["MangaKomi"]) # Initialize the router

@router2.get('/') # Index Route
def get_manga_from_MangaKomi(limit: int = 10, offset: int = 0):
    list = MK.getManga()
    data = {
        "Message": "Successfully retrieved a list of manga from MangaKomi",
        'Manga': list,
        'Chapter': [],
        'Pages': [],
        'limit': limit,
        'offset': offset,
        'total': len(list)
    }
    return data


@router2.get('/{id}') # get a manga by id (manga, author, artist, tag), return parameters should be a list
def find_manga_from_MangaKomi(id: str, limit: int = 10, offset: int = 0):
        list = [MK.findManga(id)]
    
        data = {
            "Message": "Successfully retrieved a specific manga from MangaKomi",
            'Manga': list,
            'Chapter': [],
            'Pages': [],
            'limit': limit,
            'offset': offset,
            'total': len(list)
        }
    
        return data


@router2.get('/{id}/Chapter/{chapter}') # Gets chapters for manga
def find_chapter_from_MangaKomi(id: str, chapter: str):

    data = {
        "Message": "MangaKomi Chapter endpoints work",
        'Manga': [],
        'Chapter': [],
        'Pages': [],
        'total': 0
    }

    return data


app = FastAPI(title="LEDGER° API") # Initialize the Flask application
app.include_router(router, router2) # Include the routers in the app
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
        "Framework": "FastApi"
    }

    return data


# Start the server when the script is run directly
if __name__ == '__main__':
    uvicorn.run(app)
    
