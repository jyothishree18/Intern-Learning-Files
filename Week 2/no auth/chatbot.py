import pandas as pd
import nltk
import string

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import nltk

nltk.download("punkt")
nltk.download("punkt_tab")
nltk.download("stopwords")

faq = pd.read_csv("faq.csv")


def preprocess(text):

    text = text.lower()

    tokens = word_tokenize(text)

    tokens = [
        word for word in tokens
        if word not in stopwords.words("english")
        and word not in string.punctuation
    ]

    return " ".join(tokens)


faq["Processed"] = faq["Question"].apply(preprocess)

vectorizer = TfidfVectorizer()

vectors = vectorizer.fit_transform(faq["Processed"])


def get_answer(user_question):

    user_question = preprocess(user_question)

    user_vector = vectorizer.transform([user_question])

    similarity = cosine_similarity(user_vector, vectors)

    index = similarity.argmax()

    score = similarity[0][index]

    if score < 0.30:
        return "Sorry, I couldn't find a suitable answer."

    return faq.iloc[index]["Answer"]