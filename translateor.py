import cv2
import numpy as np
import mss
import pytesseract
import customtkinter as ctk
import pygetwindow as gw
import threading
import time
from deep_translator import GoogleTranslator

pytesseract.pytesseract.tesseract_cmd = r"C:\Users\mathi\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

class ChatTranslatorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Game Chat Translator")
        self.geometry("600x450")
        self.running = False
        self.bbox = None
        self.custom_bbox = None 
        self.last_messages = []  

        ctk.set_appearance_mode("dark")
        self.create_widgets()

    def create_widgets(self):
        self.window_label = ctk.CTkLabel(self, text="Select game window:")
        self.window_label.pack(pady=5)

        self.window_var = ctk.StringVar()
        self.window_dropdown = ctk.CTkComboBox(self, variable=self.window_var, values=self.get_window_list())
        self.window_dropdown.pack(pady=5)

        self.refresh_button = ctk.CTkButton(self, text="Refresh list", command=self.update_window_list)
        self.refresh_button.pack(pady=5)

        self.select_area_button = ctk.CTkButton(self, text="Select area", command=self.select_capture_area)
        self.select_area_button.pack(pady=5)

        self.start_button = ctk.CTkButton(self, text="Start", command=self.start_translation, state="disabled")
        self.start_button.pack(pady=5)

        self.output_text = ctk.CTkTextbox(self, width=500, height=200)
        self.output_text.pack(pady=5)

        self.stop_button = ctk.CTkButton(self, text="Stop", command=self.stop_translation, state="disabled")
        self.stop_button.pack(pady=5)

    def get_window_list(self):
        return [win.title for win in gw.getAllWindows() if win.title]

    def update_window_list(self):
        self.window_dropdown.configure(values=self.get_window_list())

    def get_window_bbox(self, window_title):
        try:
            win = gw.getWindowsWithTitle(window_title)[0]
            return (win.left, win.top, win.right, win.bottom)
        except IndexError:
            self.output_text.insert("end", "❌ Window not found! Try again.\n")
            return None

    def select_capture_area(self):
        window_title = self.window_var.get()
        bbox = self.get_window_bbox(window_title)

        if not bbox:
            return

        x1, y1, x2, y2 = bbox

        with mss.mss() as sct:
            screenshot = np.array(sct.grab(bbox))
            screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)

        MAX_WIDTH = 800
        MAX_HEIGHT = 600

        height, width, _ = screenshot.shape
        scale_factor = min(MAX_WIDTH / width, MAX_HEIGHT / height, 1.0)

        if scale_factor < 1.0:
            resized_screenshot = cv2.resize(screenshot, (0, 0), fx=scale_factor, fy=scale_factor)
        else:
            resized_screenshot = screenshot

        roi = cv2.selectROI("Select area (Press ENTER to confirm)", resized_screenshot, fromCenter=False, showCrosshair=True)
        cv2.destroyAllWindows()

        if roi != (0, 0, 0, 0):
            x, y, w, h = roi

            x = int(x / scale_factor)
            y = int(y / scale_factor)
            w = int(w / scale_factor)
            h = int(h / scale_factor)

            self.custom_bbox = (x1 + x, y1 + y, x1 + x + w, y1 + y + h)
            self.output_text.insert("end", f"✅ Area selected: {self.custom_bbox}\n")
            self.start_button.configure(state="normal")


    def capture_text_from_window(self):
        with mss.mss() as sct:
            while self.running:
                if self.custom_bbox:
                    screenshot = sct.grab(self.custom_bbox)
                    img = np.array(screenshot)
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                    extracted_text = pytesseract.image_to_string(gray, lang="rus+eng+deu+fra+spa+ita+chi_sim+jpn").strip()

                    messages = extracted_text.split("\n")

                    for message in messages:
                        message = message.strip()
                        if message and message not in self.last_messages:
                            self.last_messages.append(message)

                            if len(self.last_messages) > 10:
                                self.last_messages.pop(0)

                            try:
                                translated_text = GoogleTranslator(source="auto", target="no").translate(message)
                                self.output_text.insert("end", f"{translated_text}\n")
                                self.output_text.yview_moveto(1)
                            except Exception as e:
                                self.output_text.insert("end", "⚠ Translation error, check your connection!\n")

                time.sleep(1)

    def start_translation(self):
        if not self.custom_bbox:
            self.output_text.insert("end", "⚠ Select an area first!\n")
            return

        self.running = True
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")

        threading.Thread(target=self.capture_text_from_window, daemon=True).start()

    def stop_translation(self):
        self.running = False
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.output_text.insert("end", "🛑 Translation stopped.\n")

if __name__ == "__main__":
    app = ChatTranslatorApp()
    app.mainloop()
