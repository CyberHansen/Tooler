"""
Video Converter module - separated from GUI for better performance
"""
import os
import subprocess
import ffmpeg

class VideoConverter:
    """Handles video conversion operations with lazy loading"""
    
    def __init__(self):
        self._ffmpeg_path = None
    
    def _get_ffmpeg_path(self):
        """Lazy load the ffmpeg path"""
        if self._ffmpeg_path is None:
            self._ffmpeg_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ffmpeg.exe')
        return self._ffmpeg_path
    
    def convert_video(self, input_path, output_format, output_path=None):
        """Convert a video to the specified format"""
        try:
            if not os.path.exists(input_path):
                return False, "Input file does not exist."
            
            # If output path not specified, create one based on input
            if output_path is None:
                directory, filename = os.path.split(input_path)
                filename_without_ext = os.path.splitext(filename)[0]
                output_path = os.path.join(directory, f"{filename_without_ext}.{output_format}")
            
            # Use ffmpeg to convert the video
            ffmpeg_path = self._get_ffmpeg_path()
            
            command = [
                ffmpeg_path,
                '-i', input_path,
                '-c:v', 'libx264',
                '-preset', 'medium',
                '-c:a', 'aac',
                '-b:a', '128k',
                output_path
            ]
            
            subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            return True, output_path
        
        except Exception as e:
            return False, f"Error converting video: {str(e)}"
    
    def convert_to_gif(self, input_path, output_path=None, fps=10, scale=320):
        """Convert a video to GIF format"""
        try:
            if not os.path.exists(input_path):
                return False, "Input file does not exist."
            
            # If output path not specified, create one based on input
            if output_path is None:
                directory, filename = os.path.split(input_path)
                filename_without_ext = os.path.splitext(filename)[0]
                output_path = os.path.join(directory, f"{filename_without_ext}.gif")
            
            # Use ffmpeg to convert the video to GIF
            (
                ffmpeg
                .input(input_path)
                .filter('fps', fps=fps)
                .filter('scale', scale, -1)  # Scale width to specified value, height auto
                .output(output_path, format='gif')
                .run(capture_stdout=True, capture_stderr=True)
            )
            
            return True, output_path
        
        except Exception as e:
            return False, f"Error converting to GIF: {str(e)}"
