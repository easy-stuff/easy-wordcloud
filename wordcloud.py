import glob
import os
import re
from collections import Counter

import click
import numpy as np
from PIL import Image
from wordcloud import WordCloud, STOPWORDS

# Default filter terms to exclude
DEFAULT_FILTER_TERMS = [
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


def load_mask_image(mask_filename: str):
    try:
        mask_image = np.array(Image.open(mask_filename))
        return mask_image
    except Exception as e:
        click.echo(f"[!] Error loading mask image '{mask_filename}': {e}", err=True)
        return None


def read_all_txt(folder_path: str, pattern: str = "combined.txt") -> str:
    text = ""
    glob_pattern = os.path.join(folder_path, pattern)

    files = glob.glob(glob_pattern)
    if not files:
        click.echo(f"[!] No files matched pattern: {glob_pattern}", err=True)

    for file_path in files:
        click.echo(f"[*] Reading: {file_path}")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                text += f.read() + " "
        except UnicodeDecodeError:
            click.echo(
                f"[!] Skipping {file_path}: Unable to decode with UTF-8.",
                err=True,
            )
            continue

    click.echo(f"[*] Total text length: {len(text)}")
    return text


def generate_and_save_wordcloud(
    text: str,
    stopwords_enabled: bool,
    image_filename: str,
    txt_filename: str,
    filter_terms,
    mask_image,
    max_words: int,
):
    # Extract only alphabetic words
    words = re.findall(r"\b[a-zA-Z]+\b", text.lower())

    # Build set of words to remove
    if stopwords_enabled:
        blocked = set(STOPWORDS) | set(filter_terms)
    else:
        blocked = set(filter_terms)

    # Filter words
    words = [w for w in words if w not in blocked and len(w) > 1]

    if not words:
        click.echo("[!] No valid words left after filtering. Skipping.", err=True)
        return

    word_counts = Counter(words)

    # Save frequencies to txt
    with open(txt_filename, "w", encoding="utf-8") as txt_file:
        for word, count in word_counts.items():
            txt_file.write(f"{word}: {count}\n")

    # Build word cloud
    wc = WordCloud(
        width=1920,
        height=1080,
        background_color="black",
        colormap="twilight",
        stopwords=STOPWORDS if stopwords_enabled else set(),
        max_words=max_words,
        max_font_size=100,
        min_font_size=10,
        contour_color="white",
        contour_width=2,
        relative_scaling=0.5,
        normalize_plurals=False,
        mask=mask_image,
    )

    cloud = wc.generate_from_frequencies(word_counts)

    # Save image
    cloud.to_file(image_filename)
    click.echo(f"[+] Saved {image_filename} and {txt_filename}")


@click.command()
@click.option(
    "-f",
    "--folder",
    "folder_path",
    type=click.Path(exists=True, file_okay=False, readable=True),
    default=".",
    show_default=True,
    help="Folder containing the text file(s).",
)
@click.option(
    "-p",
    "--pattern",
    "filename_pattern",
    default="combined.txt",
    show_default=True,
    help="Glob pattern for input text files inside the folder.",
)
@click.option(
    "-m",
    "--mask",
    "mask_filename",
    type=click.Path(exists=True, dir_okay=False, readable=True),
    default="mask.png",
    show_default=True,
    help="Path to mask image (PNG).",
)
@click.option(
    "-o",
    "--output-dir",
    "output_dir",
    type=click.Path(file_okay=False, dir_okay=True),
    default=".",
    show_default=True,
    help="Directory to save output images and txt files.",
)
@click.option(
    "--max-words",
    type=int,
    default=150,
    show_default=True,
    help="Maximum number of words in the word cloud.",
)
@click.option(
    "--filter-term",
    "-t",
    "extra_filter_terms",
    multiple=True,
    help="Additional word(s) to filter out (can be passed multiple times).",
)
@click.option(
    "--include-stopwords",
    is_flag=True,
    help="Generate word cloud that includes stopwords (default behaviour).",
)
@click.option(
    "--exclude-stopwords",
    is_flag=True,
    help="Generate word cloud that excludes stopwords (default behaviour).",
)
def cli(
    folder_path,
    filename_pattern,
    mask_filename,
    output_dir,
    max_words,
    extra_filter_terms,
    include_stopwords,
    exclude_stopwords,
):
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Load mask image
    mask_image = load_mask_image(mask_filename)
    if mask_image is None:
        raise click.ClickException("Failed to load mask image. Exiting.")

    # Read text
    text = read_all_txt(folder_path, pattern=filename_pattern)
    if not text.strip():
        raise click.ClickException("No valid text found in input files. Exiting.")

    # Combine default + extra filter terms
    filter_terms = DEFAULT_FILTER_TERMS + list(extra_filter_terms)

    # Decide what to generate
    # - If no flags: generate both
    # - If flags: respect them
    generate_with = include_stopwords or not (include_stopwords or exclude_stopwords)
    generate_without = exclude_stopwords or not (include_stopwords or exclude_stopwords)

    if generate_with:
        img_path = os.path.join(output_dir, "image_with_stopwords.png")
        txt_path = os.path.join(output_dir, "words_with_stopwords.txt")
        click.echo("[*] Generating word cloud WITH stopwords...")
        generate_and_save_wordcloud(
            text=text,
            stopwords_enabled=True,
            image_filename=img_path,
            txt_filename=txt_path,
            filter_terms=filter_terms,
            mask_image=mask_image,
            max_words=max_words,
        )

    if generate_without:
        img_path = os.path.join(output_dir, "image_without_stopwords.png")
        txt_path = os.path.join(output_dir, "words_without_stopwords.txt")
        click.echo("[*] Generating word cloud WITHOUT stopwords...")
        generate_and_save_wordcloud(
            text=text,
            stopwords_enabled=False,
            image_filename=img_path,
            txt_filename=txt_path,
            filter_terms=filter_terms,
            mask_image=mask_image,
            max_words=max_words,
        )


if __name__ == "__main__":
    cli()
