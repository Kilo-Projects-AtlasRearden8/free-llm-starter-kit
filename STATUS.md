# STATUS

Free LLM Starter Kit — Markdown docs + static HTML site for starting with
local LLMs. Built by Asdale Dynamics, LLC.

## What was built

| Item | Path | Purpose |
|------|------|---------|
| License | `LICENSE` | MIT License, copyright line exactly `Copyright (c) 2026 Asdale Dynamics, LLC` |
| Readme | `README.md` | Kit overview, credits Asdale Dynamics, LLC |
| Getting started | `docs/getting-started.md` | What local LLMs are, hardware needed, how to begin |
| Model cards | `docs/model-cards.md` | Beginner model recommendations (TinyLlama 1.1B, Llama 3.2 3B, Llama 3.1 8B, Llama 3.1 70B Q4_K_M, Nomic Embed Text) with RAM guidance and Ollama commands |
| Ollama cheat sheet | `docs/ollama-cheatsheet.md` | Install, run, manage models — copy-paste commands for macOS/Linux/Windows |
| Prompt starters | `docs/prompt-starters.md` | Copy-paste prompts for writing, learning, admin, healthcare-worker aids (education only), and fun |
| Privacy basics | `docs/privacy-basics.md` | What stays on your machine, safe habits, limits of local privacy |
| Build script | `scripts/build_site.py` | Pure stdlib Python: Markdown -> static HTML site, no external deps |
| Static site | `site/*.html` | Built HTML output: index + 5 guides + license page, with nav and CSS |
| Tests | `tests/test_build.py` | 11 unittest tests: build exit code, page generation, required content, link resolution, HTML parsing, credits/copyright, no secret patterns |
| This file | `STATUS.md` | Build, run, verification, gaps |

No account, no API key, no secrets or personal data in any file. No `.github/workflows`. Credits Asdale Dynamics, LLC in README and in site footer; exact MIT copyright line in LICENSE.

## How to run it

```bash
# Build the static HTML site from the Markdown docs
python3 scripts/build_site.py

# Open the site in your browser
# Linux:
xdg-open site/index.html
# macOS:
open site/index.html
# Windows:
start site/index.html
```

The build needs only Python 3 (standard library). Output goes to `site/`. Open `site/index.html` — no server, no internet, no account required after the build.

The Markdown docs under `docs/` can also be read directly.

## Verification results

- `python3 scripts/build_site.py` exits 0 and builds 7 pages:
  `index.html`, `getting-started.html`, `model-cards.html`,
  `ollama-cheatsheet.html`, `prompt-starters.html`, `privacy-basics.html`,
  `LICENSE.html`
- `python3 -m unittest discover -s tests -v`: **11 tests, 11 failures: 0, errors: 0, OK**
  - build exits cleanly
  - all expected pages generated
  - required content present on each page (model names, Ollama commands, credits)
  - all navigation links resolve to existing files
  - generated HTML parses
  - tables and code blocks render
  - LICENSE contains exact line `Copyright (c) 2026 Asdale Dynamics, LLC`
  - README credits Asdale Dynamics, LLC
  - no secret/key patterns in any Markdown file
- Ollama itself is not installed in this environment, so `ollama run` commands were not executed end-to-end. The cheat sheet documents the commands; verify them by installing Ollama from ollama.com and running `ollama run llama3.2`.

## Known gaps

- Ollama end-to-end behavior not tested here (Ollama not installed in this build environment).
- Site is plain static HTML: no search, no dark mode, no JavaScript.
- Model recommendations reflect public specifications, not benchmarks run on specific hardware.
- Only one model should be run at a time; running multiple models multiplies RAM use.
- Local AI keeps chats on your machine, but it does not by itself satisfy healthcare regulatory requirements (HIPAA, etc.); see Privacy Basics.
