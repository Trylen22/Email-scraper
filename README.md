# Email scraper

A Python command-line experiment that reads Gmail messages, processes their contents, summarizes them with a local Ollama model, and writes JSON, HTML, or text reports.

## Workflow

1. Authenticate with the Gmail API using the read-only scope.
2. Fetch messages matching the requested query and count.
3. Process message bodies and extracted links.
4. Summarize message text using the configured local model.
5. Generate a report under `reports/` or at the requested output path.

## Local setup

Use a virtual environment. The current `requirements.txt` includes standard-library entries (`re` and `subprocess`) that are not installable packages; install the third-party dependencies explicitly:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install google-auth google-auth-oauthlib google-api-python-client pandas beautifulsoup4 matplotlib requests
```

Install Ollama separately and download the model used by `scr/main.py`:

```bash
ollama pull deepseek-r1:1.5b
```

Create a Gmail API desktop OAuth client for your own account and save its configuration as `client_secret.json` in the working directory. Run from the repository root so authentication and report paths resolve consistently:

```bash
.venv/bin/python scr/main.py --max-emails 5 --format json --query 'newer_than:7d'
```

The first run opens the OAuth consent flow. Subsequent runs reuse local `token.json`. Use `--format html` or `--format text` for other report formats; these modes may open a browser or viewer. `--r1` removes model thinking tags from summaries.

## Source map

| File | Responsibility |
|---|---|
| `scr/main.py` | CLI and pipeline orchestration |
| `scr/authemail.py` | Gmail OAuth and service creation |
| `scr/scrape_emails.py` | Message retrieval |
| `scr/process_emails.py` | Message processing |
| `scr/local_model.py` | Ollama invocation |
| `scr/report_generator.py` | Report output |

## Status and data

This is an experimental personal workflow with unpinned dependencies and several older scripts. Summaries require review and are not authoritative task assignments. The current portfolio update did not authenticate to Gmail, read a mailbox, or record personal email data.

Keep OAuth files, tokens, reports, and email exports local. The ignore rules prevent new copies from being staged; they do not remove files from earlier Git history. Only use accounts and message data you are authorized to process.
