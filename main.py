import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
import threading
import pyautogui
import keyboard  # ไลบรารีสำหรับ Global Hotkey

# สร้าง Recognizer สำหรับการบันทึกเสียง
recognizer = sr.Recognizer()
recording = False  # สถานะการบันทึกเสียง
audio_data = []    # เก็บข้อมูลเสียงทั้งหมดที่บันทึกได้

# ฟังก์ชันสำหรับเริ่มและหยุดการฟังเมื่อกด F7
def toggle_recording():
    global recording
    if not recording:
        start_recording()
    else:
        stop_recording()

# ฟังก์ชันสำหรับเริ่มการฟัง
def start_recording():
    global recording
    recording = True
    result_text.set("กำลังบันทึกเสียง...")
    threading.Thread(target=record_audio).start()  # ใช้ Thread เพื่อไม่ให้บล็อก UI

# ฟังก์ชันสำหรับหยุดการฟัง
def stop_recording():
    global recording
    recording = False
    result_text.set("หยุดการบันทึก กำลังแปลงเสียงเป็นข้อความ...")
    threading.Thread(target=transcribe_audio).start()  # เริ่มแปลงเสียงเป็นข้อความใน Thread แยก

# ฟังก์ชันบันทึกเสียงต่อเนื่อง
def record_audio():
    global recording, audio_data
    audio_data = []  # รีเซ็ตข้อมูลเสียง
    with sr.Microphone() as source:
        while recording:
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                audio_data.append(audio)
            except sr.WaitTimeoutError:
                pass  # ข้ามถ้าไม่มีเสียงภายในเวลาที่กำหนด

# ฟังก์ชันแปลงเสียงทั้งหมดเป็นข้อความ
def transcribe_audio():
    global audio_data
    full_text = ""
    for audio in audio_data:
        try:
            text = recognizer.recognize_google(audio, language="th-TH")
            full_text += text + " "
        except sr.UnknownValueError:
            full_text += "[ไม่สามารถแปลงเสียงเป็นข้อความได้] "
        except sr.RequestError as e:
            full_text += f"[ข้อผิดพลาดในการเชื่อมต่อ: {e}] "
    
    result_text.set("ข้อความที่แปลงได้: " + full_text.strip())
    # ส่งข้อความไปยังโปรแกรมที่โฟกัสอยู่ (เช่น HOSxP)
    pyautogui.write(full_text.strip())

# สร้างหน้าต่างหลัก
root = tk.Tk()
root.title("โปรแกรมบันทึกเสียงและแปลงเสียงเป็นข้อความ")
root.geometry("400x300")

# ตั้งค่าให้หน้าต่างอยู่บนสุดเสมอ
root.attributes("-topmost", True)

# ข้อความแสดงผลลัพธ์
result_text = tk.StringVar()
result_text.set("")

# ปุ่มเริ่มบันทึกเสียง
start_button = tk.Button(root, text="เริ่ม/หยุดบันทึกเสียง (F7)", command=toggle_recording, bg="green", fg="white", font=("Arial", 12))
start_button.pack(pady=20)

# แสดงผลข้อความที่แปลงได้
result_label = tk.Label(root, textvariable=result_text, wraplength=350, font=("Arial", 10), justify="left")
result_label.pack(pady=20)

# กำหนด Global Hotkey สำหรับ F7
keyboard.add_hotkey('F7', toggle_recording)

# เริ่มโปรแกรม Tkinter
root.mainloop()
