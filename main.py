from sklearn.feature_extraction.text import TfidfVectorizer
from scripts.search import *
from scripts.liked_books import *
from scripts.recommender impoort *
import pandas as pd


def __name__ = '__main__':

    vectorizer = TfidfVectorizer()
    search(input("Please enter the book title", vectorizer)


    #rank recommendations(books) in the rec_line
    recs = pd.DataFrame(rec_lines, columns=["user_id", "book_id", "rating"])
    recs["book_id"] = recs["book_id"].astype(str)

    popular_recs = recommendations(recs)

    popular_recs[~popular_recs["book_id"].isin(liked_books)].head(10).style.format({'url': make_clickable, 'cover_image': show_image})