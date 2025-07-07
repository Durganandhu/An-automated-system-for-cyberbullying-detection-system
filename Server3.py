import socket
import threading
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline

clients = []
lock = threading.Lock()
reported_messages = set()  # Store reported messages for immediate blocking

def load_data():
    df = pd.read_csv("Cleaned_Suspicious_Communication.csv")
    df.dropna(subset=['comments', 'tagging'], inplace=True)
    df = df[df['comments'].str.strip() != '']
    texts = df['comments'].astype(str).tolist()
    labels = df['tagging'].astype(int).tolist()
    return texts, labels

texts, labels = load_data()

def train_model(texts, labels):
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(texts)
    classifier = SGDClassifier(loss='log_loss')
    classifier.fit(X, labels)  # Full fit instead of partial_fit
    return Pipeline([
        ('vectorizer', vectorizer),
        ('classifier', classifier)
    ])

model = train_model(texts, labels)

def is_cyberbullying(message):
    if not message.strip():
        return False
    if message.lower() in reported_messages:  # Check in-memory reported messages
        return True
    prediction = model.predict([message])[0]
    return prediction == 1

def add_reported_to_training(text):
    global model, texts, labels, reported_messages
    reported_messages.add(text.lower())
    pd.DataFrame([[text, 1]], columns=['comments', 'tagging']).to_csv(
        "Cleaned_Suspicious_Communication.csv", mode='a', header=False, index=False
    )
    texts, labels = load_data()
    model = train_model(texts, labels)

def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break

            if message.startswith("REPORT::"):
                reported_text = message.split("REPORT::", 1)[1].strip()
                if reported_text:
                    print(f"[INFO] Reported message: {reported_text}")
                    add_reported_to_training(reported_text)
                    client_socket.send("Thank you for reporting. The message will now be treated as harmful.".encode('utf-8'))
            elif is_cyberbullying(message):
                client_socket.send("Warning: Your message was detected as potentially harmful.".encode('utf-8'))
            else:
                broadcast(message, client_socket)
        except Exception as e:
            print("Client error:", e)
            break

    client_socket.close()
    with lock:
        if client_socket in clients:
            clients.remove(client_socket)

def broadcast(message, sender_socket):
    with lock:
        for client in clients:
            if client != sender_socket:
                try:
                    client.send(message.encode('utf-8'))
                except:
                    client.close()
                    clients.remove(client)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 5555))
    server.listen(5)
    print("[STARTED] Server listening on 127.0.0.1:5555")

    while True:
        client_socket, addr = server.accept()
        with lock:
            clients.append(client_socket)
        print(f"[CONNECTED] {addr}")
        threading.Thread(target=handle_client, args=(client_socket,), daemon=True).start()

if __name__ == "__main__":
    start_server()
