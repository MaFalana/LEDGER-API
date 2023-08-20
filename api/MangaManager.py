#import os, 
import requests
#from dotenv import load_dotenv
#load_dotenv()

class MangaManager(object):
    def __init__(self):
        pass



class MangaDex(MangaManager):
    def __init__(self):
        super().__init__()

    def getManga(self, limit, offset):

        url = "https://api.mangadex.org/manga"

        params = {
            'limit': limit,
            'offset': offset,
            'includedTagsMode': 'AND',
            'excludedTagsMode': 'OR',
            'contentRating[]': ['safe', 'suggestive', 'erotica'],
            'order[latestUploadedChapter]': 'desc',
            'includes[]': ['author', 'artist', 'cover_art']
        }

        response = requests.get(url, params = params)

        if response.status_code == 200:
                
            return self.parseResponse(response)

        else:
            print("Error:", response.status_code)

        return[]


    def getChapter(self, id): # Returns an array of chapter objects using a Manga id

        list = []

        url = "https://api.mangadex.org/chapter"

        params = {
            'limit': 10, # Should be a variable
            'offset': 0, # Should be a variable
            'manga': id,
            'translatedLanguage[]': 'en'
        }

        response = requests.get(url, params = params)

        if response.status_code == 200:

            data = response.json()

            results = data['data']

            for source in results:

                chapter = { # Some chapters mau not have a volume
                    'id': source['id'],
                    'volume': source['attributes'].get('volume', None),  # Handle the volume attribute condition
                    'chapter': source['attributes']['chapter'],
                    'title': source['attributes']['title'],
                    'pages': []
                }

                list.append(chapter)

        else:
            print("Error:", response.status_code)

        return list


    def getPages(self, id): # Returns an array of pages (url string) using a Chapter id, should really only be called when reading

        list = []

        url = f"https://api.mangadex.org/at-home/server/{id}"

        headers = {'Accept': 'application/json'}

        params = {'forcePort443': 'false'}

        response = requests.get(url, headers = headers, params = params)

        if response.status_code == 200:

            data = response.json()

            base = data['baseURL']
            hash = data['chapter']['hash']
            pages = data['chapter']['data'] # An array of pages

            for page in pages:

                link = f'{base}/data/{hash}{page}'
        
                list.append(link)   

        else:
            print("Error:", response.status_code)

        return list
    

    def getRelationships(self, id, relationships): # Returns a cover string using a Manga id
        author = None
        artist = None
        cover = None
        
        for source in relationships:
            if source['type'] == 'author':
                author = self.getAuthor(source['id'])

            elif source['type'] == 'artist':
                artist = self.getAuthor(source['id'])

            elif source['type'] == 'cover_art':
                cover = self.getCover(id, source['id'])
            
            if author and artist and cover:
                break

        data = {
            'author': author,
            'artist': artist,
            'cover': cover
        }

        return data
    

    def getAuthor(self, id):

        url = f"https://api.mangadex.org/author/{id}"

        response = requests.get(url)

        if response.status_code == 200:

            data = response.json()

            name = data['data']['attributes']['name']

            return {'id': id, 'name': name}

        else:
            print("Error:", response.status_code)

        return None
    

    def getCover(self, id, cover):

        url = f"https://api.mangadex.org/cover/{cover}"

        response = requests.get(url)

        if response.status_code == 200:

            data = response.json()

            link = data['data']['attributes']['fileName']

            return f'https://uploads.mangadex.org/covers/{id}/{link}'

        else:
            print("Error:", response.status_code)

        return None
    
    def getGenre(self, tags):

        list = []

        for tag in tags:

            genre = {
                'id': tag['id'],
                'name': tag['attributes']['name']['en']
            }

            list.append(genre)

        return list
    
    def parseResponse(self, response):
            
            list = []
            
            data = response.json()
    
            results = data['data']
    
            for manga in results:
    
                tags = manga['attributes']['tags']
    
                relationships = self.getRelationships(manga['id'], manga['relationships'])
    
                title1 = manga['attributes']['title'].get('en', None)
                title2 = manga['attributes']['title'].get('ja', None)
                
                Manga = {
                    'source': 'MangaDex',
                    'id': manga['id'],
                    'title':  title1 or title2 or 'Untitled',
                    'author': relationships['author'],
                    'artist': relationships['artist'],
                    'description': manga['attributes']['description'].get('en', None),
                    'status': manga['attributes']['status'], # Should be capitalized
                    'cover': relationships['cover'],
                    'genre': self.getGenre(tags),
                    'chapters': self.getChapter(manga['id'])
                }
    
                list.append(Manga)
    
            return list
    

    def searchManga(self, query, limit, offset):
        url = "https://api.mangadex.org/manga"

        params = {
            'limit': limit,
            'offset': offset,
            'title': query,
            'includes[]': ['author', 'artist', 'cover_art']
        }

        response = requests.get(url, params = params)

        if response.status_code == 200:
            return self.parseResponse(response)
        
        else:
            print("Error:", response.status_code)
            return []

    


class MangaSee(MangaManager):
    def __init__(self):
        super().__init__()

    def getManga(self):

        list = []

        query = 'One'

        url = f"https://api.consumet.org/manga/mangasee123/{query}"

        response = requests.get(url)

        if response.status_code == 200:

            source = response.json()['results']

            for data in source:

                Manga = {
                    'source': 'MangaSee',
                    'id': data['id'],
                    'title': data['title'],
                    'author': None,
                    'artist': None,
                    'description': None,
                    'status':None, # Should be capitalized
                    'cover': data['image'],
                    'genre': data['genres'],
                    'chapters': data['chapters']
                }

                list.append(Manga)

        else:
            print("Error:", response.status_code)

        return list
