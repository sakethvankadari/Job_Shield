# 🛡️ Job Shield — AI-Powered Job Fraud Detection System

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-red?logo=streamlit)
![Scikit-Learn](https://img.shields.io/badge/ScikitLearn-ML-orange?logo=scikit-learn)
![Accuracy](https://img.shields.io/badge/Accuracy-97.54%25-brightgreen)
![License](https://img.shields.io/badge/License-MIT-blue) 

Job Shield is a Machine Learning web application that detects **fraudulent job postings** in real time. Paste a job URL or a job description, and the model instantly tells you whether the posting is **safe or suspicious** — along with a fraud probability score and risk level.

---

## 📸 Demo

> Analyze any job posting in seconds — just paste the URL or description.

| Safe Job | Suspicious Job |
|----------|----------------|
| 🟢 SAFE JOB | 🔴 SUSPICIOUS JOB |
| Low fraud probability | High fraud probability |

---

## ✨ Features

- 🌐 **URL Analysis** — Paste any job posting URL and the app scrapes and analyzes it automatically
- 📝 **Description Analysis** — Manually paste a job description for instant prediction
- 📊 **Fraud Probability Score** — Shows exact fraud % with a visual progress bar
- 🎯 **Confidence Score** — How confident the model is in its prediction
- 🔴🟡🟢 **Risk Level** — HIGH / MEDIUM / LOW risk classification
- 📥 **Download Report** — Export the analysis result as a `.txt` file
- 🧹 **Smart Text Cleaning** — Removes URLs, special characters, and noise before prediction

---

## 🧠 How It Works

1. **Data** — Trained on the [Fake Job Postings dataset](https://www.kaggle.com/datasets/shivamb/real-or-fake-fake-jobposting-prediction) (~18,000 job postings)
2. **Feature Engineering** — Combines `title`, `company_profile`, `description`, `requirements`, and `benefits` into one text field
3. **Vectorization** — TF-IDF with `max_features=8000` and `ngram_range=(1,2)` to capture word pairs
4. **Model** — Logistic Regression with `class_weight="balanced"` to handle class imbalance
5. **Accuracy** — **97.54%** on the test set

---

## 📁 Project Structure

```
job-shield/
│
├── model/
│   ├── model.pkl           # Trained Logistic Regression model
│   └── vectorizer.pkl      # Fitted TF-IDF vectorizer
│
├── app.py                  # Streamlit app (Version 1)
├── appv2.py                # Streamlit app (Version 2 — recommended)
├── scraper.py              # Web scraper using BeautifulSoup
├── train_model.py          # Model training script
├── fake_job_postings.csv   # Training dataset
├── requirements.txt        # Python dependencies
└── README.md
```

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/job-shield.git
cd job-shield
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Train the Model

> Skip this step if `model/model.pkl` and `model/vectorizer.pkl` already exist.

```bash
mkdir model
python train_model.py
```

### 4. Run the App

```bash
streamlit run appv2.py
```

Open your browser at `http://localhost:8501`

---

## 📦 Requirements

```
streamlit
scikit-learn
joblib
pandas
requests
beautifulsoup4
```

> Install all at once: `pip install -r requirements.txt`

---

## 🧪 Model Performance

| Metric | Score |
|--------|-------|
| Accuracy | **97.54%** |
| Vectorizer | TF-IDF (8000 features, bigrams) |
| Algorithm | Logistic Regression |
| Class Balancing | `class_weight="balanced"` |
| Train/Test Split | 80% / 20% (stratified) |

---

## 🔍 Risk Level Classification

| Fraud Probability | Risk Level |
|-------------------|------------|
| ≥ 80% | 🔴 HIGH |
| 50% – 79% | 🟡 MEDIUM |
| < 50% | 🟢 LOW |

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Core language |
| Streamlit | Web UI |
| Scikit-Learn | ML model & TF-IDF |
| BeautifulSoup | Web scraping |
| Joblib | Model serialization |
| Pandas | Data processing |
| Regex | Text cleaning |

---

## 📌 Notes

- The scraper works best on publicly accessible job boards. Some sites (e.g. LinkedIn) may block automated requests.
- The model was trained on English-language job postings. Non-English descriptions may give less accurate results.
- For best results, include as much of the job description as possible when using manual input.

---

## 🚀 Future Improvements

- [ ] Add support for more job board sites (LinkedIn, Indeed, Glassdoor)
- [ ] Try advanced models (Random Forest, XGBoost, BERT)
- [ ] Add history of analyzed jobs within the session
- [ ] Deploy on Streamlit Cloud / Hugging Face Spaces

---

## 👤 Author

**Your Name**
- GitHub: [sakethvankadari](https://github.com/sakethvankadari)


---

## 📄 License

This project is licensed under the MIT License.

---

> ⭐ If you found this project useful, consider giving it a star on GitHub!
