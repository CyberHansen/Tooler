"""
Translator module - separated from GUI for better performance
"""
import time
import numpy as np
import pytesseract
import mss
import cv2
from deep_translator import GoogleTranslator

class TranslatorEngine:
    """Handles the translation functionality with lazy loading of dependencies"""
    
    def __init__(self):
        self.running = False
        self.bbox = None
        self.last_messages = []
        self._translator = None
    
    def _get_translator(self):
        """Lazy load the translator"""
        if self._translator is None:
            self._translator = GoogleTranslator(source='auto', target='no')
        return self._translator
    
    def capture_screen(self, bbox):
        """Capture a portion of the screen"""
        with mss.mss() as sct:
            monitor = {"top": bbox[1], "left": bbox[0], "width": bbox[2] - bbox[0], "height": bbox[3] - bbox[1]}
            screenshot = np.array(sct.grab(monitor))
            return screenshot
    
    def extract_text(self, image):
        """Extract text from an image using OCR"""
        # Convert to grayscale for better OCR
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply threshold to make text more visible
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
        
        # Extract text using pytesseract
        text = pytesseract.image_to_string(thresh)
        return text.strip()
    
    def translate_text(self, text):
        """Translate text to Norwegian"""
        if not text:
            return ""
        
        try:
            translator = self._get_translator()
            translated = translator.translate(text)
            return translated
        except Exception as e:
            return f"Translation error: {str(e)}"
    
    def process_frame(self, bbox):
        """Process a single frame: capture, extract text, and translate"""
        if not bbox:
            return None, None
        
        screenshot = self.capture_screen(bbox)
        text = self.extract_text(screenshot)
        
        # Only process if we have text and it's different from previous messages
        if text and text not in self.last_messages:
            translated = self.translate_text(text)
            
            # Update last messages (keep only the last 5)
            self.last_messages.append(text)
            if len(self.last_messages) > 5:
                self.last_messages.pop(0)
                
            return text, translated
        
        return None, None
