
# Instagram Scheduler

  

Automatically schedule and post images with captions to Instagram using Python and Instagrapi.

  

## Table of Contents

  

- [Overview](#overview)

- [Features](#features)

- [Installation](#installation)

- [Usage](#usage)

- [Configuration](#configuration)

- [Contributing](#contributing)

- [License](#license)

  

## Overview

  

Instagram Scheduler is a Python script that allows you to schedule the posting of images to Instagram at a specific time each day. It reads images from a designated folder, selects one that hasn't been posted yet, and posts it with a randomly chosen caption from a text file.

  

The script utilizes the Instagrapi library for interacting with Instagram and provides a simple scheduling mechanism using the `schedule` library.

  

## Features

  

- Automatically post images to Instagram at a scheduled time each day.

- Randomly select captions from a file for each image post.

- Ensure only new images are posted by keeping track of posted images in a text file.

- Easy setup and configuration through a `.env` file for Instagram credentials.

  

## Installation

  

1. Clone the repository:

```
git clone todo
cd instagram-scheduler
```

  

2. Install dependencies:

```
pip install -r requirements.txt
```

  
  

3. Set up environment variables:

- Create a `.env` file in the root directory.

- Add your Instagram account credentials in the following format:

```

ACCOUNT_USERNAME=your_instagram_username

ACCOUNT_PASSWORD=your_instagram_password

```

  

## Usage

  

Run the script to start scheduling and posting images to Instagram:

```
python main.py
```

  

The script will run indefinitely, scheduling posts for each day at 16:00 (4:00 PM) local time.

  

## Configuration

  

Ensure the following directories and files exist and are accessible:

  

-  `data/images/`: Store your images here.

-  `data/posted_images.txt`: Track posted images.

-  `data/captions.txt`: Store captions for posts.

  

Modify `data/captions.txt` with your desired captions, each on a new line.

  

## Contributing

  

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or create a pull request.

  

## License

  

This project is licensed under the MIT License - see the LICENSE file for details.