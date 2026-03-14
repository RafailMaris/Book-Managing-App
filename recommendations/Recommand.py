# Handle warning messages
import warnings
warnings.filterwarnings('ignore')
# Data manipulation
import numpy as np
import pandas as pd

# File handling
import os
import pickle

# Time management
import time

# Data visualization
import seaborn as sns
import matplotlib.pyplot as plt
import BookStore.Constants as Constants
# Machine learning
from sklearn.cluster import KMeans
from sklearn.decomposition import TruncatedSVD
from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import silhouette_score
from sklearn.mixture import GaussianMixture
from ollama import chat
from ollama import ChatResponse

from BookStore.DB import get_entries
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # folder where Recommand.py lives

CACHE_FILES = {
    "book_pivot_table": os.path.join(BASE_DIR, "BookAndRatingData", "book_pivot_table.pkl"),
    "books_df": os.path.join(BASE_DIR, "BookAndRatingData", "books_df.pkl"),
    "ratings_df": os.path.join(BASE_DIR, "BookAndRatingData", "ratings_df.pkl"),
    "preds": os.path.join(BASE_DIR, "BookAndRatingData", "preds_KMeans_df.pkl"),
}
def load_pickle(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return pickle.load(f)
    return None

def save_pickle(obj, path):
    with open(path, "wb") as f:
        pickle.dump(obj, f)

def load_raw_data():
    books_df = load_pickle(CACHE_FILES["books_df"])
    ratings_df = load_pickle(CACHE_FILES["ratings_df"])

    if books_df is not None and ratings_df is not None:
        #print("Loaded raw data from cache")
        return books_df, ratings_df

    #print("Loading raw CSV files...")
    books_df = pd.read_csv("../data/Books.csv")
    ratings_df = pd.read_csv("../data/Ratings.csv")

    save_pickle(books_df, CACHE_FILES["books_df"])
    save_pickle(ratings_df, CACHE_FILES["ratings_df"])

    return books_df, ratings_df

def build_or_load_pivot_table(books_df, ratings_df):
    book_pivot_table = load_pickle(CACHE_FILES["book_pivot_table"])

    if book_pivot_table is not None:
        #print("Loaded pivot table from cache")
        return book_pivot_table

    #print("Building pivot table...")
#MERGE: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.merge.html - Like for DB
    df = books_df.merge(ratings_df, on="ISBN")

    user_prune = df.groupby("User-ID")["Book-Rating"].count() > 100#only take the ratings for users that gave over 100 ratings: IS A BOOLEAN SERIES!!!
    user_and_rating = user_prune[user_prune].index
    filtered_rating = df[df['User-ID'].isin(user_and_rating)]#gets the entries where the user ID is in the filter

    rating_prune = df.groupby('Book-Title')[
                       'Book-Rating'].count() >= 50  # same business, but checks if the books have >=50 ratings. better second, since less filtering - nope, it's actually for logic reason
    # if reverse: filter books with more reviews, but maybe those users aren t serious
    famous_books = rating_prune[rating_prune].index

    final_rating = filtered_rating[filtered_rating['Book-Title'].isin(famous_books)]

    book_pivot_table = final_rating.pivot_table(index='Book-Title', columns='User-ID',
                                                values='Book-Rating')  # users up. each popular book: what review was given to it

    book_pivot_table.fillna(0, inplace=True)  # if is NULL, put 0: aka not available

    # if is NULL, put 0: aka not available

    save_pickle(book_pivot_table, CACHE_FILES["book_pivot_table"])#save to pickle

    # Notice how the number of users has shrunk from over a million to just 1,642.
    # This highlights that only 0.14% of users rated more than 100 books, and only 0.9% of books were rated more than 50 times by these avid readers.
    # => order is needed because of logic

    return book_pivot_table
def build_or_load_clusters(book_pivot_table):
    preds = load_pickle(CACHE_FILES["preds"])

    if preds is not None:
        #print("✅ Loaded clusters from cache")
        return preds

    #print("⏳ Training clustering model...")
    # STILL SLOW
    # =>Truncated Singular Value Decomposition (SVD).
    # programming side: https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.TruncatedSVD.html
    # math side: https://www.geeksforgeeks.org/machine-learning/singular-value-decomposition-svd/
    # efficient to work on sparse matrixes

    # the largest eigenvalues have the biggest contribution to the dataset => pick "R" of them: singular values?
    # Tr = X * Wr (X: og one. Wr: top r eigenvectors for the eigenvalues
    # By svd: project all those higher dimensional vectors onto a smaller one
    # => the points closer (in euclidian distance) are closer in the projection.
    # distance is preserved
    # https://www.youtube.com/watch?v=35qKVbvB6-Y
    # https://www.youtube.com/watch?v=gXbThCXjZFM
    # makes from (number of users,books) into (number_of_users, 200)
    # they compress the vote vector into one of dimension 200 such that, instead of: what rates did they give goes to: what kind of reader are they?
    # the vector is "coordinates" on a reader preferances scale.
    # can think of it like: likes fantasy, likes romance based on some indices, but the indices are, actually, related to the "like" of a specific set of books

    tsvd = TruncatedSVD(n_components=200,
                        random_state=42)  # reduce the dimentionality - similar to PCA:https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.TruncatedSVD.html
    book_pivot_table_tsvd = tsvd.fit_transform(book_pivot_table)  # transform the table using tsvd.

    indices = book_pivot_table.index  # IDs of users remaining
    # new dataframe based on a transformed version of the pivot table: dataframe is, pretty much, an excel tabel
    book_rating_clustering = pd.DataFrame(data=book_pivot_table_tsvd, index=indices)
    # split 80% for training, 20% for testing
    train_rate, test_rate = train_test_split(book_rating_clustering, test_size=0.2, random_state=42)
    # retrieve corresponding rating data from the original pivot table
    indices = test_rate.index
    test_set_rating = book_pivot_table.loc[
        indices]  # .loc[] for label-based indexing and .iloc[] for position-based indexing.

    # now: train the model on the data
    # use data clustering
    # what and why: similar books belong to similar clusters: this enables the actual recommandation
    # clustering algorithms: unsupervised ML algorithms

    # the site presents: K-Mean and Gaussian Mixture
    # we use: K++
    # the k algo:

    # Define the range of cluster numbers to test
    cluster_range = range(2, 10)  # Example range from 2 to 20 clusters
    times = []

    # Measure running time for each number of clusters
    for n_clusters in cluster_range:
        start_time = time.time()

        kmeans = KMeans(n_clusters)
        model = kmeans.fit(train_rate)

        end_time = time.time()
        elapsed_time = end_time - start_time
        times.append(elapsed_time)
        # #print(f"Number of clusters: {n_clusters}, Time taken: {elapsed_time:.2f} seconds")

    # Fit the KMeans model
    clusterer_KMeans = KMeans(n_clusters=6, random_state=42).fit(train_rate)

    # Transform the data to get predictions
    # After getting predictions, create a DataFrame
    preds_KMeans = clusterer_KMeans.predict(train_rate)

    # Create a DataFrame with cluster assignments
    preds_KMeans_df = pd.DataFrame(data={'cluster': preds_KMeans}, index=train_rate.index)

    unique_labels = np.unique(preds_KMeans)
    #print(f"Number of clusters: {len(unique_labels)}")

    KMeans_score = silhouette_score(train_rate, preds_KMeans)
    #print('Silhouette score for k-mean approach: ', KMeans_score)

    from difflib import get_close_matches


    save_pickle(preds_KMeans_df, CACHE_FILES["preds"])

    return preds_KMeans_df
def find_book_title(search_term, book_pivot_table):
    """Find the best matching book title with better substring matching"""
    all_titles = book_pivot_table.index.tolist()

    # Exact match first
    if search_term in all_titles:
        return search_term

    # Case-insensitive exact match
    for title in all_titles:
        if title.lower() == search_term.lower():
            return title

    # Substring match - search term contained in title (case-insensitive)
    substring_matches = [title for title in all_titles
                         if search_term.lower() in title.lower()]
    #print(f"Substring matches: {len(substring_matches)}")

    if len(substring_matches) == 1:
        #print(f"Found: '{substring_matches[0]}'")
        return substring_matches[0]
    elif len(substring_matches) > 1:
        #print(f"Multiple matches found for '{search_term}':")
        #for i, match in enumerate(substring_matches, 1):
            #print(f"{i}. {match}")
        # Return the first match or let user choose
        #print(f"Using: '{substring_matches[0]}'")
        return substring_matches[0]

    # If no substring match, try fuzzy matching as fallback
    from difflib import get_close_matches
    fuzzy_matches = get_close_matches(search_term, all_titles, n=5, cutoff=0.6)

    if len(fuzzy_matches) > 0:
        # #print(f"No exact matches. Did you mean one of these?")
        # for i, match in enumerate(fuzzy_matches, 1):
        #     #print(f"{i}. {match}")
        return None  # Don't auto-select fuzzy matches

    #print(f"No matches found for '{search_term}'")
    return None


def recommend_for_unrated_book(book_name, books_df, ratings_df, n_recommendations=10):
    """Recommend books based on metadata when no ratings exist"""

    # Debug: Check what we're searching for
    #print(f"Searching for: '{book_name}'")

    # First try exact match
    #print('unrated book recommendations')
    exact_match = books_df[books_df['Book-Title'] == book_name]

    if not exact_match.empty:
        book_matches = exact_match
        #print(f"Found exact match!")
    else:
        # Try case-insensitive substring match
        # Use regex=False to avoid regex special characters causing issues
        book_matches = books_df[books_df['Book-Title'].str.contains(book_name, case=False, na=False, regex=False)]
        #print(f"Found {len(book_matches)} matches using substring search")

    if book_matches.empty:
        # Debug: Show some sample titles to see what's in the dataset
        #print(f"\nSample titles in dataset:")
        #print(books_df['Book-Title'].head(10).tolist())
        return None

    book = book_matches.iloc[0]
    #print(f"Using book: '{book['Book-Title']}'")

    author = book['Book-Author']
    publisher = book['Publisher']
    year = book.get('Year-Of-Publication', None)
    image = book.get('Image-URL-L', None)

    # #print(f"\n'{book['Book-Title']}' has no ratings in the dataset.")
    # #print(f"Author: {author}")
    # #print(f"Publisher: {publisher}")
    # #print(f"Finding similar books based on author and publisher...\n")

    # Strategy 1: Same author (strongest signal)
    same_author = books_df[books_df['Book-Author'] == author]['ISBN'].tolist()
    #print(f"Found {len(same_author)} books by same author")

    # Strategy 2: Same publisher + similar time period
    # Get the books by the same publisher
    same_publisher = books_df[books_df['Publisher'] == publisher]

    # Filter the books published in the specified year and exclude the original book (book_name)
    same_publisher_and_same_year = []

    # Iterate over rows of the same_publisher DataFrame
    for _, row in same_publisher.iterrows():
        if row['Year-Of-Publication'] == year and row['Book-Title'] != book_name:
            same_publisher_and_same_year.append(row)

    # #print the number of books found
    #print(f"Found {len(same_publisher_and_same_year)} books by publisher in that year")

    # Get books that actually have ratings
    rated_books = ratings_df['ISBN'].unique()

    # Prioritize: same author books that have ratings
    author_recommendations = [isbn for isbn in same_author if isbn in rated_books]
    publisher_recommendations = [row['ISBN'] for row in same_publisher_and_same_year if row['ISBN'] in rated_books]


    # #print(f"Books by same author with ratings: {len(author_recommendations)}")
    # #print(f"Books by same publisher with ratings: {len(publisher_recommendations)}")

    # Combine and get titles
    recommendations = []

    for isbn in author_recommendations[:n_recommendations]:
        title = books_df[books_df['ISBN'] == isbn]['Book-Title'].values[0]
        author = books_df[books_df['ISBN'] == isbn]['Book-Author'].values[0]
        image = books_df[books_df['ISBN'] == isbn]['Image-URL-L'].values[0]
        if title != book['Book-Title']:
            if title not in recommendations:
                recommendations.append({
                    "title": title,
                    "author": author,
                    "image": image,
                    "type": "same author and publisher",
                })
    #print(f"{len(recommendations)} recommended books based on author")
    # Fill remaining with publisher matches
    if len(recommendations) < n_recommendations:
        for isbn in publisher_recommendations:
            title = books_df[books_df['ISBN'] == isbn]['Book-Title'].values[0]
            author = books_df[books_df['ISBN'] == isbn]['Book-Author'].values[0]
            image = books_df[books_df['ISBN'] == isbn]['Image-URL-L'].values[0]
            if title not in recommendations and title != book['Book-Title']:
                recommendations.append({
                    "title": title,
                    "author": author,
                    "image": image,
                    "type": "same publisher",
                })
                if len(recommendations) >= n_recommendations:
                    break

    if recommendations:
        #print(f"\nRecommendations based on same author/publisher:")
        return recommendations[:n_recommendations]
    else:
        return None

def recommend_books(book_name, book_pivot_table, preds, books_df, ratings_df, n_recommendations=10):
    # Try collaborative filtering first
    actual_title = find_book_title(book_name, book_pivot_table)

    if actual_title is None:
        # Book not in filtered dataset - try content-based
        #print(f"'{book_name}' not found in rated books. Switching to content-based recommendations...")
        return recommend_for_unrated_book(book_name, books_df, ratings_df, n_recommendations)

    # Your existing collaborative filtering code
    if actual_title not in preds.index:
        #print(f"'{actual_title}' exists but has no collaborative data. Switching to content-based.")
        return recommend_for_unrated_book(
            actual_title,
            books_df,
            ratings_df,
            n_recommendations
        )
    book_cluster = preds.loc[actual_title, 'cluster']
    cluster_books = preds[preds['cluster'] == book_cluster].index
    book_vector = book_pivot_table.loc[actual_title].values.reshape(1, -1)
    cluster_vectors = book_pivot_table.loc[cluster_books].values
    similarity_scores = np.dot(cluster_vectors, book_vector.T).flatten()
    similar_books_indices = np.argsort(-similarity_scores)[1:n_recommendations + 1]
    similar_books = cluster_books[similar_books_indices]

    results = []

    for title in similar_books:
        row = books_df[books_df['Book-Title'] == title].iloc[0]
        results.append({
            "title": title,
            "author": row['Book-Author'],
            "image": row['Image-URL-L'],
            "type": "similar book (CBF)",
        })

    return results


import re


def clean_recommendations(response_content):

    books = []
    lines = response_content.strip().split("\n")

    for line in lines:
        if "-1" in line:
            return ["-1"]
        match = re.match(r'^\d+\.\s*(.*)', line)
        if match:
            books.append(match.group(1).strip())


    if not books:
        return ["-1"]
    return books


def LLM_based_recommend(book_name, author_name, books_df, n_recommendations=10):
    """Use Ollama LLM for recommendations and validate against database"""
    try:
        # Ask LLM for MORE recommendations than needed (we'll filter)
        content = f"""Please suggest {n_recommendations * 3} well-known book titles similar to '{book_name}' by {author_name}. 

IMPORTANT: Only suggest real, published books that are widely known.
Format as a numbered list with ONLY the book title (no author names):
1. Book Title One
2. Book Title Two
..."""

        response: ChatResponse = chat(
            model='llama3.2',
            messages=[{
                'role': 'user',
                'content': content,
            }]
        )

        llm_response = response['message']['content']

        # Parse LLM response
        lines = llm_response.strip().split('\n')
        suggested_titles = []
        for line in lines:
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith('-')):
                # Remove numbering and clean up
                title = line.split('.', 1)[-1].strip()
                # Remove author names if present (text after "by")
                if ' by ' in title.lower():
                    title = title.split(' by ')[0].strip()
                suggested_titles.append(title)

        # Validate against database
        validated_recommendations = []

        for suggested_title in suggested_titles:
            # Try to find this book in the database
            matches = books_df[
                books_df['Book-Title'].str.contains(suggested_title, case=False, na=False, regex=False)
            ]

            if not matches.empty:
                # Book exists in database!
                actual_title = matches.iloc[0]['Book-Title']
                if actual_title not in validated_recommendations:
                    validated_recommendations.append(actual_title)
                    #print(f"✓ Validated: {suggested_title} -> {actual_title}")
            else:
                # Try fuzzy matching
                from difflib import get_close_matches
                all_titles = books_df['Book-Title'].tolist()
                fuzzy_matches = get_close_matches(suggested_title, all_titles, n=1, cutoff=0.7)

                if fuzzy_matches:
                    validated_recommendations.append(fuzzy_matches[0])
                    #print(f"✓ Fuzzy matched: {suggested_title} -> {fuzzy_matches[0]}")
                else:
                    print(f"✗ Not found in DB: {suggested_title}")

            # Stop when we have enough
            if len(validated_recommendations) >= n_recommendations:
                break

        if validated_recommendations:
            return validated_recommendations[:n_recommendations]
        else:
            # Fallback: return popular books from same genre
            return fallback_popular_books(books_df, n_recommendations)

    except Exception as e:
        #print(f"LLM Error: {e}")
        return fallback_popular_books(books_df, n_recommendations)


def fallback_popular_books(books_df, n_recommendations=10):
    """Fallback: return most popular books from database"""
    # Get books with most ratings
    from collections import Counter

    # This assumes you have ratings_df available
    popular_isbns = books_df['ISBN'].value_counts().head(n_recommendations).index
    popular_books = books_df[books_df['ISBN'].isin(popular_isbns)]['Book-Title'].unique()

    return list(popular_books[:n_recommendations])

def recommendCommunication(book_name, author_name, n_recommendations):
    books_df, ratings_df = load_raw_data()
    book_pivot_table = build_or_load_pivot_table(books_df, ratings_df)
    preds = build_or_load_clusters(book_pivot_table)

    recommendations = recommend_books(
        book_name,
        book_pivot_table,
        preds,
        books_df,
        ratings_df,
        n_recommendations=n_recommendations
    )
    if recommendations is None:
       return []  # return empty list instead of None
    # for recommendation in recommendations:
    #     #print(recommendation)

    return recommendations

    #return recommendations


if __name__ == "__main__":
    book_name = 'The Fellowship of the Ring (The Lord of the Rings, Part 1)'
    recommendations = recommendCommunication(book_name,"J. R. R. Tolkien", n_recommendations=10)
    #print(recommendations)
    # #print(f"\nBooks similar to '{book_name}':")
    # for i, book in enumerate(recommendations, 1):
    #     #print(f"{i}. {book}")


def llm_summary(promt):
    from groq import Groq
    #groq key
    client = Groq(api_key="") 

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": promt}]
    )

    return (completion.choices[0].message.content)



def get_latest_entries(table):
    return get_entries(table)
if __name__ == "__main__":
    def send_notif(request):
        books = get_latest_entries('books')
        authors = get_latest_entries('authors')
        quotes = get_latest_entries('quotes')
        print(books)
        print(authors)
        print(quotes)
    send_notif("a")