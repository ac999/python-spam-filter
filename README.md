# 🧼 SSOSM: Spam Filter

**Author:** Andrei Cristian  
**Version:** 0.1

---

## 📌 Overview

SSOSM (Simple Spam Or Sanitized Mail) is a Python-based spam filtering tool designed to classify text or file content using a Naive Bayes classifier trained on manually labeled data. It can detect spam from raw text files and HTML emails using a lightweight and customizable dataset.

This project is ideal for security research, email filtering prototypes, or educational purposes on NLP and machine learning fundamentals.

---

## 📁 Project Structure

```
.
├── main.py              # Main script containing training and scanning logic
├── requirements.txt     # Dependencies
├── .python-version      # Python version (3.7.12)
```

---

## 🛠 Features

- ✅ Detects spam content using Multinomial Naive Bayes
- ✅ Supports plain text and HTML content (auto-strips HTML)
- ✅ Trains on a CSV dataset (`dataset.csv`) generated from labeled folders
- ✅ Scans directories for potential spam files
- ✅ Outputs results to a log file
- ✅ Saves and reuses trained model and vectorizer with `pickle`

---

## 🧪 Requirements

Python 3.7.12  
Install dependencies with:

```bash
pip install -r requirements.txt
```

---

## ⚙️ Usage

### 1. Print Project Info

```bash
python main.py -info info.txt
```

Writes project metadata to the file `info.txt`.

---

### 2. Scan a Folder for Spam

```bash
python main.py -scan <directory_path> <output_file>
```

Scans all files in the specified directory, classifies them, and writes results to the output file. Each line contains:

```
<filename>|cln  # Clean
<filename>|inf  # Infected (Spam)
```

---

### 3. (Optional) Train Model from Labeled Dataset

_Note: Training logic is currently commented out in `main.py`. You can enable it manually for re-training._

Directory structure for training:
```
<root>
├── Lot1/
│   ├── Clean/
│   └── Spam/
└── Lot2/
    ├── Clean/
    └── Spam/
```

Each subfolder should contain text files. After uncommenting the `train()` function and adjusting the logic:

```bash
# Enable and modify in main.py
# python main.py -train <path_to_data_root>
```

It generates a new `dataset.csv`, trains the classifier, and saves:
- `naive_bayes_clf.pkl` – the trained model
- `naive_bayes_cv.pkl` – the fitted `CountVectorizer`

---

## 🔒 Security Notes

- Only plain text and HTML are processed (malicious scripts in HTML are stripped).
- Binary files are ignored.
- This tool is not a full antivirus scanner — it is intended for text-based spam detection.

---

## 📄 Output Example

```
offer.txt|inf
newsletter.html|cln
free-gift.msg|inf
```

---

## 🧹 Future Improvements

- ✅ Enable training via CLI argument
- 📊 Add confusion matrix and classification reports
- 🤖 Extend to detect phishing keywords
- 🗂 Add support for `.eml` email formats
- 🌐 Web dashboard (Flask/FastAPI)

---

## 📜 License

This project is currently not licensed. Contact the author for reuse or contributions.
