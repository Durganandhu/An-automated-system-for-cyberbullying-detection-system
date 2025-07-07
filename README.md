# 💬 Cyberbullying Detection Chat Application

A real-time messaging app built with Python that uses machine learning to detect and block **cyberbullying or harmful content**. Users can also report suspicious messages, which are added to the training dataset and used to improve the model dynamically.

---

## 🚀 Features

- ✅ Real-time chat between multiple users (client-server model)
- 🚨 Detects potentially harmful messages using ML
- 📣 Allows users to report messages
- 🔄 Retrains model on the fly when new reports are submitted
- 💬 Simple and clean GUI using Tkinter
- 🧠 Model: `SGDClassifier` with `TF-IDF Vectorizer`

---

## 📁 Project Structure

.
├── Server3.py # Main server code (ML + sockets)
├── Client3.py # GUI client app (Tkinter + socket)
├── Cleaned_Suspicious_Communication.csv # Dataset for training (text + tags)
└── README.md # Project overview

---

## 🛠 Installation

### 🐍 Requirements

- Python 3.7+
- `pandas`
- `scikit-learn`

### 🔧 Setup

# Install dependencies
pip install pandas scikit-learn

🖥️ How to Run
Start Server:
python Server3.py
Start Client (in a new terminal):
python Client3.py
You can run multiple clients to simulate a real chat environment.

🧠 How the Model Works
Uses a dataset of labeled messages: comments and tagging

Trains a TF-IDF + SGDClassifier pipeline

When a user reports a message:

It is appended to the dataset

Model is re-trained

Message is also blocked immediately using an in-memory set

🛡️ Reporting and Blocking
Messages can be manually reported

Once reported:

Re-sending them is blocked

They're treated as harmful even after restarting

📚 Dataset Format
CSV: Cleaned_Suspicious_Communication.csv

comments	tagging
You're so dumb	1
Let's play tonight	0
tagging: 1 = harmful, 0 = safe




💡 Future Ideas
Add user authentication

Visual dashboard for reports

Export analytics of harmful activity

Integrate with email alerts
