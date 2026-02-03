from __future__ import annotations

from dotenv import load_dotenv

from livekit import agents, rtc
from livekit.agents import AgentServer, AgentSession, Agent, room_io
from livekit.plugins import noise_cancellation, silero, deepgram, cartesia, openai
from livekit.plugins.turn_detector.multilingual import MultilingualModel


load_dotenv(".env.local")

ASSISTANT_INSTRUCTIONS = """You are a helpful voice AI assistant for a home services company (HVAC / plumbing / electrical).

Your job:
- Answer questions briefly and clearly.
- If the user wants to BOOK an appointment, run the Booking Flow.

Booking Flow:
1) Confirm the service type (HVAC/plumbing/electrical) and a short description of the issue.
2) Ask for ZIP code.
3) Ask for preferred date.
4) Ask for a time window (e.g., morning/afternoon/evening or 2-hour window).
5) Ask for name and phone number.
6) Repeat the captured details and ask for confirmation.
7) After confirmation, output ONE line exactly:
   BOOKING_PAYLOAD=<compact JSON>
   The JSON keys must be: intent, service_type, issue, zip, date, time_window, name, phone, created_utc.
8) Then verbally confirm the appointment is "requested" (not guaranteed) and that someone will follow up.

Rules:
- Keep responses short; avoid emojis and special formatting.
- If the user changes their mind, stop the flow and ask what they'd like instead.
"""


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions=ASSISTANT_INSTRUCTIONS)


server = AgentServer()


@server.rtc_session()
async def voice_agent(ctx: agents.JobContext) -> None:
    # Connect to the LiveKit room first.
    await ctx.connect()

    # Track 2: explicit provider plugins.
    session = AgentSession(
        stt=deepgram.STTv2(
            model="nova-3",
            eager_eot_threshold=0.4,
        ),
        llm=openai.responses.LLM(
            model="gpt-4o-mini",
        ),
        tts=cartesia.TTS(
            model="sonic-3",
            voice="f786b574-daa5-4673-aa0c-cbe3e8534c02",
        ),
        vad=silero.VAD.load(),
        turn_detection=MultilingualModel(),
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_options=room_io.RoomOptions(
            audio_input=room_io.AudioInputOptions(
                noise_cancellation=lambda params: (
                    noise_cancellation.BVCTelephony()
                    if params.participant.kind
                    == rtc.ParticipantKind.PARTICIPANT_KIND_SIP
                    else noise_cancellation.BVC()
                ),
            ),
        ),
    )

    # Initial greeting.
    await session.generate_reply(
        instructions="Greet the user and offer your assistance."
    )


if __name__ == "__main__":
    agents.cli.run_app(server)
