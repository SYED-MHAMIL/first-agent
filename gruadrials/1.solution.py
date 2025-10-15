import asyncio
import os

from dotenv import load_dotenv, find_dotenv
from pydantic import BaseModel

from agents import (
    Agent,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    set_tracing_disabled ,
    AsyncOpenAI
    ,OpenAIChatCompletionsModel,
    TResponseInputItem,
    input_guardrail,
)



async def main():
    load_dotenv(find_dotenv())
    gemini_api_key: str | None = os.environ.get("GOOGLE_API_KEY")

    set_tracing_disabled(disabled=True)
    external_client: AsyncOpenAI = AsyncOpenAI(api_key=gemini_api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
    llm_provider : OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(model='gemini-2.5-flash', openai_client=external_client)

    class MathHomeworkOutput(BaseModel):
        is_math_homework: bool
        reasoning: str
    
    guardrail_agent = Agent( 
    name="Homework Police",
    instructions="Check if the user is asking you to do their math homework.",
    output_type=MathHomeworkOutput,
    model=llm_provider
    )
    

    @input_guardrail
    async def math_guardrail( 
    ctx: RunContextWrapper[None], 
    agent: Agent, 
    input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
       # Run our checking agent
       result = await Runner.run(guardrail_agent, input, context=ctx.context)
    
       # Return the result with tripwire status
       return GuardrailFunctionOutput(
            output_info=result.final_output, 
            tripwire_triggered=result.final_output.is_math_homework,  # Trigger if homework detected
       )    
    
    
    # Main agent with guardrail attached
    customer_support_agent = Agent(  
    name="Customer Support Specialist",
    instructions="You are a helpful customer support agent for our software company.",
    input_guardrails=[math_guardrail],  # Attach our guardrail
     model= llm_provider
     )

    async def test_homework_detection():
     try:
        # This should trigger the guardrail
        await Runner.run(customer_support_agent, "Can you solve 2x + 3 = 11 for x?")
        print("❌ Guardrail failed - homework request got through!")
    
     except InputGuardrailTripwireTriggered:
        print("✅ Success! Homework request was blocked.")
        # Handle appropriately - maybe send a polite rejection message
    await test_homework_detection()


if __name__  == "__main__":
    asyncio.run(main())
