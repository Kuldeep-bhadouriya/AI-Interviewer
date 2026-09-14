import logging
import os

from dotenv import load_dotenv

from livekit import agents, rtc
from livekit.agents import AgentServer, AgentSession, Agent, room_io
from livekit.plugins import groq, noise_cancellation, silero, simli
from livekit.plugins.turn_detector.multilingual import MultilingualModel

load_dotenv(".env.local")

logger = logging.getLogger("my-agent")


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions=(
                "Your name is Maya and you are an interview coach specializing in behavioral interviews. "
                "Keep all responses short and conversational since this is a voice interaction. "
                "No formatting, bullet points, emojis, or special characters.\n\n"
                "Your workflow:\n"
                "1. Start by asking what role or industry the user is preparing for.\n"
                "2. Ask one behavioral interview question at a time. Begin with moderate difficulty.\n"
                "3. After the user answers, give brief constructive feedback. "
                "Note what they did well and one thing to improve. "
                "Coach them using the STAR method: Situation, Task, Action, Result. "
                "If they missed a STAR element, point out which one and suggest how to add it.\n"
                "4. Adapt difficulty based on performance. If they nail it, ask a harder or more nuanced question. "
                "If they struggle, simplify or offer a hint before moving on.\n"
                "5. Occasionally summarize patterns you notice across multiple answers.\n\n"
                "Be encouraging but honest. Act like a supportive coach, not a judge. "
                "Keep feedback to two or three sentences, then move to the next question."
            ),
        )


server = AgentServer()


@server.rtc_session(agent_name="my-agent")
async def my_agent(ctx: agents.JobContext):
    session = AgentSession(
        stt="deepgram/nova-3:multi",
        # llama-3.1-8b-instant was decommissioned by Groq on 2026-08-16 (404 model_not_found).
        # Current production replacement: openai/gpt-oss-20b
        llm=groq.LLM(model="openai/gpt-oss-20b"),
        tts="cartesia/sonic-3:9626c31c-bec5-4cca-baa8-f8ba9e84c8bc",
        vad=silero.VAD.load(),
        turn_detection=MultilingualModel(),
    )

    simli_api_key = os.getenv("SIMLI_API_KEY")
    simli_face_id = os.getenv("SIMLI_FACE_ID")
    if simli_api_key and simli_face_id:
        avatar = simli.AvatarSession(
            simli_config=simli.SimliConfig(
                api_key=simli_api_key,
                face_id=simli_face_id,
            ),
            avatar_participant_name="maya-avatar",
        )

        await avatar.start(session, room=ctx.room)
    else:
        logger.warning(
            "SIMLI_API_KEY / SIMLI_FACE_ID not set - running without avatar. "
            "Set them in .env.local to enable the Simli avatar."
        )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_options=room_io.RoomOptions(
            audio_input=room_io.AudioInputOptions(
                noise_cancellation=lambda params: noise_cancellation.BVCTelephony()
                if params.participant.kind == rtc.ParticipantKind.PARTICIPANT_KIND_SIP
                else noise_cancellation.BVC(),
            ),
        ),
    )

    await session.generate_reply(
        instructions="Greet the user warmly. Introduce yourself as Maya, their interview coach. Ask what role or industry they're preparing for so you can tailor the questions."
    )


if __name__ == "__main__":
    agents.cli.run_app(server)
