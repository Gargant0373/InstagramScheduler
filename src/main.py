import os
import schedule
import time
import random
from instagrapi import Client
from datetime import datetime, timedelta

from config import get_config

IMAGES_FOLDER = 'data/images'
POSTED_IMAGES_FILE = 'data/posted_images.txt'
CAPTIONS_FILE = 'data/captions.txt'
CAPTIONS_SUFFIX_FILE = 'data/caption_suffix.txt'

def ensure_directories_and_files():
    """
    Ensure that necessary directories and files exist.
    - Create the images folder if it does not exist.
    - Create the posted images file if it does not exist.
    - Create the captions file if it does not exist, and add a default caption.
    """
    # Create directories if they do not exist
    os.makedirs(IMAGES_FOLDER, exist_ok=True)
    
    # Create files if they do not exist
    if not os.path.exists(POSTED_IMAGES_FILE):
        with open(POSTED_IMAGES_FILE, 'w') as f:
            pass  # Just create an empty file

    if not os.path.exists(CAPTIONS_SUFFIX_FILE):
        with open(CAPTIONS_SUFFIX_FILE, 'w') as f:
            f.write("\n") # Create file with an empty suffix
    
    if not os.path.exists(CAPTIONS_FILE):
        with open(CAPTIONS_FILE, 'w') as f:
            f.write("No caption available\n")  # Create file with a default caption

def read_images_from_folder():
    """
    Read images from the images folder and return a list of image file paths.
    Only files with extensions 'png', 'jpg', or 'jpeg' are included.
    """
    images = [os.path.join(IMAGES_FOLDER, img) for img in os.listdir(IMAGES_FOLDER) if img.lower().endswith(('png', 'jpg', 'jpeg'))]
    return images

def mark_image_as_posted(image_path):
    """
    Mark an image as posted by adding its path to the posted images file.
    This prevents the same image from being posted multiple times.
    """
    with open(POSTED_IMAGES_FILE, 'a') as f:
        f.write(image_path + '\n')

def get_unposted_images(images):
    """
    Get the list of images that have not yet been posted.
    This is determined by checking the posted images file.
    """
    if not os.path.exists(POSTED_IMAGES_FILE):
        return images
    
    with open(POSTED_IMAGES_FILE, 'r') as f:
        posted_images = f.read().splitlines()
    
    unposted_images = [img for img in images if img not in posted_images]
    return unposted_images

def read_caption_suffix_from_file():
    """
    Read the caption suffix from caption_suffix.txt.
    If the file does not exist, return an empty string.
    """
    if not os.path.exists(CAPTIONS_SUFFIX_FILE):
        return ""
    
    with open(CAPTIONS_SUFFIX_FILE, 'r') as f:
        suffix = f.read()
    
    return suffix.strip()

def read_captions_from_file():
    """
    Read captions from the captions file and return a list of captions.
    If the file does not exist, return a list with a default caption.
    """
    if not os.path.exists(CAPTIONS_FILE):
        return ["No caption available"]
    
    with open(CAPTIONS_FILE, 'r') as f:
        captions = f.read().splitlines()
    
    return captions

def post_image(cl, image_path, caption):
    """
    Post an image to Instagram with a specific caption.
    Adds a specific call to action and hashtag to the caption.
    """
    caption += '\n\nCall us for reservations +40721373747\n\n#brasov'
    try:
        cl.photo_upload(image_path, caption=caption)
        print(f'Successfully posted {image_path} with caption: "{caption}"')
        mark_image_as_posted(image_path)
    except Exception as e:
        print(f'Failed to post {image_path}: {e}')

def scheduler(cl):
    """
    Schedule a job to post an image every day at 16:00.
    """
    images = read_images_from_folder()
    unposted_images = get_unposted_images(images)
    
    if not unposted_images:
        print('No unposted images available.')
        return
    
    captions = read_captions_from_file()
    image_to_post = unposted_images[0]
    caption_to_post = random.choice(captions)
    caption_suffix = read_caption_suffix_from_file()
    
    def job():
        post_image(cl, image_to_post, caption_to_post + caption_suffix)
    
    # Schedule the job to run every day at 16:00
    schedule.every().day.at("16:00").do(job)
    
    while True:
        now = datetime.now()
        next_run = schedule.next_run()
        time_left = next_run - now
        
        # Format time left as HH:MM:SS
        time_left_str = str(time_left).split('.')[0]
        
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f'Time left until next post: {time_left_str}')
        print(f'Next image to post: {image_to_post}')
        print(f'Next caption: {caption_to_post}\n{caption_suffix}')
        
        schedule.run_pending()
        time.sleep(1)

def main():
    """
    Main function to run the script.
    - Ensures directories and files exist.
    - Logs into Instagram.
    - Schedules the posting of images.
    """
    ensure_directories_and_files()
    
    print("Logging in...")
    
    # Get Instagram credentials from the config file
    (username, password) = get_config()
    cl = Client()
    cl.login(username, password)
    
    # Schedule the posting of images
    scheduler(cl)
    
if __name__ == '__main__':
    main()
