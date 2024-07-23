import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PIL import Image
import pytesseract
import cv2
import pyperclip

running = True
def process_image(filepath):
    # Replace this with your actual image processing logic
    print(f"Processing image: {filepath}")
    time.sleep(1)

    pytesseract.pytesseract.tesseract_cmd = (
        r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    )
    # Load the image using OpenCV
    image = cv2.imread(filepath)

    # Convert to graysScale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply thresholding
    _, thresh_image = cv2.threshold(gray_image, 150, 255, cv2.THRESH_BINARY)

    # Convert back to PIL Image
    pil_image = Image.fromarray(thresh_image)

    # Extract text
    extracted_text = pytesseract.image_to_string(pil_image)

    # Copy the text to the clipboard
    pyperclip.copy(extracted_text)

    print("Text copied to clipboard successfully.")
    global running
    running = False


class ScreenshotHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.src_path.endswith(".png"):  # Filter for screenshots
            filepath = event.src_path
            try:
                process_image(filepath)
                print(f"Image processing finished for: {filepath}")
            except Exception as e:
                print(f"Error processing image: {filepath} ({e})")


def main():
    # Replace with your desired screenshot directory
    screenshot_dir = r"C:\Users\Mohammed Armaan\OneDrive\Pictures\Screenshots"

    event_handler = ScreenshotHandler()
    observer = Observer()
    observer.schedule(
        event_handler, screenshot_dir, recursive=False
    )  # Watch only top-level
    observer.start()

    try:
        print("Take screenshot")  # Adjust polling interval as needed
        while running:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()


if __name__ == "__main__":
    main()

