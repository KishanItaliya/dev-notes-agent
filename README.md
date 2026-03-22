# 🤖 ML Notes Agent

Watches a YouTube tutorial → extracts transcript → summarizes with AI →
researches industry usage → generates `.md` notes + `.py` code examples →
pushes everything to your GitHub repo automatically.

**100% free to run.** No OpenAI. No paid APIs.

---

## ⚡ Quick Start (5 minutes)

### 1. Get a free Groq API key
Go to [console.groq.com](https://console.groq.com) → sign up → Create API Key.
The free tier gives you ~14,400 requests/day with llama-3.3-70b. More than enough.

### 2. Get a GitHub Personal Access Token
GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
→ Generate new token → tick **repo** scope → copy the token.

### 3. Create your notes repo on GitHub
Create a new repo, e.g. `your-username/ml-notes`.
Add a folder called `notes/` (create a placeholder `.gitkeep` file inside it).

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Set your secrets as environment variables
```bash
# Mac / Linux
export GROQ_API_KEY="gsk_xxxxxxxxxxxxxxxxxxxx"
export GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxx"
export GITHUB_REPO="your-username/ml-notes"

# Windows PowerShell
$env:GROQ_API_KEY="gsk_xxxxxxxxxxxxxxxxxxxx"
$env:GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxx"
$env:GITHUB_REPO="your-username/ml-notes"
```

Or edit the CONFIG section at the top of `ml_notes_agent.py` directly.

### 6. Run the agent!
```bash
python ml_notes_agent.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

That's it. In ~30 seconds you'll have a commit on GitHub with structured notes and
Python examples ready to review.

---

## 📂 Output file structure in your repo

```
ml-notes/
└── notes/
    ├── 20250610_gradient_descent.md
    ├── 20250610_gradient_descent.py
    ├── 20250611_neural_networks_basics.md
    ├── 20250611_neural_networks_basics.py
    └── ...
```

---

## 📝 What the generated .md file contains

| Section | Description |
|---|---|
| Overview | Plain-English summary of the lecture |
| Key Concepts | Each concept explained simply, then in depth |
| Real-World Usage | How this is used in production today |
| Best Practices | Production tips and common pitfalls |
| Code Examples | Link to the `.py` file (if generated) |
| Further Reading | Curated resources to go deeper |

---

## 🔧 Configuration options

Edit the CONFIG block at the top of `ml_notes_agent.py`:

| Variable | Default | Description |
|---|---|---|
| `GROQ_MODEL` | `llama-3.3-70b-versatile` | Free and very capable |
| `NOTES_FOLDER` | `notes` | Folder inside your GitHub repo |
| `MAX_TRANSCRIPT_CHARS` | `12000` | Trim transcripts longer than this |
| `MAX_RESEARCH_RESULTS` | `4` | Number of DuckDuckGo snippets to use |

---

## 🆓 Why is this free?

| Component | Tool | Cost |
|---|---|---|
| Transcript extraction | `youtube-transcript-api` | Free, no key |
| AI summarization & generation | Groq free tier | Free (14,400 req/day) |
| Web research | DuckDuckGo HTML scrape | Free, no key |
| GitHub push | GitHub REST API | Free with any account |

---

## 🛠 Troubleshooting

**"TranscriptsDisabled" error** — The video has no subtitles. Try a video that shows
the CC icon on YouTube.

**Groq rate limit** — The free tier is generous but if you batch many videos quickly,
add `time.sleep(3)` between runs.

**GitHub 404 on push** — Make sure the `notes/` folder exists in your repo.
Create a `.gitkeep` file inside it first.

**Research returns nothing** — DuckDuckGo occasionally blocks scraping. The agent
will still generate notes from the transcript; research context will just be absent.

---

## 💡 Pro tips

- Run it right after watching, while the lecture is fresh — compare your mental notes
  with what the agent generated.
- Commit the `.md` file with your own annotations added below the AI content.
- Add a weekly GitHub Action to compile all your notes into an index page.
