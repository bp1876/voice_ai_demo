# Production notes (quick + CTO-grade)

This repo is a **demo** of a real-time Voice AI pipeline:

**Streaming STT (Deepgram)** → **LLM (OpenAI)** → **Streaming TTS (Cartesia)**, running as a LiveKit Agent participant.

## What this demonstrates
- Realtime, low-latency conversational loop
- Streaming speech recognition and synthesis
- A simple **appointment booking** flow with a structured payload output

## Latency + reliability considerations
- **STT latency**: depends on audio conditions and network RTT. Prefer strong mic signal + stable network.
- **LLM latency**: can dominate end-to-end time for longer turns. Keep prompts concise; consider smaller models where acceptable.
- **TTS latency**: depends on voice/model choice and chunking. Streaming helps “time-to-first-audio”.

## Failure modes + mitigations
- **STT dropouts** (network/packet loss): surface a short apology and ask the user to repeat.
- **Provider timeouts**: add retry/backoff at the provider layer (not implemented in this demo).
- **Hallucinated confirmations**: require the agent to repeat captured fields and ask for confirmation.

## Observability (minimum)
Log these per session:
- session id / room name
- turn start/end timestamps
- STT partial/final events (count + duration)
- LLM request latency + token usage
- TTS time-to-first-audio, total audio duration
- any booking payloads

## Secrets hygiene
- Keep `.env.local` out of git.
- Never commit API keys.
