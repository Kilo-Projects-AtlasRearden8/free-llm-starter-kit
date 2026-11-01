# Model Cards

Plain-English snapshots of local LLMs that beginners can actually run. All models listed below can be downloaded and run with Ollama — no account, no API key, no credit card required.

Parameter counts are a rough guide to size: more parameters usually means smarter replies, but also more RAM and slower responses. Quantization (the `4-bit` or `Q4_K_M` notes) shrinks the model file so it fits on your computer, with a small trade-off in quality.

## How to read these cards

- **Size:** Approximate download size and RAM needed.
- **Best for:** What the model is comfortable doing.
- **Ollama command:** Copy-paste this to download and run the model.
- **Try first if:** A quick match for your situation.

## Recommended models

### Llama 3.2 3B — the best place to start

- **Size:** About 2 GB download, roughly 4–5 GB RAM while running.
- **Best for:** Short answers, emails, summarizing, everyday questions, first-time users.
- **Ollama command:** `ollama run llama3.2`
- **Try first if:** You have 8 GB of RAM or just want to see how local AI feels.

Llama 3.2 3B is small, fast, and surprisingly capable for everyday writing and admin tasks. It is the ideal "first model."

### Llama 3.1 8B — the everyday workhorse

- **Size:** About 4.7 GB download, roughly 8–9 GB RAM while running.
- **Best for:** Writing, brainstorming, light coding help, formatting, longer conversations.
- **Ollama command:** `ollama run llama3.1`
- **Try first if:** You have 16 GB of RAM and want one model for most things.

This is the model most people stick with after trying the 3B version. It handles longer prompts and more nuanced writing well.

### Llama 3.1 70B Q4_K_M — the heavy thinker (advanced)

- **Size:** About 40 GB download, roughly 48 GB RAM while running.
- **Best for:** Complex reasoning, coding projects, detailed analysis.
- **Ollama command:** `ollama run llama3.1:70b-q4_K_M`
- **Try first if:** You have 64 GB of RAM and a model you trust already. Not recommended as a first model.

### TinyLlama 1.1B — the tiny tester

- **Size:** About 0.6 GB download, roughly 2–3 GB RAM while running.
- **Best for:** Testing on old laptops, learning how Ollama works, very simple tasks.
- **Ollama command:** `ollama run tinyllama`
- **Try first if:** Your computer is older or you want the fastest possible download.

TinyLlama is not very smart, but it runs almost anywhere. Good for confirming your setup works before downloading bigger models.

### Nomic Embed Text — for experiments, not chatting

- **Size:** About 0.3 GB download.
- **Best for:** Turning text into numbers (embeddings) for hobby projects, not conversation.
- **Ollama command:** `ollama run nomic-embed-text`
- **Try first if:** You are curious about how AI "reads" text mathematically.

This is not a chat model. Do not use it for conversation.

## Matching a model to your RAM

| Your RAM | Start with | Then try |
|----------|-----------|----------|
| 8 GB | Llama 3.2 3B | Llama 3.1 8B (one at a time) |
| 16 GB | Llama 3.1 8B | Llama 3.2 3B for quick tasks |
| 32 GB+ | Llama 3.1 8B | Llama 3.1 70B (quantized) |

Only run one model at a time. Running two models together doubles the RAM use.

## Where model files live

Ollama stores downloaded models in `~/.ollama/models` on Linux and macOS, and in the Ollama app data folder on Windows. If you need disk space back, delete a model with:

```bash
ollama rm llama3.2
```

## Model safety reminder

Local models run offline, but they can still make mistakes, invent facts, or reflect biases from their training data. Treat output as a draft, not as truth — especially for anything important.

---

*Asdale Dynamics, LLC — beginner-friendly AI education. Credit: Asdale Dynamics, LLC.*
