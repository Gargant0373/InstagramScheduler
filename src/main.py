import tkinter as tk
from tkinter import ttk
from threading import Thread
from datetime import datetime
from PIL import Image, ImageTk
import schedule
import time
from config import get_config
import instagram_scheduler as ig

def login_and_start_scheduler():
    username, password = get_config()
    client = ig.login_instagram(username, password)
    status_label.config(text="Status: Logged in")
    ig.ensure_directories_and_files()

    scheduler_thread = Thread(target=ig.scheduler, args=(client, update_status, update_next_image))
    scheduler_thread.daemon = True
    scheduler_thread.start()

def update_status(status_message):
    status_label.config(text=f"Status: {status_message}")

def resize_image(image, max_width, max_height):
    """
    Resize image while maintaining aspect ratio to fit within the specified dimensions.
    """
    img_width, img_height = image.size
    aspect_ratio = img_width / img_height

    if img_width > max_width or img_height > max_height:
        if (max_width / aspect_ratio) < max_height:
            new_width = max_width
            new_height = int(max_width / aspect_ratio)
        else:
            new_width = int(max_height * aspect_ratio)
            new_height = max_height
    else:
        new_width = img_width
        new_height = img_height

    return image.resize((new_width, new_height), Image.LANCZOS)

def update_next_image(image_path, caption):
    if image_path != "No more images":
        # Display caption in two lines
        next_post_label.config(text=f"Next post caption:\n{caption}")
        
        img = Image.open(image_path)
        img = resize_image(img, 200, 200)  # Resize while maintaining aspect ratio
        img = ImageTk.PhotoImage(img)
        next_image_label.config(image=img)
        next_image_label.image = img
    else:
        # Display message for no more images
        next_post_label.config(text="No more images to post.")
        next_image_label.config(image='')

def update_ui():
    try:
        next_run = schedule.next_run()
        now = datetime.now()
        time_left = next_run - now
        time_left_str = str(time_left).split('.')[0]

        time_left_label.config(text=f"Time left until next post: {time_left_str}")
    except:
        pass
    
    root.after(1000, update_ui)

def main():
    global root, status_label, next_post_label, time_left_label, next_image_label

    root = tk.Tk()
    root.title("Instagram Scheduler")
    root.geometry("400x400")

    status_label = ttk.Label(root, text="Status: Logging in...")
    status_label.pack(pady=10)

    next_post_label = ttk.Label(root, text="Next post caption:\nN/A", anchor='w')
    next_post_label.pack(pady=10, padx=10, fill='x')

    next_image_label = ttk.Label(root)
    next_image_label.pack(pady=10)

    time_left_label = ttk.Label(root, text="Time left until next post: N/A")
    time_left_label.pack(pady=10)

    login_and_start_scheduler()
    update_ui()
    
    root.mainloop()

if __name__ == '__main__':
    main()
