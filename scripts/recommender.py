imoort pandas as pd
import numpy as np



def make_clickable(val):
    return '<a target="_blank" href="{}">Goodreads</a>'.format(val, val)

def show_image(val):
    return '<a href="{}"><img src="{}" width=50></img></a>'.format(val, val)

def recommendations(recs):
    # Find the books with most ratings
    top_recs = recs["book_id"].value_counts().head(10)
    top_recs = top_recs.index.values
    books_titles = pd.read_json("books_titles.json")
    books_titles["book_id"] = books_titles["book_id"].astype(str)
    books_titles[books_titles["book_id"].isin(top_recs)]
    # find books that are more popular among users like us
    all_recs = recs["book_id"].value_counts()
    all_recs = all_recs.to_frame().reset_index()
    all_recs.columns = ["book_id", "book_count"]
    all_recs = all_recs.merge(books_titles, how="inner", on="book_id")

    all_recs["score"] = all_recs["book_count"] * (all_recs["book_count"] / all_recs["ratings"])

    all_recs.sort_values("score", ascending=False).head(10)

    all_recs[all_recs["book_count"] > 200].sort_values("score", ascending=False).head(10)

    popular_recs = all_recs[all_recs["book_count"] > 200].sort_values("score", ascending=False)

    return popular_recs
