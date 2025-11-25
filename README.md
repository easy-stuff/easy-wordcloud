# easy-wordcloud

Create word cloud images easily and quickly from text files, with mask support, filtering, and a flexible command-line interface.

## Features

* Automatically reads all `.txt` files in the current folder by default
* Supports custom filename patterns
* Optional mask images for shaped word clouds
* Built-in filter terms + user-defined exclusions
* Optionally include or exclude stopwords
* Outputs a 1080p word cloud image and a text file containing word frequencies
* Simple command-line interface built with `click`

## Installation

```bash
pip install click wordcloud pillow numpy matplotlib
```

Clone the repository:

```bash
git clone https://github.com/yourusername/easy-wordcloud.git
cd easy-wordcloud
```

## Basic Usage

Without any arguments, the tool:

* Reads **all `.txt` files in the current directory**
* Looks for **mask.png**
* Outputs both versions (with and without stopwords)

```bash
python easy-wordcloud.py
```

This generates:

```
image_with_stopwords.png
image_without_stopwords.png
words_with_stopwords.txt
words_without_stopwords.txt
```

## Command-Line Options

### Use a different input folder

```bash
python easy-wordcloud.py --folder ./emails
```

### Use a custom filename pattern (default: "*.txt")

```bash
python easy-wordcloud.py --pattern "*.log"
python easy-wordcloud.py --pattern "email_*.txt"
```

### Use a custom mask image

```bash
python easy-wordcloud.py --mask ./shapes/circle.png
```

### Choose output directory

```bash
python easy-wordcloud.py --output-dir ./out/
```

### Only generate “without stopwords”

```bash
python easy-wordcloud.py --exclude-stopwords
```

### Only generate “with stopwords”

```bash
python easy-wordcloud.py --include-stopwords
```

### Add custom filter terms

```bash
python easy-wordcloud.py -t confidential -t regards -t thanks
```

### Complete example

```bash
python easy-wordcloud.py \
  --folder ./notes \
  --pattern "*.txt" \
  --mask silhouette.png \
  --output-dir results \
  --max-words 200 \
  -t hi -t thanks \
  --exclude-stopwords
```

## Input Requirements

By default, the tool processes:

```
*.txt
mask.png
```

in the current working directory.

You can override these with `--folder`, `--pattern`, and `--mask`.

## How It Works

1. All text files matching the chosen pattern are read and merged.
2. Only alphabetic words are extracted.
3. Stopwords and filter terms are removed (depending on flags).
4. Word frequencies are counted.
5. A word cloud is generated using your mask (if provided).
6. A PNG image and a text file of frequencies are written to the output directory.

## Output Files

Depending on what you choose to generate, you may get:

```
image_with_stopwords.png
image_without_stopwords.png
words_with_stopwords.txt
words_without_stopwords.txt
```
