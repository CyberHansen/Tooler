"""
Auto Clicker module - separated from GUI for better performance
"""
import time
import random
import threading

class AutoClicker:
    """Handles auto clicking functionality with lazy loading"""
    
    def __init__(self):
        self.running = False
        self.click_thread = None
        self.click_count = 0
        
        # Default settings
        self.mouse_button = "left"
        self.interval_ms = 100
        self.interval_s = 0
        self.interval_min = 0
        self.interval_hr = 0
        
        # Advanced settings
        self.random_time_offset_enabled = False
        self.random_time_offset = 50
        self.random_mouse_offset_enabled = False
        self.random_mouse_offset_x = 5
        self.random_mouse_offset_y = 5
        self.click_type = "Single"
        self.hold_duration = 0
        self.repeat_option = "Toggle"
        self.repeat_value = 10
        self.super_mode = False
        
        # UI callbacks
        self.on_click_count_changed = None
        self.on_status_changed = None
    
    def calculate_interval(self):
        """Calculate the total interval in seconds"""
        total_ms = int(self.interval_ms) if self.interval_ms else 0
        total_ms += int(self.interval_s) * 1000 if self.interval_s else 0
        total_ms += int(self.interval_min) * 60 * 1000 if self.interval_min else 0
        total_ms += int(self.interval_hr) * 60 * 60 * 1000 if self.interval_hr else 0
        
        # Minimum interval to prevent system overload
        if total_ms < 10:
            total_ms = 10
            
        return total_ms / 1000  # Convert to seconds
    
    def get_random_offset(self):
        """Get random time offset if enabled"""
        if self.random_time_offset_enabled and self.random_time_offset > 0:
            offset = random.uniform(0, float(self.random_time_offset) / 1000)
            return offset
        return 0
    
    def get_mouse_offset(self):
        """Get random mouse position offset if enabled"""
        if self.random_mouse_offset_enabled:
            x_offset = random.randint(-int(self.random_mouse_offset_x), int(self.random_mouse_offset_x))
            y_offset = random.randint(-int(self.random_mouse_offset_y), int(self.random_mouse_offset_y))
            return x_offset, y_offset
        return 0, 0
    
    def start_clicking(self):
        """Start the auto clicker"""
        if self.running:
            return False
            
        self.running = True
        self.click_count = 0
        
        # Lazy import mouse module only when needed
        import mouse
        
        def click_thread():
            while self.running:
                try:
                    # Get interval with random offset
                    interval = self.calculate_interval()
                    if self.random_time_offset_enabled:
                        interval += self.get_random_offset()
                    
                    # Get mouse offset
                    x_offset, y_offset = self.get_mouse_offset()
                    if x_offset or y_offset:
                        mouse.move(x_offset, y_offset, absolute=False)
                    
                    # Perform click based on click type
                    if self.click_type == "Single":
                        mouse.click(self.mouse_button.lower())
                    elif self.click_type == "Double":
                        mouse.double_click(self.mouse_button.lower())
                    elif self.click_type == "Hold":
                        mouse.press(self.mouse_button.lower())
                        time.sleep(float(self.hold_duration) / 1000)
                        mouse.release(self.mouse_button.lower())
                    
                    # Increment click count
                    self.click_count += 1
                    
                    # Update UI if callback is set
                    if self.on_click_count_changed:
                        self.on_click_count_changed(self.click_count)
                    
                    # Check if we've reached the repeat limit
                    if self.repeat_option == "Count" and self.click_count >= int(self.repeat_value):
                        self.stop_clicking()
                        break
                    
                    # Reset mouse position if offset was applied
                    if x_offset or y_offset:
                        mouse.move(-x_offset, -y_offset, absolute=False)
                    
                    # Wait for next click
                    time.sleep(interval)
                    
                except Exception as e:
                    print(f"Error in auto clicker: {e}")
                    self.stop_clicking()
                    break
        
        # Start clicking in a separate thread
        self.click_thread = threading.Thread(target=click_thread)
        self.click_thread.daemon = True
        self.click_thread.start()
        
        # Update UI status if callback is set
        if self.on_status_changed:
            self.on_status_changed(True)
            
        return True
    
    def stop_clicking(self):
        """Stop the auto clicker"""
        self.running = False
        
        # Update UI status if callback is set
        if self.on_status_changed:
            self.on_status_changed(False)
            
        return True
    
    def set_ui_callbacks(self, on_click_count_changed=None, on_status_changed=None):
        """Set UI callbacks for updates"""
        self.on_click_count_changed = on_click_count_changed
        self.on_status_changed = on_status_changed
