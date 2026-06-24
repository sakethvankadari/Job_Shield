import streamlit as st
import joblib
import re

from scraper import scrape_job


# --------------------------
# Load Saved Model
# --------------------------

model = joblib.load("model/model.pkl")
vectorizer = joblib.load("model/vectorizer.pkl")


# --------------------------
# Clean Text
# --------------------------

def clean_text(text):

    text = text.lower()

    text = re.sub(r"http\S+", "", text)

    text = re.sub(r"www\S+", "", text)

    text = re.sub(r"[^a-zA-Z ]", " ", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()


# --------------------------
# Prediction Function
# --------------------------

def predict(text):

    cleaned = clean_text(text)

    vector = vectorizer.transform([cleaned])

    prediction = model.predict(vector)[0]

    probability = model.predict_proba(vector)[0][1]

    return prediction, probability


# --------------------------
# Streamlit UI
# --------------------------

st.set_page_config(
    page_title="Job Fraud Detector",
    page_icon="🔍"
)
# --------------------------
# Session State
# --------------------------

if "job_text" not in st.session_state:
    st.session_state.job_text = ""

if "job_title" not in st.session_state:
    st.session_state.job_title = ""

st.title("🔍 Job Fraud Detector")

st.write(
    "Detect whether a job posting is Legitimate or Fraudulent."
)

option = st.radio(

    "Choose Input Method",

    [

        "Job URL",

        "Job Description"

    ]

)




# --------------------------
# URL Input
# --------------------------

if option == "Job URL":

    url = st.text_input("Paste Job URL")

    if st.button("Analyze URL"):

        if url:

            title, description = scrape_job(url)

            if title is None:

                st.error(description)

            else:

                st.session_state.job_title = title
                st.session_state.job_text = description

                st.success("Job extracted successfully!")

                st.subheader("Job Title")
                st.write(title)

        else:

            st.warning("Please enter a URL.")

# --------------------------
# Manual Description
# --------------------------

else:

    st.session_state.job_text = st.text_area(
        "Paste Job Description",
        height=300
    )

# --------------------------
# Prediction
# --------------------------

if st.button("Predict Fraud"):

    if st.session_state.job_text.strip() == "":

        st.warning("No job description available.")

    else:

        prediction, probability = predict(st.session_state.job_text)

        confidence = max(probability, 1 - probability) * 100

        st.divider()

        if prediction == 1:

            st.error("⚠ Fraudulent Job Detected")

        else:

            st.success("✅ Legitimate Job Posting")

        st.metric(
            "Fraud Probability",
            f"{probability*100:.2f}%"
        )

        st.metric(
            "Confidence",
            f"{confidence:.2f}%"
        )

        # ------------------------
        # Risk Level
        # ------------------------

        if probability >= 0.80:

            st.error("🔴 Risk Level : HIGH")

        elif probability >= 0.50:

            st.warning("🟡 Risk Level : MEDIUM")

        else:

            st.success("🟢 Risk Level : LOW")

        # ------------------------
        # Progress Bar
        # ------------------------

        st.subheader("Fraud Probability")

        st.progress(float(probability))

        # ------------------------
        # View Extracted Text
        # ------------------------

        with st.expander("View Extracted Job Description"):

            st.write(st.session_state.job_text[:5000])