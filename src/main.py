import tkinter as tk
from tkinter import ttk
from threading import Thread
from datetime import datetime
from PIL import Image, ImageTk
import schedule
from config import get_config
import instagram_scheduler as ig

def login_and_start_scheduler():
    """
    Logs in to Instagram and starts the scheduler.
    """
    username, password = get_config()
    client = ig.login_instagram(username, password)
    status_label.config(text="Status: Logged in")
    ig.ensure_directories_and_files()

    # Start the scheduler in a separate thread
    scheduler_thread = Thread(target=ig.scheduler, args=(client, update_status, update_next_image))
    scheduler_thread.daemon = True
    scheduler_thread.start()

def update_status(status_message):
    """
    Updates the status label with a new status message.
    """
    status_label.config(text=f"Status: {status_message}")

def resize_image(image, max_width, max_height):
    """
    Resizes the image while maintaining the aspect ratio to fit within the specified dimensions.
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
    """
    Updates the next image and caption to be posted.
    """
    if image_path != "No more images":
        next_post_label.config(text=f"Next post caption:\n{caption}")
        
        img = Image.open(image_path)
        img = resize_image(img, 200, 200)
        img = ImageTk.PhotoImage(img)
        next_image_label.config(image=img)
        next_image_label.image = img
    else:
        next_post_label.config(text="No more images to post.")
        next_image_label.config(image='')

def update_ui():
    """
    Periodically updates the UI with the time left until the next post.
    """
    try:
        next_run = schedule.next_run()
        now = datetime.now()
        time_left = next_run - now
        time_left_str = str(time_left).split('.')[0]

        time_left_label.config(text=f"Time left until next post: {time_left_str}")
    except:
        pass
    
    # Schedule the next UI update
    root.after(1000, update_ui)

def main():
    """
    Main function to set up and run the Tkinter GUI.
    """
    global root, status_label, next_post_label, time_left_label, next_image_label, profile_pic_label, username_label

    root = tk.Tk()
    root.title("Instagram Scheduler")
    root.geometry("400x500")

    # Status label at the bottom left
    status_label = ttk.Label(root, text="Status: Logging in...")
    status_label.place(x=10, y=470)

    # Signature label at the bottom right
    love_label = ttk.Label(root, text="Created with Love by Gargant")
    love_label.place(x=230, y=470)

    # Next post label
    next_post_label = ttk.Label(root, text="Next post caption:\nN/A", anchor='w')
    next_post_label.pack(pady=10, padx=10, fill='x')

    # Next image label
    next_image_label = ttk.Label(root)
    next_image_label.pack(pady=10)

    # Time left label
    time_left_label = ttk.Label(root, text="Time left until next post: N/A")
    time_left_label.pack(pady=10)

    login_and_start_scheduler()
    update_ui()
    
    root.mainloop()

if __name__ == '__main__':
    main()
