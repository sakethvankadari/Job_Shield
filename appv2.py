import streamlit as st
import joblib
import re

from scraper import scrape_job


# -----------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------

st.set_page_config(
    page_title="Job Shield",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# -----------------------------------------------------
# LOAD MODEL
# -----------------------------------------------------

model = joblib.load("model/model.pkl")
vectorizer = joblib.load("model/vectorizer.pkl")


# -----------------------------------------------------
# SESSION STATE
# -----------------------------------------------------

if "prediction_done" not in st.session_state:
    st.session_state.prediction_done = False

if "job_text" not in st.session_state:
    st.session_state.job_text = ""

if "prediction" not in st.session_state:
    st.session_state.prediction = None

if "probability" not in st.session_state:
    st.session_state.probability = 0

if "title" not in st.session_state:
    st.session_state.title = ""


# -----------------------------------------------------
# CSS
# -----------------------------------------------------

st.markdown("""

<style>

/* ---------- Main Background ---------- */

.stApp{
    background: linear-gradient(135deg,#0F172A,#111827);
    color:white;
}

/* ---------- Sidebar ---------- */

section[data-testid="stSidebar"]{
    background:#111827;
    border-right:1px solid #334155;
}

/* ---------- Hero Banner ---------- */

.hero{
    background:linear-gradient(135deg,#2563EB,#7C3AED);
    padding:45px;
    border-radius:22px;
    text-align:center;
    margin-bottom:25px;
    box-shadow:0px 10px 30px rgba(0,0,0,.45);
}

.hero h1{
    color:white;
    font-size:46px;
    margin-bottom:8px;
}

.hero p{
    color:white;
    font-size:18px;
}

/* ---------- Card ---------- */

.card{

    background:#1E293B;

    padding:22px;

    border-radius:18px;

    border:1px solid rgba(255,255,255,.08);

    box-shadow:0px 8px 20px rgba(0,0,0,.35);

    margin-top:12px;

}

/* ---------- Buttons ---------- */

.stButton>button{

width:100%;

height:55px;

background:linear-gradient(90deg,#2563EB,#7C3AED);

color:white;

font-size:18px;

font-weight:bold;

border-radius:14px;

border:none;

transition:0.3s;

}

.stButton>button:hover{

transform:translateY(-2px);

box-shadow:0px 10px 20px rgba(59,130,246,.45);

}

/* ---------- Textbox ---------- */

textarea{

border-radius:15px !important;

}

/* ---------- Footer ---------- */

.footer{

margin-top:40px;

text-align:center;

color:#CBD5E1;

font-size:15px;

}

</style>

""",unsafe_allow_html=True)


# -----------------------------------------------------
# SIDEBAR
# -----------------------------------------------------

with st.sidebar:

    st.title("🛡️ Job Shield")

    st.write("### AI-Powered Job Fraud Detection")

    st.divider()

    st.write("### Technologies")

    st.write("✅ Python")

    st.write("✅ Streamlit")

    st.write("✅ Scikit-Learn")

    st.write("✅ BeautifulSoup")

    st.write("✅ TF-IDF")

    st.write("✅ Logistic Regression")

    st.divider()

    st.success("Model Accuracy")

    st.metric("Accuracy","97.54%")

    st.divider()

    st.info(
        "Analyze a Job URL or paste a Job Description to detect fraudulent job postings."
    )


# -----------------------------------------------------
# HERO SECTION
# -----------------------------------------------------

st.markdown("""

<div class="hero">

<h1>🛡️ Job Shield</h1>

<p>

AI-Powered Job Fraud Detection System

</p>

<p>

Detect suspicious job postings instantly using
Machine Learning and NLP.

</p>

</div>

""",unsafe_allow_html=True)


# -----------------------------------------------------
# INPUT TABS
# -----------------------------------------------------

tab1,tab2 = st.tabs(
[
"🌐 Analyze from URL",
"📝 Paste Job Description"
]
)


# -----------------------------------------------------
# URL TAB
# -----------------------------------------------------

with tab1:

    url = st.text_input(
        "Paste Job URL"
    )

    analyze_url = st.button(
        "🚀 Analyze Job URL"
    )


# -----------------------------------------------------
# DESCRIPTION TAB
# -----------------------------------------------------

with tab2:

    description = st.text_area(

        "Paste Job Description",

        height=250

    )

    analyze_text = st.button(

        "🚀 Analyze Description"

    )
    # -----------------------------------------------------
# CLEAN TEXT
# -----------------------------------------------------

def clean_text(text):

    text = text.lower()

    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"www\S+", "", text)

    text = re.sub(r"[^a-zA-Z ]", " ", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()


# -----------------------------------------------------
# PREDICTION FUNCTION
# -----------------------------------------------------

def predict_job(text):

    cleaned = clean_text(text)

    vector = vectorizer.transform([cleaned])

    prediction = model.predict(vector)[0]

    probability = model.predict_proba(vector)[0][1]

    return prediction, probability


# -----------------------------------------------------
# URL ANALYSIS
# -----------------------------------------------------

if analyze_url:

    if url.strip() == "":

        st.warning("Please enter a Job URL.")

    else:

        with st.spinner("Analyzing Job URL..."):

            title, description = scrape_job(url)

            if title is None:

                st.error(description)

            else:

                prediction, probability = predict_job(description)

                st.session_state.prediction_done = True
                st.session_state.title = title
                st.session_state.job_text = description
                st.session_state.prediction = prediction
                st.session_state.probability = probability


# -----------------------------------------------------
# DESCRIPTION ANALYSIS
# -----------------------------------------------------

if analyze_text:

    if description.strip() == "":

        st.warning("Please paste a Job Description.")

    else:

        with st.spinner("Analyzing Job Description..."):

            prediction, probability = predict_job(description)

            st.session_state.prediction_done = True
            st.session_state.title = "Manual Job Description"
            st.session_state.job_text = description
            st.session_state.prediction = prediction
            st.session_state.probability = probability


# -----------------------------------------------------
# SHOW RESULT
# -----------------------------------------------------

if st.session_state.prediction_done:

    st.divider()

    confidence = max(
        st.session_state.probability,
        1 - st.session_state.probability
    ) * 100

    st.markdown("## 📊 Analysis Result")

    if st.session_state.prediction == 1:

        st.markdown("""
<div style='
background:#EF4444;
padding:20px;
border-radius:15px;
text-align:center;
font-size:28px;
font-weight:bold;
color:white;
box-shadow:0px 8px 20px rgba(0,0,0,.3);
'>
🔴 SUSPICIOUS JOB
</div>
""", unsafe_allow_html=True)

    else:

        st.markdown("""
<div style='
background:#22C55E;
padding:20px;
border-radius:15px;
text-align:center;
font-size:28px;
font-weight:bold;
color:white;
box-shadow:0px 8px 20px rgba(0,0,0,.3);
'>
🟢 SAFE JOB
</div>
""", unsafe_allow_html=True)

    st.write("### Job Title")

    st.info(st.session_state.title)

    col1, col2, col3 = st.columns(3)

    with col1:

        
            st.markdown(f"""
<div class="card">

<h4 align="center">📊 Fraud Probability</h4>

<h1 align="center" style="color:#3B82F6;">
{st.session_state.probability*100:.2f}%
</h1>

</div>
""", unsafe_allow_html=True)
        

    with col2:

        
            st.markdown(f"""
<div class="card">

<h4 align="center">🎯 Confidence</h4>

<h1 align="center" style="color:#22C55E;">
{confidence:.2f}%
</h1>

</div>
""", unsafe_allow_html=True)
        

    with col3:

        probability = st.session_state.probability

        if probability >= 0.80:

            st.error("🔴 HIGH")

        elif probability >= 0.50:

            st.warning("🟡 MEDIUM")

        else:

            st.success("🟢 LOW")

    st.write("### Fraud Probability")

    st.progress(float(st.session_state.probability))

    st.write("### Confidence")

    st.progress(float(confidence/100))

    with st.expander("📄 View Job Description"):

        st.write(st.session_state.job_text)

    st.download_button(

        "📥 Download Result",

        data=f"""

Job Shield Report

==========================

Prediction :
{"Fraudulent" if st.session_state.prediction==1 else "Legitimate"}

Fraud Probability :
{st.session_state.probability*100:.2f}%

Confidence :
{confidence:.2f}%

Job Title :
{st.session_state.title}

""",

        file_name="JobShield_Report.txt"

    )


# -----------------------------------------------------
# FOOTER
# -----------------------------------------------------

st.markdown("<br><br>",unsafe_allow_html=True)

st.markdown("""

---

<div class="footer">

<h2>🛡️ Job Shield</h2>

AI-Powered Job Fraud Detection System

<br>

Made with ❤️ using

Python • Machine Learning • NLP • Streamlit

<br><br>

Version 2.0

</div>

""", unsafe_allow_html=True)