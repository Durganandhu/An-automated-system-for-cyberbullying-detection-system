import socket
import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading

class ChatClient:
    def __init__(self, master):
        self.master = master
        self.master.title("Messaging App")
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

        self.text_area = scrolledtext.ScrolledText(master, state='disabled', wrap='word', height=20, width=60)
        self.text_area.pack(padx=10, pady=10)

        self.message_entry = tk.Entry(master, width=50)
        self.message_entry.pack(padx=10, pady=5)
        self.message_entry.bind('<Return>', self.send_message)

        self.send_button = tk.Button(master, text="Send", command=self.send_message)
        self.send_button.pack(padx=10, pady=5)

        self.report_button = tk.Button(master, text="Report Message", command=self.report_message)
        self.report_button.pack(padx=10, pady=5)

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect(('127.0.0.1', 5555))
        except Exception as e:
            messagebox.showerror("Connection Error", str(e))
            self.master.quit()
            return

        threading.Thread(target=self.receive_messages, daemon=True).start()

    def send_message(self, event=None):
        message = self.message_entry.get().strip()
        if message:
            try:
                self.client_socket.send(message.encode('utf-8'))
                self.display_message(f"You: {message}")
                self.message_entry.delete(0, tk.END)
            except Exception as e:
                messagebox.showerror("Send Error", str(e))

    def report_message(self):
        reported = self.message_entry.get().strip()
        if reported:
            try:
                self.client_socket.send(f"REPORT::{reported}".encode('utf-8'))
                self.message_entry.delete(0, tk.END)
            except Exception as e:
                messagebox.showerror("Report Error", str(e))

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if message:
                    if "potentially harmful" in message:
                        messagebox.showwarning("Warning", "Message detected as cyberbullying and blocked.")
                    elif "Thank you for reporting" in message:
                        messagebox.showinfo("Report Submitted", message)
                    else:
                        self.display_message(f"Friend: {message}")
            except Exception as e:
                print("[ERROR] Receiving message:", e)
                break

    def display_message(self, message):
        self.text_area.config(state='normal')
        self.text_area.insert(tk.END, message + "\n")
        self.text_area.config(state='disabled')
        self.text_area.yview(tk.END)

    def on_close(self):
        try:
            self.client_socket.close()
        except:
            pass
        self.master.destroy()

root = tk.Tk()
client = ChatClient(root)
root.mainloop()
