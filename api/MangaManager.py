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

    def getManga2(self, id, limit, offset):

        url = f"https://api.mangadex.org/manga/{id}"

        params = {
            'limit': limit,
            'offset': offset,
            'includes[]': ['author', 'artist', 'cover_art', 'tag']
        }

        response = requests.get(url, params = params)

        if response.status_code == 200:
                
            return self.parseResponse(response)

        else:
            print("Error:", response.status_code)

        return []

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

        return []


    def getChapter(self, id): # Returns an array of chapter objects using a Manga id

        list = []

        limit = 100
        
        offset = 0

        url = "https://api.mangadex.org/chapter"

        while True:

            params = {
                'limit': limit, # Should be a variable
                'offset': offset, # Should be a variable
                'manga': id,
                'translatedLanguage[]': 'en'
            }

            response = requests.get(url, params = params)

            if response.status_code == 200:

                data = response.json()

                results = data['data']

                total = data['total'] # Total number of chapters

                for source in results:

                    chapter = { # Some chapters may not have a volume
                        'id': source['id'],
                        'volume': source['attributes'].get('volume', None),  # Handle the volume attribute condition
                        'chapter': source['attributes']['chapter'],
                        'title': source['attributes']['title'],
                        'pages': []
                        #'date': '09/02/2023',
                    }

                    list.append(chapter)

                offset += limit  # Move to the next page

                if offset >= total:
                    break  # Stop fetching if all chapters are retrieve

            else:
                print("Error:", response.status_code)
                break

        return list


    def getPages(self, id): # Returns an array of pages (url string) using a Chapter id, should really only be called when reading

        list = []

        url = f"https://api.mangadex.org/at-home/server/{id}"

        headers = {'Accept': 'application/json'}

        params = {'forcePort443': 'false'}

        response = requests.get(url, headers = headers, params = params)

        if response.status_code == 200:

            data = response.json()

            base = data['baseUrl']
            hash = data['chapter']['hash']
            pages = data['chapter']['data'] # An array of pages

            for page in pages:

                link = f'{base}/data/{hash}/{page}'
        
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
                author = self.getAuthor(source['id'], source['type'])

            elif source['type'] == 'artist':
                artist = self.getAuthor(source['id'], source['type'])

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
    

    def getAuthor(self, id, type):

        url = f"https://api.mangadex.org/author/{id}"

        response = requests.get(url)

        if response.status_code == 200:

            data = response.json()

            name = data['data']['attributes']['name']

            return {'id': id, 'name': name, 'type': type}

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
                'name': tag['attributes']['name']['en'],
                'type': 'tag'
            }

            list.append(genre)

        return list
    
    def parseResponse(self, response):
            
            rlist = []
            
            data = response.json()
    
            results = data['data']

            if isinstance(results, list): # If the results is a list, then it is a search query
    
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
        
                    rlist.append(Manga)

            else:
                tags = results['attributes']['tags']
        
                relationships = self.getRelationships(results['id'], results['relationships'])
    
                title1 = results['attributes']['title'].get('en', None)
                title2 = results['attributes']['title'].get('ja', None)
                
                Manga = {
                    'source': 'MangaDex',
                    'id': results['id'],
                    'title':  title1 or title2 or 'Untitled',
                    'author': relationships['author'],
                    'artist': relationships['artist'],
                    'description': results['attributes']['description'].get('en', None),
                    'status': results['attributes']['status'], # Should be capitalized
                    'cover': relationships['cover'],
                    'genre': self.getGenre(tags),
                    'chapters': []#self.getChapter(manga['id'])
                }
    
                rlist.append(Manga)
    
            return rlist
    

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
            

    def searchExtra(self, type, id, limit, offset): # search manga, either by tag, author, or artist

        url = f"https://api.mangadex.org/manga"

        if type == 'author' or type == 'artist':
            params = {
                'limit': limit,
                'offset': offset,
                'authorOrArtist': id,
                'includes[]': ['author', 'artist', 'cover_art']
            }
        else:
            params = {
                'limit': limit,
                'offset': offset,
                'includedTags[]': [id],
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
