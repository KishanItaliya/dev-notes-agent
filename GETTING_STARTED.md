# Getting Started with ML Notes Agent (Local Setup Guide)

This guide walks you through setting up and running the ML Notes Agent on your local Windows machine.

---

## What This Agent Does

The ML Notes Agent automates study-note creation from YouTube videos. You give it a YouTube URL, and it:

1. Extracts the video transcript (subtitles)
2. Summarizes the content using Groq AI (free LLM)
3. Researches the topic on DuckDuckGo for real-world context
4. Generates structured Markdown notes (`.md`) and Python code examples (`.py`)
5. Pushes both files to your GitHub repository

```
YouTube URL --> Transcript --> AI Summary --> Web Research --> .md + .py --> GitHub
```

---

## Prerequisites

- **Python 3.10+** installed on your machine
- A **GitHub account**
- A **Groq account** (free)
- An internet connection

---

## Step-by-Step Setup

### Step 1: Verify Python is installed

Open PowerShell or Command Prompt and run:

```powershell
python --version
```

You need Python 3.10 or higher. If not installed, download it from [python.org](https://www.python.org/downloads/).

### Step 2: Navigate to the project directory

```powershell
cd "d:\Learnings\AI Agent\Youtube_Notes"
```

### Step 3: (Recommended) Create a virtual environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

> If you get an execution policy error, run:
> `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

### Step 4: Install dependencies

```powershell
pip install -r requirements.txt
```

This installs:
| Package | Purpose |
|---|---|
| `youtube-transcript-api` | Extracts YouTube video subtitles (no API key needed) |
| `requests` | HTTP requests to Groq, GitHub, and DuckDuckGo |
| `beautifulsoup4` | Parses DuckDuckGo HTML search results |
| `lxml` | Faster HTML parser backend for BeautifulSoup |

### Step 5: Get a free Groq API Key

1. Go to [console.groq.com](https://console.groq.com)
2. Sign up / log in
3. Navigate to **API Keys** and click **Create API Key**
4. Copy the key (starts with `gsk_...`)

The free tier provides ~14,400 requests/day with `llama-3.3-70b-versatile`, which is more than enough.

### Step 6: Get a GitHub Personal Access Token

1. Go to GitHub -> **Settings** -> **Developer settings** -> **Personal access tokens** -> **Tokens (classic)**
2. Click **Generate new token (classic)**
3. Give it a descriptive name (e.g., "ML Notes Agent")
4. Check the **repo** scope (full control of private repositories)
5. Click **Generate token** and copy it (starts with `ghp_...`)

### Step 7: Create your GitHub notes repository

1. Create a new repository on GitHub (e.g., `your-username/ml-notes`)
2. Initialize it with a README or any file
3. Create a folder called `notes/` inside it (add a `.gitkeep` file inside it as a placeholder)

### Step 8: Set environment variables

In PowerShell, set these before running the agent:

```powershell
$env:GROQ_API_KEY = "gsk_xxxxxxxxxxxxxxxxxxxx"
$env:GITHUB_TOKEN = "ghp_xxxxxxxxxxxxxxxxxxxx"
$env:GITHUB_REPO  = "your-username/ml-notes"
```

> **Note:** These variables only persist for the current PowerShell session. To make them permanent, add them via:
> **System Properties** -> **Environment Variables** -> **User variables** -> **New**

Alternatively, you can edit the CONFIG section directly at the top of `ml_notes_agent.py` (lines 35-37), but environment variables are preferred so you don't accidentally commit secrets.

### Step 9: Run the agent

```powershell
python ml_notes_agent.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

Replace `VIDEO_ID` with an actual YouTube video ID. The video **must have subtitles/CC enabled**.

---

## What Happens When You Run It

```
ML Notes Agent starting ...
   URL: https://www.youtube.com/watch?v=VIDEO_ID

   Video: 'Some ML Lecture Title' by ChannelName
  [1/5] Fetching transcript ...
  [2/5] Summarizing with AI ...
   Topic detected: Gradient Descent
  [3/5] Researching industry usage ...
  [4a/5] Generating Markdown notes ...
  [4b/5] Generating Python examples ...
  [5/5] Pushing to GitHub ...
   Notes pushed  -> https://github.com/you/ml-notes/blob/main/notes/20260322_gradient_descent.md
   Code pushed   -> https://github.com/you/ml-notes/blob/main/notes/20260322_gradient_descent.py

Done! Files are live on GitHub.
```

---

## Output Structure

Files are pushed into the `notes/` folder in your GitHub repo:

```
ml-notes/
  notes/
    20260322_gradient_descent.md      <-- Structured study notes
    20260322_gradient_descent.py      <-- Runnable Python code examples
    20260323_neural_networks_basics.md
    20260323_neural_networks_basics.py
    ...
```

### The `.md` file contains:
- Overview / plain-English summary
- Key concepts explained (simple first, then in-depth)
- Real-world usage and industry examples
- Best practices and production tips
- Further reading suggestions

### The `.py` file contains:
- Clean, commented Python code examples
- Type hints and docstrings
- A `__main__` block for running demos
- Uses numpy/scikit-learn/PyTorch as appropriate

---

## Configuration Options

These can be changed in the CONFIG section of `ml_notes_agent.py` (or via environment variables where supported):

| Variable | Default | Description |
|---|---|---|
| `GROQ_MODEL` | `llama-3.3-70b-versatile` | The LLM model to use on Groq |
| `NOTES_FOLDER` | `notes` | Target folder inside your GitHub repo |
| `MAX_TRANSCRIPT_CHARS` | `12000` | Transcript is trimmed beyond this length |
| `MAX_RESEARCH_RESULTS` | `4` | Number of DuckDuckGo snippets to include |

---

## Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| `TranscriptsDisabled` error | Video has no subtitles | Use a video that has CC (closed captions) enabled |
| Groq rate limit / 429 error | Too many requests in a short time | Wait a few minutes, or add `time.sleep(3)` between batch runs |
| GitHub 404 on push | The `notes/` folder doesn't exist in the repo | Create the folder with a `.gitkeep` file first |
| Research returns nothing | DuckDuckGo blocked scraping temporarily | Notes still generate from the transcript; research section will be empty |
| `ModuleNotFoundError` | Dependencies not installed | Run `pip install -r requirements.txt` |
| `ValueError: Cannot extract video ID` | Unsupported URL format | Use standard YouTube URLs: `youtube.com/watch?v=...` or `youtu.be/...` |

---

## Architecture at a Glance

```
ml_notes_agent.py
  |
  |-- extract_video_id()       Parse YouTube URL -> video ID
  |-- get_video_metadata()     Fetch title/channel via YouTube oEmbed (no key)
  |-- get_transcript()         Pull subtitles via youtube-transcript-api
  |-- groq_chat()              Generic wrapper for Groq chat completions API
  |-- summarize_transcript()   LLM extracts topic, concepts, prerequisites
  |-- research_topic()         Scrapes DuckDuckGo for industry context
  |-- generate_notes()         LLM writes structured .md notes
  |-- generate_code()          LLM writes .py code examples
  |-- push_to_github()         Commits file to GitHub via REST API
  |-- run_agent()              Orchestrates the full pipeline (steps 1-5)
```

---

## Tips

- Run the agent right after watching a video to compare your understanding with the generated notes.
- The video must have English subtitles for the transcript extraction to work.
- You can batch multiple videos by calling `run_agent()` in a loop, but add a `time.sleep(3)` between calls to avoid rate limits.
- Review and annotate the generated `.md` files with your own observations for better retention.
