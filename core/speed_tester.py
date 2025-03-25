"""
Speed Test module - separated from GUI for better performance
"""
import threading
import speedtest
import time

class SpeedTester:
    """Handles internet speed testing with lazy loading"""
    
    def __init__(self):
        self._speedtest = None
        self.running = False
        self.results = {
            'download': 0,
            'upload': 0,
            'ping': 0
        }
    
    def _get_speedtest(self):
        """Lazy load the speedtest module"""
        if self._speedtest is None:
            self._speedtest = speedtest.Speedtest()
        return self._speedtest
    
    def loading_bar(self, current, total):
        """Update progress bar if available"""
        if hasattr(self, 'progress_bar') and self.progress_bar:
            progress = current / total
            self.progress_bar.set(progress)
    
    def start_test(self, progress_bar=None, info_label=None, server_label=None, results_label=None):
        """Run a complete speed test with UI updates"""
        if self.running:
            return False
        
        self.progress_bar = progress_bar
        self.info_label = info_label
        self.server_label = server_label
        self.results_label = results_label
        
        def test_thread():
            try:
                self.running = True
                
                # Get a fresh speedtest instance
                st = self._get_speedtest()
                
                # Update UI
                if self.info_label:
                    self.info_label.configure(text="Finding best server...")
                
                # Get the best server
                st.get_best_server()
                
                # Update server info
                if self.server_label:
                    res_dict = st.results.dict()
                    self.server_label.configure(
                        text=f"HOST:{res_dict['server']['country']} | SUPPLIER:{res_dict['server']['sponsor']} | LATENCY: {res_dict['server']['latency']:.2f}"
                    )
                
                time.sleep(1)
                
                # Test download speed
                if self.info_label:
                    self.info_label.configure(text="Testing download speed.....")
                
                download_speed = st.download(self.loading_bar) / 1_000_000  # Convert to Mbps
                self.results['download'] = download_speed
                
                # Reset progress bar
                if self.progress_bar:
                    self.progress_bar.set(0)
                
                # Test upload speed
                if self.info_label:
                    self.info_label.configure(text="Testing upload speed.....")
                
                upload_speed = st.upload(self.loading_bar) / 1_000_000  # Convert to Mbps
                self.results['upload'] = upload_speed
                
                # Update results
                if self.results_label and download_speed and upload_speed:
                    self.results_label.configure(
                        text=f"Download Speed: {download_speed:.3f} Mbps\n"
                             f"Upload Speed: {upload_speed:.3f} Mbps"
                    )
                
            except Exception as e:
                if self.info_label:
                    self.info_label.configure(text=f"Error: {str(e)}")
            finally:
                self.running = False
        
        # Start the test in a separate thread
        thread = threading.Thread(target=test_thread)
        thread.daemon = True
        thread.start()
        
        return True
    
    def get_results(self):
        """Get the latest test results"""
        return self.results
