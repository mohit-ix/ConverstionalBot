from dotenv import load_dotenv

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import (
    groq,
    elevenlabs,
    noise_cancellation,
    silero,
)
from livekit.agents import metrics, MetricsCollectedEvent
import logging

load_dotenv()

class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions='''
            You are a helpful voice assistant and I want you to help me collect the following information from the user:
                - Name
                - Age
                - Highest education
                - Hobby
            You can ask for at most two things at once. And don't get distracted from the conversation.
            Remember to keep the questions precise.
            After the information is collected thank the user and end the conversation.
        ''')

# TTS model for groq is also available but it is not as good as elevenlabs and the context window is very small
async def entrypoint(ctx: agents.JobContext):
    session = AgentSession(
        stt=groq.STT(
            model="whisper-large-v3-turbo",
            language="en",
        ),
        llm=groq.LLM(model="llama-3.3-70b-versatile"),
        tts=elevenlabs.TTS(
            voice_id="cgSgspJ2msm6clMCkdW9",
            model="eleven_flash_v2_5"
        ),
        # tts=groq.TTS(
        #     model="playai-tts",
        #     voice="Arista-PlayAI",
        # ),
        vad=silero.VAD.load(),
        turn_detection="vad",
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(
            # LiveKit Cloud enhanced noise cancellation
            # - If self-hosting, omit this parameter
            # - For telephony applications, use `BVCTelephony` for best results
            noise_cancellation=noise_cancellation.BVC(), 
        ),
    )

    await ctx.connect()

    # Greetings message
    await session.generate_reply(
        instructions="Greet the user and offer your assistance."
    )

    usage_collector = metrics.UsageCollector()
    logger = logging.getLogger()

    # Collecting the metrics after every sentence is finished
    @session.on("metrics_collected")
    def _on_metrics_collected(ev: MetricsCollectedEvent):
        metrics.log_metrics(ev.metrics)
        usage_collector.collect(ev.metrics)

    async def log_usage():
        summary = usage_collector.get_summary()
        logger.info(f"Usage: {summary}")

    # At shutdown, generate and log the summary from the usage collector
    ctx.add_shutdown_callback(log_usage)


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))