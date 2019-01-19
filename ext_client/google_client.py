import json
import textwrap
import urllib.request


# class GoogleApiClientService:
#     def __init__(self):
#         API_KEY = "AIzaSyBiepAN_JJFNYeDHN7yGqyfWWNr8SHQpL8"# copied from project credentials page
#         self.GPLUS = discovery.build('plus', 'v1', developerKey=API_KEY)
# 
#     def search_by_genre(self, genre):
# 
#         items = self.GPLUS.activities().search(query='subject:'+genre).execute().get('items', [])
#         for data in items:
#             post = ' '.join(data['title'].strip().split())
#             if post:
#                 print(TMPL % (data['actor']['displayName'],
#                               data['published'], post))
class GoogleBookApiService:

    def __init__(self):
        # https://www.googleapis.com/books/v1/volumes?q=harry%20potter&maxResults=1&startIndex=100
        self.max_result = 10

    def recommend_book_by_genre_intent(self, genre):  
        
        base_api_link = "https://www.googleapis.com/books/v1/volumes?q=subject:" + genre + "&maxResult=5"
    
        with urllib.request.urlopen(base_api_link) as f:
            text = f.read()
    
        decoded_text = text.decode("utf-8")
        print(decoded_text)
        obj = json.loads(decoded_text)  # deserializes decoded_text to a Python object
        items = obj["items"]
        titles = []
        for item in items:
            titles.append(item["volumeInfo"]["title"])
        
        str_title = ""
        if len(titles) > 0:
            str_title = ",".join(titles)
        return str_title
    
    def recommend_book_by_author_intent(self, author):
        """
        """
        base_api_link = "https://www.googleapis.com/books/v1/volumes?q=inauthor:" + author + "&maxResult=1"
    
        with urllib.request.urlopen(base_api_link) as f:
            text = f.read()
    
        decoded_text = text.decode("utf-8")

        # deserializes decoded_text to a Python object
        obj = json.loads(decoded_text)
        items = obj["items"]
        results = []
        for item in items:
            volume_info = item["volumeInfo"]
            results.append(volume_info["title"])
            results.append(volume_info["authors"])
            # Plot
            results.append(volume_info["description"])
        
#         str_result = ""
#         if len(results) > 0:
#             str_result = ",".join(results)
        return results
    
# googleBook = GoogleBookApiService() 
# # googleBook.search_by_genre("Art")
# googleBook.recommend_book_by_author_intent("JK")
