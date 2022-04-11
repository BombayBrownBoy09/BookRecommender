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


# parse each line
# go line by line and parse each line

def parse_lineByline():

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
    return tfidf, vectorizer


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
