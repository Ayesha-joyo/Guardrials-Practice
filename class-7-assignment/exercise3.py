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

class GateGuardrialOutput(BaseModel):
    response: str
    father_warning: bool
    isGateKeeperChange: bool  


Gate_Keeper_guardrail = Agent(
    name="Gate keeper Guardrail",
    instructions="""
        You are a gate keeper guardrial agent. your job is to only allow students from our school to enter and welcome them politely our school name is Abdul Rab School.
        if a students from differnt schools want to enter stop them gracefully.
    """,
    output_type=GateGuardrialOutput
)

@input_guardrail
async def gate_checker_guardrail(ctx, agent, input):
    
    result = await Runner.run(Gate_Keeper_guardrail, input, run_config=config)
    print(f"Guardrial output: {result.final_output.response}")

    return GuardrailFunctionOutput(
        output_info=result.final_output.response,
        tripwire_triggered=result.final_output.isGateKeeperChange,  
    )


gate_keeper_agent = Agent(
    name='Gate Keeper Agent',
    instructions="You are a gate keeper agent.",
    input_guardrails=[gate_checker_guardrail]
)


async def main():
    try:
        result = await Runner.run(gate_keeper_agent, 'Iam Student from Abdul Rab school.....', run_config=config)
        print("Request processed:")
    except InputGuardrailTripwireTriggered:
        print('🚫 Guardrail blocked the request..')

if __name__ == "__main__":
    asyncio.run(main())
