# Swapper

An automation script that randomly rotates your LinkedIn headline using a curated list of bios — because nobody likes LinkedIn, but everyone needs it.

---

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
[![Playwright](https://custom-icon-badges.demolab.com/badge/Playwright-2EAD33?style=for-the-badge&logo=playwright&logoColor=fff)](#)
![python-dotenv](https://img.shields.io/badge/python--dotenv-fff?style=for-the-badge&logo=python&logoColor=black)

---

## Overview

Stuck with the same stale Linkedin headline you've had since 2022? But you've always had so many good potential ones—you just ALWAYS forgot to change it?

This tool uses [Playwright](https://playwright.dev/) to automate the process of updating your LinkedIn profile headline. It picks a random bio from `bios_list.txt` and updates it on your profile, handling authentication (login + session persistence) along the way.

## Features

- **Random bio rotation** — picks a fresh headline from your list every run
- **Session persistence** — saves browser state (cookies/local storage) so you only log in once
- **Human verification** — asks for explicit confirmation before making changes
- **Manual login fallback** — if auto-login fails, you get 40 seconds to log in manually
- **Headed browser mode** — watch the automation happen in real-time (disable with `headless=True`)

## How it works

The script runs as a single-shot automation pipeline:

1. Load bios from `bios_list.txt`
2. Ask for user confirmation (`Type 'yes' to confirm`)
3. Launch Chromium browser
4. Check for saved browser state (session persistence)
   - If state exists → load cookies, skip login
   - If no state → perform login flow
5. Navigate to LinkedIn profile edit page
6. Pick a random bio and update the headline
7. Save updated browser state for next run
8. Close browser

## Tech stack

| Layer                  | Technology    | Purpose                                    |
| ---------------------- | ------------- | ------------------------------------------ |
| **Core Language**      | Python 3.12+  | Automation logic and credential management |
| **Browser Automation** | Playwright    | Headed Chromium automation for LinkedIn    |
| **Environment**        | python-dotenv | Loads credentials from `secrets.env`       |

## Prerequisites

- Python 3.12+
- A LinkedIn account
- Playwright browsers installed

## Installation

1. Clone or navigate to the project directory:

   ```bash
   cd CODING/linkedin_bio_swapper
   ```

2. Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   # or
   pip install playwright python-dotenv
   ```

4. Install Playwright browsers:

   ```bash
   playwright install
   ```

## Setup

1. **Add your LinkedIn credentials** to `secrets.env`:

   ```env
   LINKEDIN_USERNAME=your_username
   EMAIL=your_email
   LINKEDIN_PASSWORD=your_password
   ```

2. **Add your bios** to `bios_list.txt` — one bio per line. The script picks one at random each run.

3. **Run the script:**

   ```bash
   python main.py
   ```

   _(Wait for the browser to open, confirm with `yes`, and watch the magic happen.)_

## Project Structure

```
linkedin_bio_swapper/
├── main.py              # Main automation script
├── bios_list.txt        # List of bios/headlines to rotate
├── secrets.env          # LinkedIn credentials (do NOT commit)
├── pyproject.toml       # Project metadata & dependencies
├── README.md            # This file
└── playwright/
    └── .auth/
        └── state.json   # Saved browser session state
```

## Notes & Warnings

- **Do not commit `secrets.env`** — it contains your LinkedIn credentials. Add it to `.gitignore`.
- The saved browser state (`playwright/.auth/state.json`) contains session cookies. Keep it private.
- LinkedIn may detect automation. Use responsibly and at your own risk.
- The `headless=False` setting means you'll see the browser open. Set it to `True` for background runs.

## What's next

- [ ] Schedule automatic runs via cron or a scheduler
- [ ] Add a CLI flag to preview bios before applying
- [ ] Export current headline before overwriting
- [ ] Support multiple profile fields (About, Experience, etc.)
- [ ] Add a web dashboard to manage bios and view history

---

<div align="center">

don't rage at the game, play it • 🤷🏽‍♂️

_Happy swapping._

</div>
