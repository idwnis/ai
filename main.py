import asyncio
from dotenv import load_dotenv
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, llm
from livekit.agents.voice_assistant import VoiceAssistant
from livekit.plugins import openai, silero
from api import CustomAssistantFunctions  # Updated name for the imported class

# Load environment variables
load_dotenv()


async def main_entry(ctx: JobContext):
    """
    Main entry point for the voice assistant worker.
    Initializes the assistant and connects it to the audio stream.
    """
    # Define the initial chat context for the assistant
    assistant_context = llm.ChatContext().append(
        role="system",
        text=(
            "You are a smart voice assistant designed to interact with users through voice. "
            "Provide brief, clear, and concise responses, avoiding complex or unpronounceable punctuation."
        ),
    )

    # Connect to the room with audio-only auto subscription
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    # Load custom assistant functions
    functions_context = CustomAssistantFunctions()

    # Initialize the voice assistant with components
    assistant = VoiceAssistant(
        vad=silero.VAD.load(),       # Voice activity detection
        stt=openai.STT(),           # Speech-to-text
        llm=openai.LLM(),           # Language model
        tts=openai.TTS(),           # Text-to-speech
        chat_ctx=assistant_context, # Chat context
        fnc_ctx=functions_context,  # Function context
    )

    # Start the assistant in the current room
    assistant.start(ctx.room)

    # Greet the user
    await asyncio.sleep(1)
    await assistant.say("Hello! How can I assist you today?", allow_interruptions=True)


if __name__ == "__main__":
    # Run the application using the LiveKit CLI
    cli.run_app(WorkerOptions(entrypoint_fnc=main_entry))
