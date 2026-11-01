# Getting Started with Local LLMs

## What is a local LLM?

A large language model (LLM) is a program that reads and writes text in a way that feels conversational. Most people meet LLMs through websites that require an account and a subscription. A **local LLM** runs on your own computer instead. Nothing you type leaves your machine, and you never need an account or an API key.

## Why run models locally

- **Privacy:** Your chats stay on your computer. They are not uploaded to a company's servers.
- **No account needed:** No signup, no email, no credit card.
- **No per-token cost:** Once a model is downloaded, using it is free.
- **Works offline:** After downloading a model, you can chat without internet access.
- **You stay in control:** You can delete a model anytime, and no one can change it out from under you.

## What you need

### Computer

Any modern laptop or desktop will work. The main thing that matters is **RAM** (memory), not a fancy graphics card.

| RAM | What you can run |
|-----|------------------|
| 8 GB | Small models (1–3 billion parameters). Good for trying it out. |
| 16 GB | Medium models (7–8 billion parameters). Good for everyday writing and admin. |
| 32 GB+ | Larger models (14–32 billion parameters). Better reasoning, slower on older machines. |

### Disk space

Models are files. A small model is about 2–5 GB. A medium model is about 4–9 GB. Budget at least 20 GB of free space so you can try a few.

### No special hardware required

You do not need a powerful GPU. Models run on your CPU, though a graphics card can make them faster. Start with what you have.

## How this kit works

1. **Pick a model** from [Model Cards](model-cards.md) that fits your computer's RAM.
2. **Install Ollama** using the [Ollama Setup Cheat Sheet](ollama-cheatsheet.md).
3. **Download and run** your model with one command.
4. **Chat** using a prompt from [Prompt Starters](prompt-starters.md).
5. **Read [Privacy Basics](privacy-basics.md)** so you know exactly what stays on your machine.

## Your first chat, in plain English

Think of a local LLM as a very well-read assistant with no memory of your personal life unless you tell it something. You type a message (a **prompt**), the model reads it, and replies. The model does not "know" you, does not remember last week's chat unless you paste it back in, and cannot see your files unless you copy text into the chat window.

## If something feels hard

You are not behind. Everyone starts with one command. If a step does not work, re-read it slowly, copy the command exactly, and try again. This kit is written for humans, not experts.

---

*Asdale Dynamics, LLC — beginner-friendly AI education. Credit: Asdale Dynamics, LLC.*
