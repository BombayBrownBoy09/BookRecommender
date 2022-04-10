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

# load data
with gzip.open("goodreads_books.json.gz") as f:
    line = f.readline()
data = json.loads(line)

# Extract only the fileds which are rewuired from the json
def parse_fields(line):
    data = json.loads(line)
    return {
        "book_id": data["book_id"], 
        "title": data["title_without_series"], 
        "ratings": data["ratings_count"], 
        "url": data["url"], 
        "cover_image": data["image_url"]
    }

# go line by line and parse each line
books_titles = []
with gzip.open("goodreads_books.json.gz") as f:
    while True:
        line = f.readline()
        if not line:
            break
        fields = parse_fields(line)
        try:
            ratings = int(fields["ratings"])
        except ValueError:
            continue
        # Only take books with more than 15 ratings to reduce the corpus
        if ratings > 15:
            books_titles.append(fields)

titles = pd.DataFrame.from_dict(books_titles)
titles["ratings"] = pd.to_numeric(titles["ratings"])
titles["mod_title"] = titles["title"].str.replace("[^a-zA-Z0-9 ]", "", regex=True)
titles["mod_title"] = titles["mod_title"].str.lower()
titles["mod_title"] = titles["mod_title"].str.replace("\s+", " ", regex=True)
titles = titles[titles["mod_title"].str.len() > 0]
titles.to_json("books_titles.json")

vectorizer = TfidfVectorizer()
tfidf = vectorizer.fit_transform(titles["mod_title"])

def make_clickable(val):
    return '<a target="_blank" href="{}">Goodreads</a>'.format(val, val)

def show_image(val):
    return '<a href="{}"><img src="{}" width=50></img></a>'.format(val, val)

def search(query,vectorizer):
    processed = re.sub("[^a-zA-Z0-9 ]", "", query.lower())
    query_vec = vectorizer.transform([query])
    similarity = cosine_similarity(query_vec, tfidf).flatten()
    # find indices of 10 largest similarity values
    indices = np.argpartition(similarity, -10)[-10:]
    results = titles.iloc[indices]
    results = results.sort_values("ratings", ascending=False)
    
    return results.head(5).style.format({'url': make_clickable, 'cover_image': show_image})

liked_books = input()
if type(liked_books)==list:
  continue

 # form a dictionary of books where key is csv id from interactions and value is book id from json
csv_book_mapping = {}

with open("book_id_map.csv", "r") as f:
    while True:
        line = f.readline()
        if not line:
            break
        csv_id, book_id = line.strip().split(",")
        csv_book_mapping[csv_id] = book_id
        
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
# Find books which the overlapped users have read
# reclines contains potential books we want to read
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
            
recs = pd.DataFrame(rec_lines, columns=["user_id", "book_id", "rating"])
recs["book_id"] = recs["book_id"].astype(str)

top_recs = recs["book_id"].value_counts().head(10)
top_recs = top_recs.index.values
books_titles = pd.read_json("books_titles.json")
books_titles["book_id"] = books_titles["book_id"].astype(str)
# find books that are more popular among users like us
all_recs = recs["book_id"].value_counts()
all_recs = all_recs.to_frame().reset_index()
all_recs.columns = ["book_id", "book_count"]
all_recs = all_recs.merge(books_titles, how="inner", on="book_id")

# Assign a score to compare each book( If a book is more popular among our set and less popular on goodreads it is going to be recommended)
# looking for books that are popular among users like us but not necessarily on all of goodreads
all_recs["score"] = all_recs["book_count"] * (all_recs["book_count"] / all_recs["ratings"])

popular_recs = all_recs[all_recs["book_count"] > 200].sort_values("score", ascending=False)

def make_clickable(val):
    return '<a target="_blank" href="{}">Goodreads</a>'.format(val, val)

def show_image(val):
    return '<a href="{}"><img src="{}" width=50></img></a>'.format(val, val)
