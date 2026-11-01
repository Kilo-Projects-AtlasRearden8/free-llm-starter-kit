# Privacy Basics for Local AI

## The one-sentence version

When you run a model locally, your chats stay on your computer. Nothing you type is uploaded to a company's servers, and no account or API key is needed.

## Why local is private

Most popular AI tools work like this: you type a message, it travels over the internet to a company's computer, the company processes it, and sends back an answer. That means the company can see, store, and sometimes train on what you type.

A **local LLM** works differently: the model is a file on your computer, and when you chat, your computer does all the work. The conversation never leaves your machine.

## What stays on your machine

| Stays local | Leaves your computer |
|-------------|----------------------|
| The model file you downloaded | Nothing, if you are offline |
| Every message you type | Nothing |
| Every reply the model gives | Nothing |
| Your chat history (until you delete it) | Nothing |

You can turn off Wi-Fi, unplug the ethernet cable, and keep chatting. That is the practical test of local AI: if it works without internet, your data is not going anywhere.

## What you still control

- **Deleting chats:** Clear your chat history anytime. In Ollama, start a new conversation or delete the model with `ollama rm <model>`.
- **Deleting models:** Remove a model and its file is gone from your disk.
- **No hidden training:** Local models do not send your chats back to improve someone else's product.

## What local AI does NOT protect you from

Local privacy is strong, but it is not magic:

- **Shoulder surfing:** Anyone who can see your screen can read your chats.
- **Access to your computer:** Anyone who can log into your user account can read your chat history and model files.
- **Backups:** If you back up your computer to a cloud service, your chat history may be included in that backup. Check your backup settings.
- **Mistakes and bias:** A local model can still make things up, get facts wrong, or repeat stereotypes from its training data. Treat output as a draft.
- **Healthcare privacy:** If you work in healthcare, running a model locally does not by itself make you HIPAA-compliant. Never paste real patient names, dates of birth, medical record numbers, or identifying details into any AI. These prompts are education only, never medical advice.

## Safe habits

1. **Do not paste secrets.** Passwords, credit card numbers, API keys, Social Security numbers, and other sensitive data do not belong in a chat — local or not.
2. **Do not paste real patient or client data.** Use fake examples when practicing.
3. **Lock your computer** when you step away, just like you would with any private document.
4. **Know where your backups go.** If your chat folder syncs to the cloud, so do your chats.
5. **Verify important information.** Local models hallucinate too. Double-check anything that affects money, health, or legal decisions.

## Quick privacy check

Before you start a new chat, ask:

- Am I offline right now? (Try it — the chat should still work.)
- Am I pasting anything I would not want on a billboard?
- Do I know how to delete this conversation when I am done?

If you can answer yes to all three, you are using local AI the way it was meant to be used: private, quiet, and under your control.

---

*Asdale Dynamics, LLC — beginner-friendly AI education. Credit: Asdale Dynamics, LLC. Education only, never medical advice.*
