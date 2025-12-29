# News Digest Email Bot

This project fetches news articles from NewsAPI, filters them by keywords (in any language), extracts relevant snippets, translates content into Ukrainian, and sends a formatted HTML email via the Gmail API.

The pipeline is designed to handle:
- non-English news sources
- embedded HTML in article content
- truncated NewsAPI text
- noisy bullet lists and formatting artifacts
- duplicate or overlapping snippets

---

## Features

- Fetches news from **NewsAPI**
- Keyword matching works for **any language**
- Automatic fallback translation to English for keyword detection
- Controlled snippet extraction with overlap prevention
- HTML stripping and entity decoding
- Translation to Ukrainian for final email output
- Gmail API email delivery (OAuth 2.0)
- Translation caching to reduce API calls

---

## Requirements

- Python 3.10+
- Google account
- NewsAPI API key

---

## Installation

```bash
git clone https://github.com/desaga/news-scraper
cd news-scraper
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root:
[https://newsapi.org](https://newsapi.org/)

```env
API_KEY=your_newsapi_key_here
```

---

## Usage

```bash
python main.py
```

On the first run, a browser window will open for Google OAuth authorization.  
After authorization, emails are sent automatically without further prompts.

---

## Project Structure

```
.
├── main.py
├── send_email.py
├── credentials.json
├── token.json
├── .env
├── requirements.txt
└── README.md
```

- `credentials.json` – Google OAuth client secrets (manual download)
- `token.json` – generated automatically after first authorization

---

## Email Output

Each email contains:
- Clickable article titles
- Clean, readable Ukrainian text
- Short contextual snippets explaining relevance
- No bullet artifacts, broken HTML, or truncated words

---

## Google OAuth Setup (How to Get `credentials.json`)

The Gmail API requires OAuth 2.0 authentication.  
You must manually download `credentials.json` from Google Cloud.

---

### Step 1: Create a Google Cloud Project

1. Go to: https://console.cloud.google.com/
2. Create a new project or select an existing one

---

### Step 2: Enable Gmail API

1. Open **APIs & Services → Library**
2. Search for **Gmail API**
3. Click **Enable**

---

### Step 3: Configure OAuth Consent Screen

1. Go to **APIs & Services → OAuth consent screen**
2. User type: **External**
3. Publishing status: **Testing**
4. Add your Gmail address to **Test users**
5. Save changes

---

### Step 4: Create OAuth Client ID

1. Go to **APIs & Services → Credentials**
2. Click **Create Credentials → OAuth client ID**
3. Application type: **Desktop app**
4. Create the client

---

### Step 5: Download Client Secrets

1. Open the created OAuth client
2. Click **Download JSON**
3. Rename the downloaded file to:

```
credentials.json
```

4. Place the file in the project root directory

---

### Step 6: First Authorization

Run the script:

```bash
python main.py
```

- A browser window will open
- Log in to your Google account
- Approve access
- `token.json` will be created automatically

After this step, no further authorization is required.

---

## Security Notes

- Never commit `credentials.json` or `token.json` to GitHub
- Add both files to `.gitignore`
- Treat OAuth client secrets as sensitive credentials

---

## Limitations

- NewsAPI `content` is frequently truncated
- Snippets are extracted from partial text by design
- The project does not attempt to reconstruct missing article content

---

## License

MIT License
