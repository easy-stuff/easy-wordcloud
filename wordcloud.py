from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import glob
import os
import re
from collections import Counter
import numpy as np
from PIL import Image

# Filter terms to exclude
filter_terms = [
    "from",
    "sent",
    "to",
    "subject",
    "attachments",
    "call",
    "re",
    "fw",
    "no",
    "pm",
    "co",
    "wrote",
    "message",
    "forwarded",
    "date",
    "recipients",
]


# Load mask image for word cloud
def load_mask_image(mask_filename):
    try:
        mask_image = np.array(Image.open(mask_filename))
        return mask_image
    except Exception as e:
        print(f"Error loading mask image: {e}")
        return None


def read_all_txt(folder_path):
    text = ""
    for file_path in glob.glob(os.path.join(folder_path, "combined.txt")):
        print(f"Reading: {file_path}")  # Debug line
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                text += f.read() + " "
        except UnicodeDecodeError:
            # If the file can't be read in UTF-8, skip it
            print(f"Skipping {file_path}: Unable to decode with UTF-8.")
            continue  # Skip to the next file
    print(f"Total text length: {len(text)}")  # Debug line
    return text


def generate_and_save_wordcloud(
    text, stopwords, image_filename, txt_filename, filter_terms, mask_image
):
    words = re.findall(r"\b[a-zA-Z]+\b", text.lower())  # Only words, no numbers
    if stopwords:
        # Remove stopwords (with stopwords) and filter terms
        words = [
            word
            for word in words
            if word not in STOPWORDS and word not in filter_terms and len(word) > 1
        ]
    else:
        # No stopwords, just single-letter word removal and filter terms
        words = [word for word in words if word not in filter_terms and len(word) > 1]

    word_counts = Counter(words)

    # Save words list to a txt file
    with open(txt_filename, "w", encoding="utf-8") as txt_file:
        for word, count in word_counts.items():
            txt_file.write(f"{word}: {count}\n")

    # Generate word cloud with the mask
    wc = WordCloud(
        width=1920,  # Set width to 1920 for 1080p resolution
        height=1080,  # Set height to 1080 for 1080p resolution
        background_color="black",
        colormap="twilight",  # Using the 'twilight' colormap
        stopwords=STOPWORDS if stopwords else set(),
        max_words=150,  # Limit the number of words shown
        max_font_size=100,  # Increase the maximum font size
        min_font_size=10,  # Set a minimum font size for readability
        contour_color="white",  # Add a white contour to the words for better visibility
        contour_width=2,  # Adjust contour width for readability
        relative_scaling=0.5,  # Adjust how word frequency scales with word size
        normalize_plurals=False,  # Avoid plural word collapsing
        mask=mask_image,  # Apply the mask
    )
    cloud = wc.generate_from_frequencies(word_counts)

    # Save word cloud image
    cloud.to_file(image_filename)
    print(f"Saved {image_filename} and {txt_filename}")


def generate_word_cloud_from_folder(folder_path, mask_image):
    text = read_all_txt(folder_path)
    if not text.strip():
        print("No valid text found in the UTF-8 files.")
        return  # Exit if no valid UTF-8 text was found

    # Generate word cloud with stopwords
    generate_and_save_wordcloud(
        text,
        stopwords=True,
        image_filename="image1.png",
        txt_filename="words_with_stopwords.txt",
        filter_terms=filter_terms,
        mask_image=mask_image,
    )

    # Generate word cloud without stopwords
    generate_and_save_wordcloud(
        text,
        stopwords=False,
        image_filename="image2.png",
        txt_filename="words_without_stopwords.txt",
        filter_terms=filter_terms,
        mask_image=mask_image,
    )


# Example: Call the function to process text files in the current directory
mask_image = load_mask_image("mask.png")  # Load the mask image
if mask_image is not None:
    generate_word_cloud_from_folder(".", mask_image)  # Use current directory (.)
else:
    print("Failed to load mask image. Exiting.")
