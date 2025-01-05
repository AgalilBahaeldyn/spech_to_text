import tkinter as tk
import speech_recognition as sr
import threading

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
    result_text.set("\u0e01\u0e33\u0e25\u0e31\u0e07\u0e1a\u0e31\u0e19\u0e17\u0e36\u0e01\u0e40\u0e2a\u0e35\u0e22\u0e07...")
    update_red_border(True)
    threading.Thread(target=record_audio).start()  # ใช้ Thread เพื่อไม่ให้บล็อก UI

# ฟังก์ชันสำหรับหยุดการฟัง
def stop_recording():
    global recording
    recording = False
    update_red_border(False)
    result_text.set("\u0e2b\u0e22\u0e38\u0e14\u0e01\u0e32\u0e23\u0e1a\u0e31\u0e19\u0e17\u0e36\u0e01 \u0e01\u0e33\u0e25\u0e31\u0e07\u0e41\u0e1b\u0e25\u0e07\u0e40\u0e2a\u0e35\u0e22\u0e07\u0e40\u0e1b\u0e47\u0e19\u0e02\u0e49\u0e2d\u0e04\u0e27\u0e32\u0e21...")
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
            pass  # ข้ามข้อความที่ไม่สามารถแปลงได้
        except sr.RequestError as e:
            full_text += f"[\u0e02\u0e49\u0e2d\u0e1c\u0e34\u0e14\u0e1e\u0e25\u0e32\u0e14\u0e43\u0e19\u0e01\u0e32\u0e23\u0e40\u0e0a\u0e37\u0e48\u0e2d\u0e21\u0e15\u0e48\u0e2d: {e}] "
    
    result_text.set(full_text.strip())
    if full_text.strip():
        copy_button.pack(pady=20)  # แสดงปุ่ม Copy Text

# ฟังก์ชันแสดง/ซ่อนขอบสีแดง
def update_red_border(show):
    if show:
        root.config(highlightbackground="red", highlightcolor="red", highlightthickness=5)
    else:
        root.config(highlightthickness=0)

# ฟังก์ชันคัดลอกข้อความไปยัง Clipboard
def copy_to_clipboard():
    text = result_text.get()
    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()  # อัปเดต Clipboard

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

# ปุ่มคัดลอกข้อความ (ซ่อนเริ่มต้น)
copy_button = tk.Button(root, text="Copy Text", command=copy_to_clipboard, bg="blue", fg="white", font=("Arial", 12))
copy_button.pack_forget()

# เริ่มโปรแกรม Tkinter
root.mainloop()
