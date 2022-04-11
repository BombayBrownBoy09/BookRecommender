# import packages
import pandas as pd
import numpy as np
import gzip
import re
import json
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from gensim import corpora
import random
import pickle



liked_books = ['22543496', '39661', '12816830', '482060', "9401317", "9317691", "8153988"]



def book_mapping():
    
    csv_book_mapping = {}

    with open("book_id_map.csv", "r") as f:
        while True:
            line = f.readline()
            if not line:
                break
            csv_id, book_id = line.strip().split(",")
            csv_book_mapping[csv_id] = book_id
    return csv_book_mapping


def overlap_users():

    overlap_users = set()

    with open("goodreads_interactions.csv", 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            user_id, csv_id, _, rating, _ = line.split(",")
            
            if user_id in overlap_users:
                continue

            try:
                rating = int(rating)
            except ValueError:
                continue
            
            #convert csvid to book id
            book_id = csv_book_mapping[csv_id]
            
            # if the booke id is in our liked books, add the user to the list of overlapped users
            if book_id in liked_books and rating >= 4:
                    overlap_users.add(user_id)  
    return overlap_users


def rec_lines():

    rec_lines = []

    with open("goodreads_interactions.csv", 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            user_id, csv_id, _, rating, _ = line.split(",")
            
            if user_id in overlap_users:
                book_id = csv_book_mapping[csv_id]
                rec_lines.append([user_id, book_id, rating])
    return rec_lines