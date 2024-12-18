import tkinter as tk
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk
import threading

class VideoPlayer:
    def __init__(self, root, video_path):
        self.root = root
        self.root.title("Custom MP4 Player")
        self.video_path = video_path

        # Create a canvas to display the video
        self.canvas = tk.Canvas(root, width=640, height=480)
        self.canvas.pack()

        # Load the video using OpenCV
        self.cap = cv2.VideoCapture(video_path)

        # Variable to control video playback
        self.running = True

        # Start video playback in a separate thread
        self.thread = threading.Thread(target=self.play_video)
        self.thread.daemon = True
        self.thread.start()

        # Add a close button
        self.close_button = tk.Button(root, text="Close", command=self.close)
        self.close_button.pack()

    def play_video(self):
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                # Convert the frame to RGB format
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (640, 480))

                # Convert the frame to a PIL image
                img = ImageTk.PhotoImage(Image.fromarray(frame))

                # Display the frame in the canvas
                self.canvas.create_image(0, 0, anchor=tk.NW, image=img)
                self.root.update()
                self.current_image = img  # Keep a reference to avoid garbage collection
            else:
                break

    def close(self):
        self.running = False
        self.cap.release()
        self.root.destroy()

def select_video():
    video_path = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4")])
    if video_path:
        root = tk.Tk()
        player = VideoPlayer(root, video_path)
        root.mainloop()

if __name__ == "__main__":
    select_video()
