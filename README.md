# easy-wordcloud

Create word cloud images easily and quickly from text files, with mask support, filtering, and a flexible command-line interface.

## Features

* Generate masked word clouds using any PNG silhouette or shape
* Filter out unwanted words (built-in list + custom terms)
* Optionally include or exclude stopwords
* Read from any folder and any filename pattern
* Export both the word cloud image and a text file with word frequencies
* Full CLI built with `click`
* Output is generated in 1080p resolution

## Installation

Clone the repository:

```bash
git clone https://github.com/easy-stuff/easy-wordcloud.git
cd easy-wordcloud
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Basic Usage

If your folder contains `combined.txt` and `mask.png`, simply run:

```bash
python easy-wordcloud.py
```

This will produce:

* `image_with_stopwords.png`
* `image_without_stopwords.png`
* `words_with_stopwords.txt`
* `words_without_stopwords.txt`

## Command-Line Options

### Use a different input folder

```bash
python easy-wordcloud.py --folder ./emails
```

### Use a different filename pattern

```bash
python easy-wordcloud.py --pattern "*.txt"
```

### Use a custom mask image

```bash
python easy-wordcloud.py --mask ./mask.png
```

### Specify an output directory

```bash
python easy-wordcloud.py --output-dir ./output
```

### Only generate the version without stopwords

```bash
python easy-wordcloud.py --exclude-stopwords
```

### Only generate the version with stopwords

```bash
python easy-wordcloud.py --include-stopwords
```

### Add custom terms to filter

```bash
python easy-wordcloud.py -t hi -t thanks -t regards
```

### Full example

```bash
python easy-wordcloud.py \
  --folder ./emails \
  --pattern "*.txt" \
  --mask mask.png \
  --output-dir ./results \
  --exclude-stopwords \
  -t confidential -t forwarded \
  --max-words 200
```

## Input Requirements

The tool expects text files located in the folder you specify, and optionally a PNG mask.
Typical structure:

```
project/
    combined.txt
    mask.png
```

You can also use patterns like:

```
--pattern "*.log"
--pattern "email_*.txt"
```

## How It Works

1. Text files matching your pattern are read and combined.
2. Only alphabetic words are extracted.
3. Filter terms and stopwords (if enabled) are removed.
4. Word frequencies are counted.
5. A masked word cloud is generated.
6. The image and frequency list are written to the output directory.

## Output Files

The tool generates:

```
image_with_stopwords.png
image_without_stopwords.png
words_with_stopwords.txt
words_without_stopwords.txt
```

(Depending on which modes you enable.)
