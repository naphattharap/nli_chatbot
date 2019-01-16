import json
import json
import textwrap
import textwrap
import urllib.request
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
    
    def search_by_isbn(self):
        while True:
        
            base_api_link = "https://www.googleapis.com/books/v1/volumes?q=isbn:"
            user_input = input("Enter ISBN: ").strip()
        
            with urllib.request.urlopen(base_api_link + user_input) as f:
                text = f.read()
        
            decoded_text = text.decode("utf-8")
            obj = json.loads(decoded_text)  # deserializes decoded_text to a Python object
            volume_info = obj["items"][0] 
            authors = obj["items"][0]["volumeInfo"]["authors"]
        
            # displays title, summary, author, domain, page count and language
            print("\nTitle:", volume_info["volumeInfo"]["title"])
            print("\nSummary:\n")
            print(textwrap.fill(volume_info["searchInfo"]["textSnippet"], width=65))
            print("\nAuthor(s):", ",".join(authors))
            print("\nPublic Domain:", volume_info["accessInfo"]["publicDomain"])
            print("\nPage count:", volume_info["volumeInfo"]["pageCount"])
            print("\nLanguage:", volume_info["volumeInfo"]["language"])
            print("\n***")
        
            status_update = input("\nEnter another ISBN? y or n: ").lower().strip()
        
            if status_update == "n":
                print("\nThank you! Have a nice day.")
                break
  
    def search_by_genre(self, genre):  
        
        base_api_link = "https://www.googleapis.com/books/v1/volumes?q=subject:" + genre + "&maxResult=5"
    
        with urllib.request.urlopen(base_api_link + genre) as f:
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
    
# googleBook = GoogleBookApiService() 
# googleBook.search_by_genre("Art")
