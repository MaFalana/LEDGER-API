from fastapi import APIRouter # Import the APIRouter class from fastapi
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
async def get_a_list_of_manga_from_MangaDex(limit: int = 10, offset: int = 0):
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
async def find_a_manga_from_MangaDex(id: str, limit: int = 10, offset: int = 0):

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

@router.get('/Search') # Search Route
async def search_manga_from_MangaDex(query: str, limit: int = 10, offset: int = 0):
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
async def get_chapters_from_MangaDex(id: str):
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
async def get_pages_from_MangaDex(id: str):
    pages = MD.getPages(id)
    data = {
        'Message': f"Found pages for Chapter: {id}",
        'Manga': [],
        'Chapter': [],
        'Pages': pages,
        'total': len(pages)
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
def get_a_list_of_manga_from_MangaKomi(limit: int = 10, offset: int = 0):
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



# GOOGLE BOOKS ROUTER

router3 = APIRouter(prefix="/GoogleBooks", tags=["Google Books"]) # Initialize the router