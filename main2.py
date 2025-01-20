import tkinter as tk
from tkinter import scrolledtext, messagebox
import speech_recognition as sr
import threading
import pyperclip  # สำหรับคัดลอกข้อความไปยัง Clipboard
import time  # สำหรับตรวจจับเวลาไม่มีเสียง


class SpeechToTextApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Speech to Text (Real-time)")
        self.is_listening = False
        self.last_audio_time = time.time()  # เก็บเวลาล่าสุดที่ได้รับเสียง

        # ทำให้หน้าต่างอยู่ด้านบนเสมอ
        self.root.attributes('-topmost', True)

        # Status Label
        self.status_label = tk.Label(root, text="สถานะ: หยุดการฟัง", font=("Arial", 12), fg="white", bg="red")
        self.status_label.pack(fill=tk.X, padx=10, pady=5)

        # Input Area
        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Arial", 12), width=40, height=8)
        self.text_area.pack(fill=tk.BOTH, expand=False, padx=10, pady=10)

        # Button Frame
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(fill=tk.X, padx=10, pady=5)

                # Version Label
        self.version_label = tk.Label(root, text="version 1.2", font=("Arial", 8), fg="gray")
        self.version_label.pack(side=tk.BOTTOM, pady=5)  # วางไว้ที่ด้านล่างของหน้าต่าง
        # Button Frame (Row 1)
        self.button_frame_row1 = tk.Frame(root)
        self.button_frame_row1.pack(fill=tk.X, padx=10, pady=5)

        self.start_button = tk.Button(self.button_frame_row1, text="Start Listening", command=self.start_listening, font=("Arial", 10))
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = tk.Button(self.button_frame_row1, text="Stop Listening", command=self.stop_listening, state=tk.DISABLED, font=("Arial", 10))
        self.stop_button.pack(side=tk.LEFT, padx=5)

        # Button Frame (Row 2)
        self.button_frame_row2 = tk.Frame(root)
        self.button_frame_row2.pack(fill=tk.X, padx=10, pady=5)

        self.copy_button = tk.Button(self.button_frame_row2, text="Copy Text", command=self.copy_text, font=("Arial", 10))
        self.copy_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = tk.Button(self.button_frame_row2, text="Clear Text", command=self.clear_text, font=("Arial", 10))
        self.clear_button.pack(side=tk.LEFT, padx=5)



        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    def start_listening(self):
        self.is_listening = True
        self.last_audio_time = time.time()  # ตั้งเวลาเริ่มต้น
        self.status_label.config(text="สถานะ: กำลังฟัง...", bg="green")  # อัปเดต Badge Status
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        threading.Thread(target=self.listen_in_background).start()
        threading.Thread(target=self.check_no_input_timeout).start()  # ตรวจสอบเวลาไม่มีเสียง

    def stop_listening(self):
        self.is_listening = False
        self.status_label.config(text="สถานะ: หยุดการฟัง", bg="red")  # อัปเดต Badge Status
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def clear_text(self):
        self.text_area.delete('1.0', tk.END)

    def copy_text(self):
        text = self.text_area.get('1.0', tk.END).strip()
        if text:
            pyperclip.copy(text)
        else:
            messagebox.showwarning("Copy Text", "ไม่มีข้อความสำหรับคัดลอก")

    def listen_in_background(self):
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)  # ปรับเสียงรบกวนในสภาพแวดล้อม
            while self.is_listening:
                try:
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                    text = self.recognizer.recognize_google(audio, language="th-TH")
                    self.last_audio_time = time.time()  # อัปเดตเวลาที่ได้ยินเสียงล่าสุด
                    self.text_area.insert(tk.END, f"{text} ")  # ต่อข้อความในบรรทัดเดิม
                    self.text_area.see(tk.END)  # เลื่อนหน้าจอลงอัตโนมัติ
                except sr.WaitTimeoutError:
                    pass  # ข้ามกรณีไม่มีเสียงพูดในเวลาที่กำหนด
                except sr.UnknownValueError:
                    pass  # ข้ามข้อความ "ไม่สามารถแปลงเสียงได้"
                except sr.RequestError as e:
                    self.text_area.insert(tk.END, f"[API Error: {e}] ")
                except Exception as e:
                    self.text_area.insert(tk.END, f"[Error: {e}] ")

    def check_no_input_timeout(self):
        while self.is_listening:
            time.sleep(1)  # ตรวจสอบทุก 1 วินาที
            if time.time() - self.last_audio_time > 15:  # หากไม่มีเสียงเกิน 15 วินาที
                self.stop_listening()
                break


# Main Program
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("300x320")  # กำหนดขนาดเริ่มต้น
    app = SpeechToTextApp(root)
    root.mainloop()
