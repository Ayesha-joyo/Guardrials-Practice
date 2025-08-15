from dotenv import load_dotenv
import os
from agents import AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig

# Load environment variables
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

# Check if the API key is present
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please add it to your .env file.")

# Create an AsyncOpenAI client for Gemini
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Set up the Gemini model
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client,
)

# RunConfig for the agent
config = RunConfig(
    model=model,
    model_provider=external_client
)
