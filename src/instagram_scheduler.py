import os
import schedule
import time
import random
from instagrapi import Client
from datetime import datetime

IMAGES_FOLDER = 'data/images'
POSTED_IMAGES_FILE = 'data/posted_images.txt'
CAPTIONS_FILE = 'data/captions.txt'
CAPTIONS_SUFFIX_FILE = 'data/caption_suffix.txt'

def ensure_directories_and_files():
    """
    Ensure that necessary directories and files exist.
    """
    os.makedirs(IMAGES_FOLDER, exist_ok=True)
    
    if not os.path.exists(POSTED_IMAGES_FILE):
        with open(POSTED_IMAGES_FILE, 'w') as f:
            pass

    if not os.path.exists(CAPTIONS_SUFFIX_FILE):
        with open(CAPTIONS_SUFFIX_FILE, 'w') as f:
            f.write("\n")
    
    if not os.path.exists(CAPTIONS_FILE):
        with open(CAPTIONS_FILE, 'w') as f:
            f.write("No caption available\n")

def read_images_from_folder():
    """
    Read images from the images folder and return a list of image file paths.
    """
    images = [os.path.join(IMAGES_FOLDER, img) for img in os.listdir(IMAGES_FOLDER) if img.lower().endswith(('png', 'jpg', 'jpeg'))]
    return images

def mark_image_as_posted(image_path):
    """
    Mark an image as posted by adding its path to the posted images file.
    """
    with open(POSTED_IMAGES_FILE, 'a') as f:
        f.write(image_path + '\n')

def get_unposted_images(images):
    """
    Get the list of images that have not yet been posted.
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
    """
    if not os.path.exists(CAPTIONS_SUFFIX_FILE):
        return ""
    
    with open(CAPTIONS_SUFFIX_FILE, 'r') as f:
        suffix = f.read()
    
    return suffix

def read_captions_from_file():
    """
    Read captions from the captions file and return a list of captions.
    """
    if not os.path.exists(CAPTIONS_FILE):
        return ["No caption available"]
    
    with open(CAPTIONS_FILE, 'r') as f:
        captions = f.read().splitlines()
    
    return captions

def post_image(cl, image_path, caption):
    """
    Post an image to Instagram with a specific caption.
    """
    try:
        cl.photo_upload(image_path, caption=caption)
        mark_image_as_posted(image_path)
        return f'Successfully posted {image_path} with caption: "{caption}"'
    except Exception as e:
        return f'Failed to post {image_path}: {e}'

def scheduler(cl, update_status_callback, update_next_image_callback):
    """
    Schedule a job to post an image every day at 16:00.
    """
    images = read_images_from_folder()
    unposted_images = get_unposted_images(images)
    
    if not unposted_images:
        update_status_callback('No unposted images available.')
        return
    
    captions = read_captions_from_file()
    caption_suffix = read_caption_suffix_from_file()
    
    def job():
        image_to_post = random.choice(unposted_images)
        caption_to_post = random.choice(captions)
        full_caption = f"{caption_to_post}{caption_suffix}"
        result = post_image(cl, image_to_post, full_caption)
        update_status_callback(result)
        unposted_images.pop(0)
        if unposted_images:
            update_next_image_callback(unposted_images[0], full_caption)
        else:
            update_next_image_callback("No more images", "")

    schedule.every().day.at("16:00").do(job)
    
    # Call update_next_image_callback initially
    if unposted_images:
        update_next_image_callback(unposted_images[0], f"{random.choice(captions)}\n{caption_suffix}")
    else:
        update_next_image_callback("No more images", "")
    
    while True:
        schedule.run_pending()
        time.sleep(1)

def login_instagram(username, password):
    """
    Login to Instagram.
    """
    cl = Client()
    cl.login(username, password)
    return cl
