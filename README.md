# Uzum Reviews Scraper

A web scraper that extracts product reviews from [uzum.uz](https://uzum.uz) using Playwright.

## What it does

- Automatically loads all reviews by clicking the "load more" button
- Extracts: author name, date, star rating, pros, cons, and comment
- Saves results to a JSON file with proper UTF-8 encoding (Cyrillic/Uzbek text supported)

## Sample Output

```json
[
  {
    "name": "Iskander",
    "date": "4 Noyabr 2025",
    "rating": 5,
    "pros": "Eng arzoni Uzumda, raxmat IMEI o'tkan",
    "cons": "Kamchilik yo'q",
    "comment": "Sotuvchi va Uzum marketga raxmat, 1 kunda etkazib berishdi"
  }
]
```

## Tech Stack

- Python 3.9+
- [Playwright](https://playwright.dev/python/) — browser automation
- JSON — data storage

## Installation

```bash
pip install playwright
playwright install chromium
```

## Usage

```bash
python3 uzum.py
```

Results are saved to `reviews.json`.

## What I learned building this

- Dynamic content loading with Playwright
- "Load more" pagination pattern
- CSS selector specificity (`:not()` pseudo-class)
- Handling missing elements gracefully
- UTF-8 encoding for multilingual text