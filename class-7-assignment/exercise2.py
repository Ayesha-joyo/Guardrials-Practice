import rich
import asyncio
from connection import config
from pydantic import BaseModel

from agents import (
    Agent,
    Runner,
    input_guardrail,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered
)

class FatherOutput(BaseModel):
    response: str
    father_warning: bool  


father_guardrail = Agent(
    name="Father Guardrail",
    instructions="""
        You are a father agent. your responsibility is to make sure your child does not lower the AC temperature below 26C.
        if the child tries to set the AC temperature less than 26C , you must block the request immediately.
        if the AC temperature is set to 26C or higher, you can allow the request.
    """,
    output_type=FatherOutput
)

@input_guardrail
async def check_temperature_guardrail(ctx, agent, input):
    
    result = await Runner.run(father_guardrail, input, run_config=config)
    print(f"Guardrial output: {result.final_output.response}")

    return GuardrailFunctionOutput(
        output_info=result.final_output.response,
        tripwire_triggered=result.final_output.father_warning,  
    )


father_agent = Agent(
    name='father Agent',
    instructions="You are a father agent.",
    input_guardrails=[check_temperature_guardrail]
)


async def main():
    try:
        result = await Runner.run(father_agent, 'Set AC to 24C.....', run_config=config)
        print("Request processed:")
    except InputGuardrailTripwireTriggered:
        print('🚫 Guardrail blocked the request..')

if __name__ == "__main__":
    asyncio.run(main())
