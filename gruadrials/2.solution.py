import asyncio
import os

from dotenv import load_dotenv, find_dotenv
from pydantic import BaseModel

from agents import (
    Agent,    
    GuardrailFunctionOutput,
    OutputGuardrailTripwireTriggered , 
    RunContextWrapper,
    Runner,
    set_tracing_disabled ,
    AsyncOpenAI
    ,OpenAIChatCompletionsModel,
    TResponseInputItem,
    output_guardrail,
)



async def main():
    load_dotenv(find_dotenv())
    gemini_api_key: str | None = os.environ.get("GOOGLE_API_KEY")

    set_tracing_disabled(disabled=True)
    external_client: AsyncOpenAI = AsyncOpenAI(api_key=gemini_api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
    llm_provider : OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(model='gemini-2.5-flash', openai_client=external_client)
    
    class MessageOutput(BaseModel): 
         response: str

    class SensitivityCheck(BaseModel): 
        contains_sensitive_info: bool
        reasoning: str
        confidence_level: int  # 1-10 scale
    
    sensitivity_guardrail_agent = Agent(
        name="Privacy Guardian",
        instructions="""
        Check if the response contains:
        - Personal information (SSN, addresses, phone numbers)
        - Internal company information
        - Confidential data
        - Inappropriate personal details
        
        Be thorough but not overly sensitive to normal business information.
        """,
        output_type=SensitivityCheck,
        model= llm_provider
    )

    @output_guardrail
    async def privacy_guardrail(  
        ctx: RunContextWrapper, 
        agent: Agent, 
        output: MessageOutput
    ) -> GuardrailFunctionOutput:
        # Check the agent's response for sensitive content
        result = await Runner.run(
            sensitivity_guardrail_agent, 
            f"Please analyze this customer service response: {output.response}", 
            context=ctx.context
        )
        
        return GuardrailFunctionOutput(
            output_info=result.final_output,
            tripwire_triggered=result.final_output.contains_sensitive_info,
        )

# Main customer support agent with output guardrail
    support_agent = Agent( 
        name="Customer Support Agent",
        instructions="Help customers with their questions. Be friendly and informative.",
        output_guardrails=[privacy_guardrail],  # Add our privacy check
        output_type=MessageOutput,
        model= llm_provider
    )

    async def test_privacy_protection():
        try:
            # This might generate a response with sensitive info
            result = await Runner.run(
                support_agent, 
                "What's my account status for john.doe@email.com?"
            )
            print(f"✅ Response approved: {result.final_output.response}")
        
        except OutputGuardrailTripwireTriggered as e:
            print("🛑 Response blocked - contained sensitive information!")
            # Send a generic response instead
            fallback_message = "I apologize, but I need to verify your identity before sharing account details."
    
    await test_privacy_protection()

if __name__  == "__main__":
    asyncio.run(main())

