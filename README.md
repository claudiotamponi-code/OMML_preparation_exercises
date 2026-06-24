# OMML Quiz App

An interactive quiz app for studying **Optimization Methods for Machine Learning (OMML)** based on questions extracted from past exam PDFs.

## How it works

Open `omml_quiz.html` directly in a browser — no server or installation needed.

The app presents multiple-choice and true/false questions organized by exam source. Key features:

- **Filters** — filter by exam source or question type (multiple choice / true-false)
- **Shuffle** — randomize question order for varied practice
- **Progress saving** — answers are saved in `localStorage` and restored on refresh
- **Wrong answers review** — a dedicated mode to repeat only questions you got wrong
- **Da rivedere** (Bookmarks) — flag any question to review later; a filter lets you practice bookmarked questions only

Questions are grouped when they share the same dataset or network context, so related sub-questions always appear together.

## Disclaimer

> **This app is an unofficial study tool and may contain errors.**
>
> Questions and answers were extracted and adapted from past OMML exam PDFs. Some answers may be incorrect, incomplete, or reflect a specific interpretation of the material. Always cross-check with official course materials, textbooks, and your professor's solutions.
>
> Use at your own risk. No guarantee of correctness is provided.

## Usage

1. Clone or download the repository
2. Open `omml_quiz.html` in any modern browser
3. Select a filter (optional) and start answering

KaTeX for math rendering is loaded from a CDN — an internet connection is needed for formulas to render correctly.
