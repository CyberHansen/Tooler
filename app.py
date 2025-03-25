import os
import sys
import threading
from time import sleep
import customtkinter as Ctk
from CTkMessagebox import CTkMessagebox
from PIL import Image

# Configure the customtkinter appearance - this is lightweight
Ctk.set_appearance_mode("dark")
Ctk.set_default_color_theme("blue")

# Add the current directory to the path to ensure modules can be found
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Basic imports needed for core functionality
if sys.stdout is None:
    sys.stdout = open(os.devnull, "w")
if sys.stderr is None:
    sys.stderr = open(os.devnull, "w")

# Import utilities for resource path handling
def get_resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class App(Ctk.CTk):
    def __init__(self):
        # Initialize the main window as quickly as possible
        super().__init__()
        self.title("Tooler")
        self.geometry("800x500")
        
        # Initialize minimal variables needed for startup
        self.current_frame = None
        self.menu_frame = None
        
        # Show the homepage immediately
        self.show_homepage()
        
        # Initialize state variables
        self.running = False
        self.bbox = None
        self.custom_bbox = None  
        self.last_messages = []
        
        # Lazy-loaded module instances
        self._translator_engine = None
        self._video_converter = None
        self._auto_clicker = None
        self._speed_tester = None

    # Lazy loading methods for modules
    def _get_translator_engine(self):
        if self._translator_engine is None:
            from core.translator import TranslatorEngine
            self._translator_engine = TranslatorEngine()
        return self._translator_engine
        
    def _get_video_converter(self):
        if self._video_converter is None:
            from core.video_converter import VideoConverter
            self._video_converter = VideoConverter()
        return self._video_converter
        
    def _get_auto_clicker(self):
        if self._auto_clicker is None:
            from core.auto_clicker import AutoClicker
            self._auto_clicker = AutoClicker()
        return self._auto_clicker
        
    def _get_speed_tester(self):
        if self._speed_tester is None:
            from core.speed_tester import SpeedTester
            self._speed_tester = SpeedTester()
        return self._speed_tester

    def show_homepage(self):
        if self.current_frame or self.menu_frame:
            if self.current_frame:
                self.current_frame.destroy()
            if self.menu_frame:
                self.menu_frame.destroy()
            
        self.destroy_main_interface()

        self.current_frame = Ctk.CTkFrame(self, corner_radius=0, border_color="black", border_width=0.7)
        self.current_frame.pack(side="right", fill="both", expand=True)

        self.menu_frame = Ctk.CTkFrame(self, fg_color="#21266B", corner_radius=0, border_color="black", border_width=0.7)
        self.menu_frame.pack(side="left", fill="both")

        label = Ctk.CTkLabel(self.current_frame, text="Welcome To Tooler!", font=("Arial", 25, "bold"))
        label.pack(pady=20)

        whats_new = Ctk.CTkLabel(self.current_frame, text="Whats new? ", font=("Arial", 20))
        whats_new.pack(side="top", padx=(0,400), pady=(30,0))

        whats_new_text = Ctk.CTkLabel(self.current_frame, text="• Changed from Tkinter to CustomTkinter\n\n""• Updated UI\n\n""• Added ICO picture\n\n""• Cleaned up code\n\n""• MORE NEW TOOLS!\n\n""• New logo\n\n""• New brand name\n\n""• Optimized for faster startup", justify="left" ,font=("Arial", 15))
        whats_new_text.pack(side="left", padx=(60,0), pady=(0,130))

        image_path = get_resource_path("wave.png")

        water = Ctk.CTkImage(
            light_image=Image.open(image_path),
            dark_image=Image.open(image_path),
            size=(300, 200)
        )

        water_wave = Ctk.CTkLabel(self.current_frame, text="", image=water)
        water_wave.pack(side="right", pady=(0, 150))

        button = Ctk.CTkButton(self.menu_frame, text="Youtube Downloader", command=self.show_youtube)
        button.pack(pady=20, padx=10)

        button2 = Ctk.CTkButton(self.menu_frame, text="Image Converter", command=self.show_imgconverter)
        button2.pack()

        button3 = Ctk.CTkButton(self.menu_frame, text="Speed Test", command=self.show_speedtest)
        button3.pack(pady=20)

        button4 = Ctk.CTkButton(self.menu_frame, text="Video Converter", command=self.show_video_converter)
        button4.pack()

        button5 = Ctk.CTkButton(self.menu_frame, text="MP4 To GIF", command=self.show_mp4togif)
        button5.pack(pady=20)

        button6 = Ctk.CTkButton(self.menu_frame, text="Chat Translator", command=self.show_translate_page)
        button6.pack()

        button7 = Ctk.CTkButton(self.menu_frame, text="Auto Clicker", command=self.show_autoclicker)
        button7.pack(pady=20)

        back_button_youtube = Ctk.CTkButton(self.menu_frame, text="Back to Homepage", command=self.show_homepage, font=("Arial", 12))
        back_button_youtube.pack(side="bottom", pady=(0,20))

    def show_youtube(self):
        if self.current_frame:
            self.current_frame.destroy()

        self.destroy_main_interface()

        self.current_frame = Ctk.CTkFrame(self)
        self.current_frame.pack(fill="both", expand=True)
        
        def handle_youtube_download():
            youtube_url = url_entry.get()
            selected_file_type = file_type.get()
            # Lazy import the youtube downloader module
            from core.youtube_downloader import start_download
            start_download(youtube_url, selected_file_type)

        youtube_page_label = Ctk.CTkLabel(self.current_frame, text="YouTube Video Downloader", font=("Arial",20, "bold"))
        youtube_page_label.pack(pady=20)

        url_label = Ctk.CTkLabel(self.current_frame, text="Enter YouTube URL:", font=("Arial", 12))
        url_label.pack(pady=5)

        url_entry = Ctk.CTkEntry(self.current_frame, width=500, font=("Arial", 10))
        url_entry.pack(pady=2, ipady=6)

        file_type_label = Ctk.CTkLabel(self.current_frame, text="Select File Type:", font=("Arial", 12))
        file_type_label.pack(pady=(20, 0))

        file_type = Ctk.StringVar(value="mp4")
        mp4_radio = Ctk.CTkRadioButton(self.current_frame, text="MP4", variable=file_type, value="mp4", font=("Arial", 10))
        mp4_radio.pack(pady=(0, 10))

        mp3_radio = Ctk.CTkRadioButton(self.current_frame, text="MP3", variable=file_type, value="mp3", font=("Arial", 10))
        mp3_radio.pack()

        download_button = Ctk.CTkButton(self.current_frame, text="Download", font=("Arial", 12), command=handle_youtube_download)
        download_button.pack(pady=20)
    
    def show_imgconverter(self):
        if self.current_frame:
            self.current_frame.destroy()

        self.destroy_main_interface()

        self.current_frame = Ctk.CTkFrame(self)
        self.current_frame.pack(fill="both", expand=True)

        picchanger_label = Ctk.CTkLabel(self.current_frame, text="Picture File Type Changer", font=("Arial", 20, "bold"))
        picchanger_label.pack(pady=20)

        self.img_selected_file = Ctk.StringVar()
        self.original_file = Ctk.StringVar()
        self.selected_format = Ctk.StringVar(value="jpeg")

        file_label = Ctk.CTkLabel(self.current_frame, text="Select Image File:", font=("Arial", 12))
        file_label.pack(pady=5)

        file_button = Ctk.CTkButton(self.current_frame, text="Browse", command=self.select_file, font=("Arial", 10))
        file_button.pack(pady=5)

        file_path_label = Ctk.CTkLabel(self.current_frame, textvariable=self.img_selected_file, wraplength=300, font=("Arial", 10))
        file_path_label.pack(pady=5)

        output_format_label = Ctk.CTkLabel(self.current_frame, text="Select Output Format:", font=("Arial", 12))
        output_format_label.pack(pady=10)

        output_formats = ["jpeg", "png", "webp"]
        format_menu = Ctk.CTkOptionMenu(self.current_frame, variable=self.selected_format, values=output_formats)
        format_menu.pack(pady=5)

        convert_button = Ctk.CTkButton(self.current_frame, text="Convert", command=self.start_conversion, font=("Arial", 12, "bold"))
        convert_button.pack(pady=20)

        self.delete_button = Ctk.CTkButton(self.current_frame, text="Delete Original Image", command=self.delete_original_image, font=("Arial", 12),
                                           state="disabled")
        self.delete_button.pack(pady=10)

        copyright_label = Ctk.CTkLabel(self.current_frame, text=" 2024 Dem Som Vet", font=("Arial", 10))
        copyright_label.pack(side="bottom", pady=10)

    def select_file(self):
        file_path = Ctk.filedialog.askopenfilename(
            title="Select an Image File",
            filetypes=[("Image Files", "*.jpeg *.png *.webp"), ("All Files", "*.*")]
        )
        if file_path:
            self.img_selected_file.set(file_path)
            self.delete_button.configure(state="disabled")

    def start_conversion(self):
        input_file = self.img_selected_file.get()
        if not input_file:
            CTkMessagebox(title="Error", message="Please select an image file first", icon="cancel")
            return

        output_format = self.selected_format.get()
        
        # Lazy import the image converter module
        from core.image_converter import convert_image
        
        success, result = convert_image(input_file, output_format)
        
        if success:
            self.original_file.set(input_file)
            CTkMessagebox(title="Success", message=f"Image converted successfully!\nSaved to: {result}", icon="check")
            self.delete_button.configure(state="normal")
        else:
            CTkMessagebox(title="Error", message=f"Conversion failed: {result}", icon="cancel")

    def delete_original_image(self):
        original_file = self.original_file.get()
        if original_file:
            # Lazy import the image converter module
            from core.image_converter import delete_file
            
            success, message = delete_file(original_file)
            
            if success:
                CTkMessagebox(title="Success", message="Original image deleted successfully", icon="check")
                self.delete_button.configure(state="disabled")
            else:
                CTkMessagebox(title="Error", message=f"Failed to delete original image: {message}", icon="cancel")

    def show_speedtest(self):
        if self.current_frame:
            self.current_frame.destroy()
            
        self.destroy_main_interface()

        self.current_frame = Ctk.CTkFrame(self)
        self.current_frame.pack(fill="both", expand=True)

        overskrift = Ctk.CTkLabel(self.current_frame, text="Internett Speed Test", font=("Arial", 20, "bold"))
        overskrift.pack(pady=(20))

        download_progressbar = Ctk.CTkProgressBar(self.current_frame)
        download_progressbar.pack(pady=(10,10))
        download_progressbar.set(0)

        def start():
            def speedtest_function():
                # Lazy import the speed tester module
                from core.speed_tester import SpeedTester
                speed_tester = SpeedTester()
                speed_tester.start_test(download_progressbar, info_label, server_label, results)

            thread = threading.Thread(target=speedtest_function)
            thread.start()

        start_test = Ctk.CTkButton(self.current_frame, text="start the test", command=start)
        start_test.pack(pady=10)

        info_label = Ctk.CTkLabel(self.current_frame, text="")
        info_label.pack(pady=5)

        server_label = Ctk.CTkLabel(self.current_frame, text="")
        server_label.pack(pady=(10,2))

        results = Ctk.CTkLabel(self.current_frame, text="")
        results.pack()

        def loading_bar(i, request_count, end=False, start=False):
            if end == True:
                progress = (i + 1)/request_count
                download_progressbar.set(progress)
    
    def show_video_converter(self):
        if self.current_frame:
                self.current_frame.destroy()

        self.destroy_main_interface()
            
        self.current_frame = Ctk.CTkFrame(self)
        self.current_frame.pack(fill="both", expand=True)
            
        file_var = Ctk.StringVar()
        format_var = Ctk.StringVar(value="mp4")
            
        video_label = Ctk.CTkLabel(self.current_frame, text="Video Converter", font=("Arial", 20 ,"bold"))
        video_label.pack(pady=(20))
            
        select_file_button = Ctk.CTkButton(self.current_frame, text="Select Media File", command=lambda: file_var.set(self._get_video_converter().select_file()))
        select_file_button.pack(pady=20)
            
        format_menu = Ctk.CTkComboBox(self.current_frame, values=["mp4", "avi", "mkv", "mov", "mp3", "wav"], variable=format_var)
        format_menu.pack(pady=10)
            
        convert_button = Ctk.CTkButton(self.current_frame, text="Convert", command=lambda: self._get_video_converter().convert_media(file_var.get(), format_var.get()))
        convert_button.pack(pady=10)
            
        delete_button = Ctk.CTkButton(self.current_frame, text="Delete Original File", command=lambda: self._get_video_converter().delete_original(file_var.get()))
        delete_button.pack(pady=10)
            
        video_warning_label = Ctk.CTkLabel(self.current_frame, text="Warning: Big video files with high quality and frame rate can cause high pc usage!", font=("Arial",12), text_color="Red")
        video_warning_label.pack(pady=10)

    
    def show_mp4togif(self):
        if self.current_frame:
            self.current_frame.destroy()

        self.destroy_main_interface()

        self.current_frame = Ctk.CTkFrame(self)
        self.current_frame.pack(fill="both", expand=True)

        ffmpeg_path = os.path.join(os.path.dirname(__file__), 'ffmpeg.exe')
        self.selected_file = None

        def check_ffmpeg():
            if not os.path.exists(ffmpeg_path):
                CTkMessagebox (title="Error", text="FFmpeg not found at {ffmpeg_path}. Please ensure 'ffmpeg.exe' is in the script directory.", icon="warning")
                return False
            return True

        def select_file():
            root = Ctk.CTk()
            root.withdraw()
            root.update()
            file_path = Ctk.filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4")])
            root.destroy()
            if file_path:
                self.selected_file = file_path
                selected_label.configure(text=f"Selected file: {self.selected_file}")
            else:
                selected_label.configure(text=f"No Selected file.")

        def mp4_to_gif(fps: int = 10, scale: int = -1):
            def gif_start():

                if not check_ffmpeg():
                    return

                if not self.selected_file:
                    CTkMessagebox(message="An error occurred, No file is choosen!", title="ERROR 903", icon="warning")

                if not os.path.exists(self.selected_file):
                    raise FileNotFoundError (CTkMessagebox(text=f"Input file {self.selected_file} does not exist."))
                
                self.selected_file = self.selected_file
                
                output_file = os.path.splitext(self.selected_file)[0] + ".gif"
                
                try:
                    # Lazy import the video converter module
                    from core.video_converter import VideoConverter
                    
                    # Create an instance and convert to GIF
                    converter = VideoConverter()
                    success, result = converter.convert_to_gif(
                        self.selected_file, 
                        output_file, 
                        fps=fps
                    )
                    
                    if success:
                        CTkMessagebox(title="Success", message=f"Successfully converted {self.selected_file} to {output_file}")
                    else:
                        CTkMessagebox(title="Error", message=f"Error converting file: {result}", icon="warning")
                except Exception as e:
                    CTkMessagebox(title="Error", message=f"Error converting file: {e}", icon="warning")
        
            thread_gif = threading.Thread(target=gif_start)
            thread_gif.start()


        def start_conv_gif():
            mp4_to_gif(fps=15, scale=500)

        def delete_original_mp4():
            if self.selected_file:
                try:
                    os.remove(self.selected_file)
                    return True, CTkMessagebox (message=f"The original image file {self.selected_file} has been deleted.", title="Success")
                except Exception as e:
                    return False, CTkMessagebox(message=f"An error occurred while deleting the file: {e}", title="ERROR 554", icon="warning")
            elif not self.selected_file:
                CTkMessagebox(message="An error occurred, No file is choosen!", title="ERROR 903", icon="warning")


        mp4_to_gif_label = Ctk.CTkLabel(self.current_frame, text="MP4 To GIF", font=("Arial", 20, "bold"))
        mp4_to_gif_label.pack(pady=20)

        select_button = Ctk.CTkButton(self.current_frame, text="Select file", command=select_file, font=("Arial", 12))
        select_button.pack(pady=10)

        selected_label = Ctk.CTkLabel(self.current_frame, text="")
        selected_label.pack(pady=5)

        conver_gif_button = Ctk.CTkButton(self.current_frame, text="Convert", command=start_conv_gif, font=("Arial", 12))
        conver_gif_button.pack(pady=15)

        delete_original_button = Ctk.CTkButton(self.current_frame, text="Delete original file", command=delete_original_mp4)
        delete_original_button.pack(pady=15)

    def show_translate_page(self):
        if self.current_frame:
            self.current_frame.destroy()
            
        self.destroy_main_interface()
        
        # Initialize variables for translator
        self.custom_bbox = None
        self.running = False
        self.last_messages = []

        self.current_frame = Ctk.CTkFrame(self)
        self.current_frame.pack(fill="both", expand=True)

        translate_page_label = Ctk.CTkLabel(self.current_frame, text="Chat Translator", font=("Arial", 20, "bold"))
        translate_page_label.pack(pady=(20))

        self.window_var = Ctk.StringVar()
        self.window_dropdown = Ctk.CTkComboBox(self.current_frame, variable=self.window_var, values=self.get_window_list())
        self.window_dropdown.pack(pady=5)

        self.refresh_button = Ctk.CTkButton(self.current_frame, text="Refresh list", command=self.update_window_list)
        self.refresh_button.pack(pady=5)

        self.select_area_button = Ctk.CTkButton(self.current_frame, text="Select area", command=self.select_capture_area)
        self.select_area_button.pack(pady=5)

        self.output_text = Ctk.CTkTextbox(self.current_frame, width=500, height=200)
        self.output_text.pack(pady=5)

        button_frame = Ctk.CTkFrame(self.current_frame)
        button_frame.pack(pady=5)

        self.start_button = Ctk.CTkButton(button_frame, text="Start", command=self.start_translation, state="disabled")
        self.start_button.pack(side="left", padx=5)

        self.stop_button = Ctk.CTkButton(button_frame, text="Stop", command=self.stop_translation, state="disabled")
        self.stop_button.pack(side="left", padx=5)

        back_button = Ctk.CTkButton(self.current_frame, text="Back to Home", command=self.show_homepage)
        back_button.pack(pady=5)

        # Add instructions
        self.output_text.insert("end", " Instructions:\n")
        self.output_text.insert("end", " 1. Select a window from the dropdown\n")
        self.output_text.insert("end", " 2. Click 'Select area' and draw a rectangle around the chat area\n")
        self.output_text.insert("end", " 3. Click 'Start' to begin translation\n")
        self.output_text.insert("end", " 4. Click 'Stop' when done\n\n")

    def get_window_list(self):
        try:
            # Lazy import pygetwindow
            import pygetwindow as gw
            windows = gw.getAllTitles()
            return [w for w in windows if w]
        except ImportError:
            CTkMessagebox(title="Error", message="Could not import pygetwindow module. Make sure it's installed.", icon="warning")
            return []

    def update_window_list(self):
        self.window_dropdown.configure(values=self.get_window_list())
        self.window_var.set("")

    def get_window_bbox(self, window_title):
        try:
            # Lazy import pygetwindow
            import pygetwindow as gw
            win = gw.getWindowsWithTitle(window_title)[0]
            return (win.left, win.top, win.right, win.bottom)
        except ImportError:
            self.output_text.insert("end", " Error: pygetwindow module not found.\n")
            return None
        except IndexError:
            self.output_text.insert("end", " Window not found! Try again.\n")
            return None

    def select_capture_area(self):
        window_title = self.window_var.get()
        bbox = self.get_window_bbox(window_title)

        if not bbox:
            return

        try:
            # Lazy import required modules
            import mss
            import numpy as np
            import cv2
            
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
                self.output_text.insert("end", f" Area selected: {self.custom_bbox}\n")
                self.start_button.configure(state="normal")
        except ImportError as e:
            self.output_text.insert("end", f" Error: Missing required module - {str(e)}.\n")
        except Exception as e:
            self.output_text.insert("end", f" Error: {str(e)}.\n")

    def capture_text_from_window(self):
        try:
            # Lazy import required modules
            import mss
            import numpy as np
            import cv2
            import pytesseract
            from deep_translator import GoogleTranslator
            
            # Set tesseract path
            pytesseract.pytesseract.tesseract_cmd = r"Tesseract-OCR\tesseract.exe"
            
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
                                    self.output_text.insert("end", f" {message} → {translated_text}\n")
                                    self.output_text.see("end")
                                except Exception as e:
                                    self.output_text.insert("end", f" Error translating: {str(e)}\n")
                                    self.output_text.see("end")

                        time.sleep(1)
        except ImportError as e:
            self.output_text.insert("end", f" Error: Missing required module - {str(e)}.\n")
            self.running = False
        except Exception as e:
            self.output_text.insert("end", f" Error: {str(e)}.\n")
            self.running = False

    def start_translation(self):
        if not self.custom_bbox:
            self.output_text.insert("end", " Select an area first!\n")
            return

        self.running = True
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")

        threading.Thread(target=self.capture_text_from_window, daemon=True).start()

    def stop_translation(self):
        self.running = False
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.output_text.insert("end", " Translation stopped.\n")

    def destroy_main_interface(self):
        # Clean up main frame
        if hasattr(self, 'main_frame') and self.main_frame:
            self.main_frame.destroy()
            self.main_frame = None
            
        # Clean up buttons frame
        if hasattr(self, 'buttons_frame') and self.buttons_frame:
            self.buttons_frame.destroy()
            self.buttons_frame = None
            
        # Clean up info frame
        if hasattr(self, 'info_frame') and self.info_frame:
            self.info_frame.destroy()
            self.info_frame = None
            
        # Remove any keyboard hotkeys
        if hasattr(self, 'hotkey') and self.hotkey:
            try:
                import keyboard
                keyboard.remove_hotkey(self.hotkey.get())
            except:
                pass
                
        if hasattr(self, 'killswitch_hotkey') and self.killswitch_hotkey:
            try:
                import keyboard
                keyboard.remove_hotkey('Ctrl+Shift+K')
            except:
                pass
                
    def show_autoclicker(self):
        # First, destroy any existing frames
        if self.current_frame:
            self.current_frame.destroy()
            
        # Make sure to clean up any existing UI components
        self.destroy_main_interface()
        
        # Reset the stop thread flag
        self.stop_main_thread = False

        # Initialize variables for auto clicker
        self.interval_ms = Ctk.StringVar(value='100')
        self.interval_s = Ctk.StringVar(value='0')
        self.interval_min = Ctk.StringVar(value='0')
        self.interval_hr = Ctk.StringVar(value='0')

        self.interval_ms.trace('w', lambda x, y, z: self.validate(self.interval_ms))
        self.interval_s.trace('w', lambda x, y, z: self.validate(self.interval_s))
        self.interval_min.trace('w', lambda x, y, z: self.validate(self.interval_min))
        self.interval_hr.trace('w', lambda x, y, z: self.validate(self.interval_hr))

        self.mouse_button = Ctk.StringVar(value='Left')
        self.hotkey = Ctk.StringVar(value='f8')

        self.super_mode = Ctk.BooleanVar(value=False)

        self.random_time_offset_enabled = Ctk.BooleanVar(value=False)
        self.random_time_offset = Ctk.StringVar(value='0')

        self.random_mouse_offset_enabled = Ctk.BooleanVar(value=False)
        self.random_mouse_offset_x = Ctk.StringVar(value='0')
        self.random_mouse_offset_y = Ctk.StringVar(value='0')

        self.click_type = Ctk.StringVar(value='Single')
        self.hold_duration = Ctk.StringVar(value='0')

        self.repeat_option = Ctk.StringVar(value='Toggle')
        self.repeat_value = Ctk.StringVar(value='0')

        self.killswitch_hotkey = Ctk.StringVar(value='Ctrl+Shift+K')

        self.random_time_offset.trace('w', lambda x, y, z: self.validate(self.random_time_offset))
        self.random_mouse_offset_x.trace('w', lambda x, y, z: self.validate(self.random_mouse_offset_x))
        self.random_mouse_offset_y.trace('w', lambda x, y, z: self.validate(self.random_mouse_offset_y))
        self.hold_duration.trace('w', lambda x, y, z: self.validate(self.hold_duration))
        self.repeat_value.trace('w', lambda x, y, z: self.validate(self.repeat_value))

        # Create UI components
        self.main_frame = MainFrame(self)
        self.buttons_frame = ButtonsFrame(self)
        self.info_frame = InfoFrame(self)

        # Add keyboard hotkey
        import keyboard
        keyboard.add_hotkey((self.hotkey.get()), self.start_clicking)
        keyboard.add_hotkey('Ctrl+Shift+K', self.destroy)

    def get_interval_sum(self) -> float | int:
        return (self.normalize(self.interval_ms) * 0.001
                + self.normalize(self.interval_s)
                + self.normalize(self.interval_min) * 60
                + self.normalize(self.interval_hr) * 3600)

    def start_clicking(self) -> None:
        self.stop_main_thread = False

        import keyboard
        keyboard.remove_hotkey(self.hotkey.get())
        self.buttons_frame.start_button.configure(state='disabled')
        self.buttons_frame.stop_button.configure(state='normal')
        self.buttons_frame.change_hotkey_button.configure(state='disabled')

        import keyboard
        keyboard.add_hotkey(self.hotkey.get(), self.stop_clicking)

        # Use the modular auto clicker with lazy loading
        from core.auto_clicker import AutoClicker
        
        # Create auto clicker instance
        self.auto_clicker = AutoClicker()
        
        # Configure auto clicker settings
        self.auto_clicker.mouse_button = self.mouse_button.get().lower()
        self.auto_clicker.interval_ms = int(self.interval_ms.get()) if self.interval_ms.get() else 0
        self.auto_clicker.interval_s = int(self.interval_s.get()) if self.interval_s.get() else 0
        self.auto_clicker.interval_min = int(self.interval_min.get()) if self.interval_min.get() else 0
        self.auto_clicker.interval_hr = int(self.interval_hr.get()) if self.interval_hr.get() else 0
        
        # Advanced settings
        self.auto_clicker.random_time_offset_enabled = self.random_time_offset_enabled.get()
        self.auto_clicker.random_time_offset = int(self.random_time_offset.get()) if self.random_time_offset.get() else 0
        self.auto_clicker.random_mouse_offset_enabled = self.random_mouse_offset_enabled.get()
        self.auto_clicker.random_mouse_offset_x = int(self.random_mouse_offset_x.get()) if self.random_mouse_offset_x.get() else 0
        self.auto_clicker.random_mouse_offset_y = int(self.random_mouse_offset_y.get()) if self.random_mouse_offset_y.get() else 0
        self.auto_clicker.click_type = self.click_type.get()
        self.auto_clicker.hold_duration = int(self.hold_duration.get()) if self.hold_duration.get() else 0
        self.auto_clicker.repeat_option = self.repeat_option.get()
        self.auto_clicker.repeat_value = int(self.repeat_value.get()) if self.repeat_value.get() else 0
        self.auto_clicker.super_mode = self.super_mode.get()
        
        # Set UI callbacks
        self.auto_clicker.set_ui_callbacks(
            on_click_count_changed=lambda count: self.info_frame.click_counter.configure(text=f"Clicks: {count}"),
            on_status_changed=lambda running: self.update_clicking_status(running)
        )
        
        # Start clicking
        self.auto_clicker.start_clicking()

    def stop_clicking(self) -> None:
        self.stop_main_thread = True

        import keyboard
        keyboard.remove_hotkey(self.hotkey.get())

        self.buttons_frame.start_button.configure(state='normal')
        self.buttons_frame.stop_button.configure(state='disabled')
        self.buttons_frame.change_hotkey_button.configure(state='normal')

        import keyboard
        keyboard.add_hotkey(self.hotkey.get(), self.start_clicking)
        
        # Stop the auto clicker if it exists
        if hasattr(self, 'auto_clicker') and self.auto_clicker:
            self.auto_clicker.stop_clicking()
    
    def update_clicking_status(self, running):
        """Update UI based on clicking status"""
        if running:
            self.buttons_frame.start_button.configure(state='disabled')
            self.buttons_frame.stop_button.configure(state='normal')
            self.buttons_frame.change_hotkey_button.configure(state='disabled')
        else:
            self.buttons_frame.start_button.configure(state='normal')
            self.buttons_frame.stop_button.configure(state='disabled')
            self.buttons_frame.change_hotkey_button.configure(state='normal')

    def change_hotkey(self) -> None:
        import keyboard
        keyboard.remove_hotkey(self.hotkey.get())
        hotkey_created = False
        new_hotkey = []
        used_modifiers = []
        self.buttons_frame.change_hotkey_button.configure(text='Press any key...')

        def callback(key) -> None:
            nonlocal hotkey_created
            if key.name not in keyboard.all_modifiers:
                new_hotkey.append(key.name)
                hotkey_created = True
                return
            if key.name not in used_modifiers:
                    new_hotkey.append(key.name)
                    used_modifiers.append(key.name)

        import keyboard
        keyboard.hook(callback)

        def wait_for_callback() -> None:
            while not hotkey_created:
                sleep(0.01)
            import keyboard
            keyboard.unhook(callback)
            hotkey = '+'.join(new_hotkey)

            self.hotkey.set(hotkey)
            import keyboard
            keyboard.add_hotkey(self.hotkey.get(), self.start_clicking)

            self.buttons_frame.change_hotkey_button.configure(text='Change Hotkey')

            self.buttons_frame.start_button.configure(text=f"Start: {self.hotkey.get().replace('+', '-').title()}")
            self.buttons_frame.stop_button.configure(text=f"Stop: {self.hotkey.get().replace('+', '-').title()}")

            exit()

        threading.Thread(target=wait_for_callback, daemon=True).start()

    @staticmethod
    def normalize(variable: Ctk.StringVar) -> int:
        if variable.get() == '':
            return 0
        return int(variable.get())

    @staticmethod
    def validate(variable: Ctk.StringVar) -> None:
        variable_text = variable.get()
        for letter in variable_text:
            if not letter.isdigit():
                variable_text = variable_text.replace(letter, '')
            variable.set(variable_text)


class MainFrame(Ctk.CTkFrame):
    def __init__(self, master: App):
        super().__init__(master)
        self.pack(expand=True, fill='both', padx=5, pady=5)

        self.info_frame = MainFrameInfoFrame(self, master)
        self.interval_frame = IntervalFrame(self, master)


class MainFrameInfoFrame(Ctk.CTkFrame):
    def __init__(self, master, root: App):
        super().__init__(master, fg_color='transparent')
        self.pack(expand=True, fill='x')

        self.description = Ctk.CTkLabel(self, text='Click Interval:')
        self.description.pack(side='left', padx=10)

        self.advanced_options = Ctk.CTkButton(
            self,
            text='>>',
            width=40,
            command=lambda: AdvancedOptions(root),
        )
        self.advanced_options.pack(side='right', padx=5, pady=10)

        self.dropdown = Ctk.CTkOptionMenu(
            self,
            values=['Left', 'Right', 'Middle'],
            variable=root.mouse_button,
            )
            
        self.dropdown.pack(side='right', padx=5, pady=10)

        self.dropdown_label = Ctk.CTkLabel(self, text='Mouse Button:')
        self.dropdown_label.pack(side='right', padx=5, pady=10)


class IntervalFrame(Ctk.CTkFrame):
    def __init__(self, master, root: App):
        super().__init__(master, fg_color='transparent')
        self.pack(expand=True, fill='x', padx=5)

        self.label_ms = IntervalFrameLabel(self, text='Ms:')
        self.entry_ms = IntervalFrameEntry(self, root.interval_ms, width=60)

        self.label_sec = IntervalFrameLabel(self, text='Sec:')
        self.entry_sec = IntervalFrameEntry(self, root.interval_s, width=60)

        self.label_min = IntervalFrameLabel(self, text='Min:')
        self.entry_min = IntervalFrameEntry(self, root.interval_min, width=60)

        self.label_hr = IntervalFrameLabel(self, text='Hr:')
        self.entry_hr = IntervalFrameEntry(self, root.interval_hr, width=60)


class IntervalFrameEntry(Ctk.CTkEntry):
    def __init__(self, master, interval_variable, *, width):
        super().__init__(master, textvariable=interval_variable, width=width)
        self.pack(side='left', expand=True, fill='x', padx=5, pady=5)


class IntervalFrameLabel(Ctk.CTkLabel):
    def __init__(self, master, *, text):
        super().__init__(master, text=text, )
        self.pack(side='left', expand=True, fill='x', padx=5, pady=5)


class ButtonsFrame(Ctk.CTkFrame):
    def __init__(self, master: App):
        super().__init__(master, fg_color='transparent')
        self.pack(expand=True, fill='y', padx=5, pady=5)

        self.start_button = Ctk.CTkButton(
            self,
            text=f"Start: {master.hotkey.get().replace('+', '-').title()}",
            command=lambda: master.start_clicking(),
        )

        self.start_button.pack(side='left', expand=True, padx=5)

        self.stop_button = Ctk.CTkButton(
            self,
            text=f"Stop: {master.hotkey.get().replace('+', '-').title()}",
            state='disabled',
            command=lambda: master.stop_clicking(),
        )
        self.stop_button.pack(side='left', expand=True, padx=5)

        self.change_hotkey_button = Ctk.CTkButton(
            self,
            text='Change Hotkey',
            command=lambda: master.change_hotkey(),
        )
        self.change_hotkey_button.pack(side='left', expand=True, padx=5)

        import keyboard
        keyboard.add_hotkey((master.hotkey.get()), master.start_clicking)


class InfoFrame(Ctk.CTkFrame):
    def __init__(self, master: App):
        super().__init__(master, fg_color='transparent')
        self.pack(fill='x', padx=10, pady=5)
        self.killswitch_label = Ctk.CTkLabel(self, text=f'Killswitch: {master.killswitch_hotkey.get().replace("+", "-").title()}')
        self.killswitch_label.pack(side='left')

        self.super_mode_switch = Ctk.CTkSwitch(self, text='Super Mode', variable=master.super_mode)
        self.super_mode_switch.pack(side='right', padx=5)


class AdvancedOptions(Ctk.CTkToplevel):
    def __init__(self, root: App):
        super().__init__()
        self.title("Advanced Options")
        self.grab_set()
        self.geometry(
            f"500x300"
            f"+{int(self.winfo_screenwidth() / 2 - 500 / 2)}"
            f"+{int(self.winfo_screenheight() / 2 - 300 / 2)}"
        )
        self.resizable(False, False)

        self.rowconfigure((0, 1, 2), weight=3, uniform='a')
        self.columnconfigure((0, 1), weight=1, uniform='a')

        self.root = root

        self.time_offset = TimeOffset(self)
        self.mouse_offset = MouseOffset(self)
        self.click_type = ClickType(self)
        self.repeat_options = RepeatOptions(self)
        self.killswitch = KillSwitch(self)

    def change_killswitch_hotkey(self, buttons_frame):
        import keyboard
        keyboard.remove_hotkey(self.root.killswitch_hotkey.get())
        hotkey_created = False
        new_hotkey = []
        used_modifiers = []
        buttons_frame.change_killswitch_hotkey.configure(text='Press any key...')

        def callback(key):
            nonlocal hotkey_created
            if key.name not in keyboard.all_modifiers:
                new_hotkey.append(key.name)
                hotkey_created = True
                return
            if key.name not in used_modifiers:
                new_hotkey.append(key.name)
                used_modifiers.append(key.name)

        import keyboard
        keyboard.hook(callback)

        def wait_for_callback():
            while not hotkey_created:
                sleep(0.01)
            import keyboard
            keyboard.unhook(callback)
            hotkey = '+'.join(new_hotkey)

            self.root.killswitch_hotkey.set(hotkey)
            import keyboard
            keyboard.add_hotkey(self.root.killswitch_hotkey.get(), self.root.destroy)

            buttons_frame.change_killswitch_hotkey.configure(text='Change KillSwitch Hotkey')
            buttons_frame.killswitch_hotkey.configure(
                text=f"{self.root.killswitch_hotkey.get().replace('+', '-').title()}"
            )
            self.root.info_frame.killswitch_label.configure(text=f'Killswitch: {hotkey.replace("+", "-").title()}')
            exit()

        threading.Thread(target=wait_for_callback, daemon=True).start()

class TimeOffset(Ctk.CTkFrame):
    def __init__(self, master: AdvancedOptions):
        super().__init__(master)
        self.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        self.switch = Ctk.CTkSwitch(
            self,
            text='Random Time Offset',
            variable=master.root.random_time_offset_enabled,
        )
        self.switch.place(relx=0.05, rely=0.1)

        self.label = Ctk.CTkLabel(self, text='Milliseconds')
        self.label.place(relx=0.05, rely=0.55)

        self.entry = Ctk.CTkEntry(self, width=60, textvariable=master.root.random_time_offset)
        self.entry.place(relx=0.4, rely=0.55)


class MouseOffset(Ctk.CTkFrame):
    def __init__(self, master: AdvancedOptions):
        super().__init__(master)
        self.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

        self.switch = Ctk.CTkSwitch(
            self,
            text='Random Mouse Offset',
            variable=master.root.random_mouse_offset_enabled,
        )
        self.switch.place(relx=0.05, rely=0.1)

        self.x = Ctk.CTkLabel(self, text='X:')
        self.x.place(relx=0.05, rely=0.55)

        self.x_entry = Ctk.CTkEntry(self, width=60, textvariable=master.root.random_mouse_offset_x)
        self.x_entry.place(relx=0.15, rely=0.55)

        self.y = Ctk.CTkLabel(self, text='Y:')
        self.y.place(relx=0.45, rely=0.55)

        self.y_entry = Ctk.CTkEntry(self, width=60, textvariable=master.root.random_mouse_offset_y)
        self.y_entry.place(relx=0.55, rely=0.55)


class ClickType(Ctk.CTkFrame):
    def __init__(self, master: AdvancedOptions):
        super().__init__(master)
        self.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        self.description = Ctk.CTkLabel(self, text='Click Type:')
        self.description.place(relx=0.05, rely=0.1)

        self.option_menu = Ctk.CTkOptionMenu(
            self,
            values=['Single', 'Double'],
            width=135,
            variable=master.root.click_type,
        )

        self.option_menu.place(relx=0.37, rely=0.1)

        self.hold_label = Ctk.CTkLabel(
            self, text='Hold duration (ms):'
        )
        self.hold_label.place(relx=0.05, rely=0.55)

        self.hold_entry = Ctk.CTkEntry(
            self,
            width=60,
            textvariable=master.root.hold_duration
        )
        self.hold_entry.place(relx=0.6, rely=0.55)


class RepeatOptions(Ctk.CTkFrame):
    def __init__(self, master: AdvancedOptions):
        super().__init__(master)
        self.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')

        self.description = Ctk.CTkLabel(self, text='Repeat Options:')
        self.description.place(relx=0.05, rely=0.1)

        self.toggle = Ctk.CTkRadioButton(
            self,
            text='Toggle',
            variable=master.root.repeat_option,
            value='Toggle',
        )
        self.toggle.place(relx=0.05, rely=0.55)

        self.repeat = Ctk.CTkRadioButton(
            self,
            text='Repeat',
            variable=master.root.repeat_option,
            value='Repeat',
        )
        self.repeat.place(relx=0.4, rely=0.55)

        self.entry = Ctk.CTkEntry(self, width=50, textvariable=master.root.repeat_value)
        self.entry.place(relx=0.75, rely=0.53)


class KillSwitch(Ctk.CTkFrame):
    def __init__(self, master: AdvancedOptions):
        super().__init__(master)
        self.grid(row=2, column=0, padx=10, pady=10, sticky='nsew')

        self.change_killswitch_hotkey = Ctk.CTkButton(
            self,
            text='Change KillSwitch Hotkey',
            command=lambda: master.change_killswitch_hotkey(self),
        )
        self.change_killswitch_hotkey.place(relx=0.5, rely=0.15, anchor='n')

        self.killswitch_hotkey = Ctk.CTkLabel(
            self,
            text=f"{master.root.killswitch_hotkey.get().replace('+', '-').title()}"
        )
        self.killswitch_hotkey.place(relx=0.5, rely=0.6, anchor='n')


if __name__ == "__main__":
    app = App()
    app.mainloop()
