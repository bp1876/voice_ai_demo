# Voice AI Agent Demo (Track 2: Deepgram + Cartesia + OpenAI)

I implemented the appointment-booking flow, added logging + payload output, and wrote production notes on latency/failures/observability.

This repo is a practical demo I can show in a CTO/fractional CTO hiring process:

- **Streaming STT:** Deepgram
- **LLM:** OpenAI (Responses API)
- **Streaming TTS:** Cartesia
- **Realtime transport + rooms:** LiveKit Cloud (Agents)

The agent includes a small **home services appointment booking** flow and prints a structured payload when details are collected.

## Requirements
- Python **3.10–3.13** (LiveKit Agents requirement)
- A LiveKit Cloud project + API keys
- API keys for Deepgram, Cartesia, and OpenAI (Track 2 plugins)

> Note on cost: provider accounts may require billing (especially OpenAI). You can keep this demo cheap by keeping sessions short and using small models.

---

## Quick start (Fedora / Linux)

### 1) Create a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2) Install dependencies
```bash
pip install -U pip
pip install -r requirements.txt
```

### 3) Configure environment
Copy `.env.example` to `.env.local` and fill in your keys:
```bash
cp .env.example .env.local
nano .env.local
```

### 4) Download required model files
This downloads local assets used by the VAD/turn detector/noise cancellation.
```bash
python agent.py download-files
```

### 5) Run (console mode)
Talk to the agent directly from your terminal:
```bash
python agent.py console
```

### 6) Run (dev mode) + use the Playground
To connect from the LiveKit Agents Playground:
```bash
python agent.py dev
```

---

## What to show an employer (fast)
1) Run `python agent.py dev`
2) Open the LiveKit Agents Playground
3) Ask to book an appointment
4) Show the console line:
   - `BOOKING_PAYLOAD={...}`

See `demo_script.md` for a tight video script.

---

## Files
- `agent.py` – LiveKit Agent + Deepgram/OpenAI/Cartesia pipeline
- `production_notes.md` – CTO-grade production considerations
- `demo_script.md` – simple recording flow
