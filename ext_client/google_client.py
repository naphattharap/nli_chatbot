#!/usr/bin/env python
__author__ = "Naphatthara P."
__version__ = "1.0.0"
__email__ = "naphatthara.p@gmail.com"
__status__ = "Prototype"

import json
import urllib.request
import logging
"""
Find books' information by calling API.
https://developers.google.com/books/docs/v1/using
"""
logging.getLogger().setLevel(logging.DEBUG)


class GoogleBookApiService:

    def __init__(self):
        # https://www.googleapis.com/books/v1/volumes?q=harry%20potter&maxResults=1&startIndex=100
        self.max_result = 10

    def get_json_respond(self, base_api_link):
        """
        Execute request URL and return as JSON object
        """
        # encode space to %20
        base_api_link = base_api_link.replace(" ", "%20")
        # logging.debug("encoded URL: %s", base_api_link)
        with urllib.request.urlopen(base_api_link) as f:
            text = f.read()
    
        decoded_text = text.decode("utf-8")
        # logging.debug("respond json: %s", decoded_text)
        json_obj = json.loads(decoded_text)  # deserializes decoded_text to a Python object
        items = json_obj["items"]
       
        book_list = []
        for item in items:
            volumn_info = item["volumeInfo"]
            sale_info = item["saleInfo"]
            book = {}
            book["title"] = volumn_info["title"]
            
            if 'authors' in volumn_info:
                if len(volumn_info["authors"]) > 0:
                    book["authors"] = ",".join(volumn_info["authors"])
                else:
                    book["authors"] = volumn_info["authors"]
            else:
                book["authors"] = ""

            if 'description' in volumn_info:
                book["description"] = volumn_info["description"]
            else:
                book["description"] = ""
            
            if 'categories' in volumn_info:
                if len(volumn_info["categories"]) > 0:
                    book["genre"] = ",".join(volumn_info["categories"])
                else:
                    book["genre"] = volumn_info["categories"]
            else:
                book["genre"] = ""
            
            if 'retailPrice' in sale_info:
                retail_price = sale_info["retailPrice"]
                book["price"] = str(retail_price["amount"]) + " " + retail_price["currencyCode"]
            else:
                book["price"] = ""

            logging.debug("book info: %s", book)
            book_list.append(book)
        
        return book_list

    def get_json_respond_book_detail(self, base_api_link):
        """
        Execute request URL and return as JSON object
        """
        # encode space to %20
        base_api_link = base_api_link.replace(" ", "%20")
        # logging.debug("encoded URL: %s", base_api_link)
        with urllib.request.urlopen(base_api_link) as f:
            text = f.read()
    
        decoded_text = text.decode("utf-8")
        # logging.debug("respond json: %s", decoded_text)
        json_obj = json.loads(decoded_text)  # deserializes decoded_text to a Python object
        items = json_obj["items"]
       
        book_list = []
        for item in items:
            volumn_info = item["volumeInfo"]
            sale_info = item["saleInfo"]
            book = {}
            book["title"] = volumn_info["title"]
            
            if 'authors' in volumn_info:
                if len(volumn_info["authors"]) > 0:
                    book["authors"] = ",".join(volumn_info["authors"])
                else:
                    book["authors"] = volumn_info["authors"]
            else:
                book["authors"] = ""

            if 'description' in volumn_info:
                book["description"] = volumn_info["description"]
            else:
                book["description"] = ""
            
            if 'categories' in volumn_info:
                if len(volumn_info["categories"]) > 0:
                    book["genre"] = ",".join(volumn_info["categories"])
                else:
                    book["genre"] = volumn_info["categories"]
            else:
                book["genre"] = ""
            
            if 'retailPrice' in sale_info:
                retail_price = sale_info["retailPrice"]
                book["price"] = str(retail_price["amount"]) + " " + retail_price["currencyCode"]
            else:
                book["price"] = ""
            
            logging.debug("book info: %s", book)
            book_list.append(book)
            break  # add break here to get only, just in case we want more in future
        
        return book_list
    
    def google_book_by_title_intent(self, title, max_result):  
        """
        Get title, authors, description, category (genre) and retail price
        """
        # ex. https://www.googleapis.com/books/v1/volumes?q=subect:Harry%20Potter&maxResults=1
        base_api_link = "https://www.googleapis.com/books/v1/volumes?q=intitle:" + title + "&maxResults=" + str(max_result)
        book_list = self.get_json_respond(base_api_link)
        return book_list
    
    def google_book_by_genre_intent(self, genre, max_result):  
        """
        Get book information by genre
        """
        base_api_link = "https://www.googleapis.com/books/v1/volumes?q=subject:" + genre + "&maxResults=" + str(max_result)
        book_list = self.get_json_respond(base_api_link)
        return book_list
    
    def google_book_by_author_intent(self, author, max_result):
        """
        Get book information by author
        """
        base_api_link = "https://www.googleapis.com/books/v1/volumes?q=inauthor:" + author + "&maxResults=" + str(max_result)
        book_list = self.get_json_respond(base_api_link)
        return book_list
  
    def google_book_details(self, key, max_result):
        """
        Get book information by author
        """
        base_api_link = "https://www.googleapis.com/books/v1/volumes?q=" + key + "&maxResults=" + str(max_result)
        book_list = self.get_json_respond_book_detail(base_api_link)
        return book_list      

