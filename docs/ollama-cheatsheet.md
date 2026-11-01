# Ollama Setup Cheat Sheet

Ollama is the free, open-source tool that downloads and runs local LLMs. Everything here is copy-paste friendly. No account, no API key, no signup.

## Step 1 — Install Ollama

### macOS

Download the app from ollama.com, or install with Homebrew:

```bash
brew install ollama
```

Then start it:

```bash
ollama serve
```

### Linux

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

The installer starts Ollama as a background service automatically.

### Windows

Download the Windows installer from ollama.com and run it. Ollama appears as a tray icon.

### Check it is running

```bash
ollama --version
```

You should see a version number. If you get "command not found," restart your terminal after installing.

---

## Step 2 — Download and run your first model

```bash
ollama run llama3.2
```

This downloads the model (about 2 GB) and opens a chat prompt. Type a message and press Enter. Type `/bye` to exit the chat.

---

## Step 3 — Common commands (copy-paste)

| Goal | Command |
|------|---------|
| List installed models | `ollama list` |
| Download a model | `ollama pull llama3.1` |
| Run (download + chat) | `ollama run llama3.1` |
| Remove a model | `ollama rm llama3.2` |
| Show model details | `ollama show llama3.1` |
| Stop the Ollama server | `Ctrl+C` in the terminal where you ran `ollama serve` |

### Show a model card in the terminal

```bash
ollama show llama3.1 --modelfile
```

This prints the recipe Ollama used to build the model — useful for learning, not required.

---

## Run a model without the chat prompt

Send one question and get one answer:

```bash
ollama run llama3.2 "Explain local AI in one sentence."
```

Great for scripts and quick tests.

---

## Keep a model running in the background

Open a terminal and run:

```bash
ollama serve
```

Leave that terminal open. In another terminal, run:

```bash
ollama run llama3.2
```

Multiple chat windows can talk to the same running model.

---

## Uninstall Ollama

### macOS (Homebrew)

```bash
brew uninstall ollama
```

### Linux

```bash
sudo rm -rf /usr/bin/ollama
rm -rf ~/.ollama
```

### Windows

Uninstall from Settings > Apps, then delete `C:\Users\<you>\.ollama` if you want to remove downloaded models.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `ollama: command not found` | Restart your terminal, or reinstall. On Linux, log out and back in. |
| Download is slow | Your internet connection, not Ollama. Try again later or pick a smaller model (Llama 3.2 3B). |
| "Not enough memory" | Pick a smaller model. Close browser tabs and other apps to free RAM. |
| Chat is slow on first reply | The first response after loading a model is slower; later replies speed up. |
| Port already in use | Another Ollama instance is running. Close it, or only run `ollama serve` once. |

---

## What Ollama does and does not do

- ✅ Downloads models and keeps them on your computer
- ✅ Runs models locally, offline capable
- ✅ Free and open source
- ❌ Is not an account or subscription service
- ❌ Does not require an API key
- ❌ Does not upload your chats

---

*Asdale Dynamics, LLC — beginner-friendly AI education. Credit: Asdale Dynamics, LLC.*
