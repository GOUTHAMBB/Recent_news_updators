# 🚀 Automated Tech Intelligence Dashboard

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![GitHub Actions](https://img.shields.io/badge/Automation-GitHub%20Actions-2088FF.svg)
![Status](https://img.shields.io/badge/Status-Live-success.svg)

A fully automated "News Agent" that scrapes, filters, and curates high-relevance tech news every morning. The system uses GitHub Actions to run Python scripts on a schedule, fetching data via the NewsAPI, and updating a static HTML dashboard hosted on GitHub Pages.

🔗 **Live Dashboard:** [View the Daily Updates Here](https://gouthambb.github.io/Recent_news_updators/)

---

## 🛠️ How It Works (Architecture)

This project operates as a **self-sustaining intelligence loop**:

1.  **Trigger:** Every day at **08:00 UTC**, a GitHub Action workflow wakes up.
2.  **Execution:** It spins up a remote server, installs Python dependencies, and runs the `news_script.py`.
3.  **Intelligence Gathering:**
    * The script queries the **NewsAPI** for 3 specific sectors: **AI**, **AdTech**, and **Tech Mergers**.
    * **Smart Filtering:** It restricts results to a curated list of ~60 high-trust domains (e.g., TechCrunch, Reuters, MIT) to eliminate clickbait.
    * **Relevance Sorting:** It prioritizes articles based on keyword density and recency (last 48 hours).
4.  **Deployment:** The script saves the fresh data as JSON files, commits them to the repository, and GitHub Pages automatically serves the updated dashboard.

---

## 📂 Project Structure

```text
├── .github/workflows
│   └── daily_update.yml   # The automation timer (Cron job)
├── news_script.py         # The core logic (Fetching & filtering)
├── index.html             # The frontend dashboard
├── news_ai.json           # Live data store for AI news
├── news_adtech.json       # Live data store for AdTech
├── news_mergers.json      # Live data store for Mergers
└── requirements.txt       # Python dependencies
