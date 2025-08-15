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

class StudentOutput(BaseModel):
    response: str
    isClassTimingChange: bool  


student_assistant_guardrail = Agent(
    name="Student Assistant Guardrail",
    instructions="""
        You are a student assistant whose job is to check if the student is requesting 
        a change to their class timings. If yes, set isClassTimingChange = true.
        Otherwise, set it to false.
    """,
    output_type=StudentOutput
)

@input_guardrail
async def class_timing_guardrail(ctx, agent, input):
    
    result = await Runner.run(student_assistant_guardrail, input, run_config=config)
    rich.print(result.final_output)

    return GuardrailFunctionOutput(
        output_info=result.final_output.response,
        tripwire_triggered=result.final_output.isClassTimingChange  # True means block
    )


student_agent = Agent(
    name='Student Agent',
    instructions="You are a  student agent.",
    input_guardrails=[class_timing_guardrail]
)

# Main runner
async def main():
    try:
        result = await Runner.run(student_agent, 'I want to change my class timings 😭😭', run_config=config)
        print("Request processed:", result)
    except InputGuardrailTripwireTriggered:
        print('🚫 Guardrail blocked the request..')

if __name__ == "__main__":
    asyncio.run(main())
