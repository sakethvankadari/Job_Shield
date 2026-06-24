import re
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report


# -----------------------------
# Load Dataset
# -----------------------------
df = pd.read_csv("fake_job_postings.csv")


# Replace missing values
df.fillna("", inplace=True)


# -----------------------------
# Combine Important Columns
# -----------------------------
df["text"] = (
    df["title"] + " " +
    df["company_profile"] + " " +
    df["description"] + " " +
    df["requirements"] + " " +
    df["benefits"]
)


# -----------------------------
# Text Cleaning
# -----------------------------
def clean_text(text):

    text = text.lower()

    text = re.sub(r"http\S+", "", text)

    text = re.sub(r"www\S+", "", text)

    text = re.sub(r"[^a-zA-Z ]", " ", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()


df["text"] = df["text"].apply(clean_text)


# -----------------------------
# Features and Labels
# -----------------------------
X = df["text"]

y = df["fraudulent"]


# -----------------------------
# TF-IDF Vectorizer
# -----------------------------
vectorizer = TfidfVectorizer(
    stop_words="english",
    max_features=8000,
    ngram_range=(1, 2)
)

X = vectorizer.fit_transform(X)


# -----------------------------
# Train/Test Split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# -----------------------------
# Train Model
# -----------------------------
model = LogisticRegression(
    max_iter=1000,
    class_weight="balanced"
)

model.fit(X_train, y_train)


# -----------------------------
# Evaluate
# -----------------------------
predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("\nAccuracy :", round(accuracy * 100, 2), "%\n")

print(classification_report(y_test, predictions))


# -----------------------------
# Save Model
# -----------------------------
joblib.dump(model, "model/model.pkl")

joblib.dump(vectorizer, "model/vectorizer.pkl")

print("\nModel Saved Successfully!")