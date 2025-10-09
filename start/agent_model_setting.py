import os
from dotenv import load_dotenv
from agents import Agent,Runner,function_tool,ModelSettings,OpenAIChatCompletionsModel,AsyncOpenAI,set_tracing_disabled

# load env
load_dotenv()
# disabled to connect the openAI API tracing
set_tracing_disabled(disabled=True)
GIMINI_API_KEY = os.getenv("GOOGLE_API_KEY")  
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

external_client: AsyncOpenAI = AsyncOpenAI(api_key=GIMINI_API_KEY,base_url=BASE_URL)
model:OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(model="gemini-2.5-flash" , openai_client=external_client)


@function_tool  
def calculate_area(length:int,width: int) -> int:
    """Calculate the area of rectangle """
    area = length * width
    return area

@function_tool
def translator(text) -> str:
    """Translate any language into English """
    return text



def main():
    """ Learn model stting with simple examples"""
    # print("\n Temperature Settings")
    # print("-"*30)

    # agent_cold = Agent(
    #     name= "Cold Agent" ,
    #     instructions="You are a helpfull assistant" ,
    #     model_settings=ModelSettings(temperature =0.1),
    #     model = model                     
    # )
     
    # agent_Hot = Agent(
    #     name= "Hot Agent" ,
    #     instructions="You are a helpfull assistant" ,
    #     model_settings=ModelSettings(temperature =1.9),
    #     model = model                     
    # )
    
    # question = "Tell me about AI  in 2 sentance"

    # print("\nCold agent (temperature = 0.1):")
    # result_cold = Runner.run_sync(agent_cold,question)
    # print(result_cold.final_output)


    
    # print("\nHot agent (temperature = 0.9):")
    # result_cold = Runner.run_sync(agent_Hot,question)
    # print(result_cold.final_output)

    # #  2 Example : Tool Choice

    # print("\nTool Choice Temperature Settings")
    # print("-"*30)
    
    # agent_auto = Agent(
    #     name= "Auto" ,
    #     tools=[calculate_area] ,
    #     model_settings=ModelSettings(tool_choice ="auto"),
    #     model = model                     
    # )
     
    # agent_required = Agent(
    #     name= "Required" ,
    #     # instructions="You are a helpfull assistant" ,
    #     tools=[calculate_area] ,
    #     model_settings=ModelSettings(tool_choice="required"),
    #     model = model                     
    # )
    
    
    # agent_none = Agent(
    #     name= "None tool use" ,
    #     instructions="You cannot the use tool" ,
    #     tools=[calculate_area] ,
    #     model_settings=ModelSettings(tool_choice="none"),
    #     model = model                     
    # )
    

    # question = "What's the area of a 5x3 rectangle?"

    # print("\nAgent decison auto:")
    # result_auto = Runner.run_sync(agent_auto,question)
    # print(result_auto.final_output)


    
    # print("\nAgent must use tool :")
    # result_required = Runner.run_sync(agent_required,question)
    # print(result_required.final_output)

    
    
    # print("\nAgent will not use this tool :")
    # result_none = Runner.run_sync(agent_none,question)
    # print(result_none.final_output)


    # Example 3 : Token Setting agent

    print('\n Token and Temperature setting')
    print("-" *30)
    # Short, concise responses

    agent_brief = Agent(
    name="short Assistant",
    instructions="You are a Math tutor" ,
    model_settings=ModelSettings(max_tokens=300,temperature=0.1)
    ,model=model
    )

    # Longer, detailed responses
    # agent_detailed = Agent(
    #     name="Assistant", 
    #     instructions="You are pyhsics asistant" , 
    #     model_settings=ModelSettings(max_tokens=1000,temperature="0.1")
    #     ,model=model
    # )

    agent_creative = Agent(
    name="short Story Writer",
    instructions="You are a creative short storyteller.",
    model_settings=ModelSettings(max_tokens=200,temperature=0.9),
    model= model
)
    # question = "What is multiplication of 4x5"
    # question1 = "The Spider and the Fly"
    
    # print("\nAgent gives the brief assistment:") 
    # result_brief = Runner.run_sync(agent_brief,question)
    # print(result_brief.final_output)


    
    # print("\nAgent gives the Detailed assistment:") 
    # result_detailed = Runner.run_sync(agent_creative,question1)
    # print(result_detailed.final_output)
    


 
 


# ************************************************************* 
    # Example 4: Parallel tool calls
# ************************************************************* 


    # Agent can use multiple tools at once

    parallel_agent = Agent(
    name="Multi-tasker" , 
    tools= [calculate_area,translator],
    model_settings=ModelSettings(
        tool_choice="auto",
        # parallel_tool_calls=True , 
        max_tokens=1500
    ),
    model=model
    )

    question  = "What is the area of ​​a 5x3 rectangle?"
    result_parallel_agent =Runner.run_sync(parallel_agent,question)

    # print('\n Parallels tools run simultaneously:')
    # print(result_parallel_agent.final_output)
    
     
    #   EXAMPLES# 6
    
    # Top-P and Penalties
    
    focused_agent = Agent(
        name="Focused",
        model_settings=ModelSettings(
            temperature=0.7,
            top_p=0.3,
            # remove penalties from here 👇
        ),
        model=model
    )

    # When you actually call the model/run, pass penalties like this:
    # response = focused_agent.run(
    #     "Write a creative intro",
    #     frequency_penalty=0.5,
    #     presence_penalty=0.3
    # )
    question ="What is differnce between shall and will"
    result_focused_agent =Runner.run_sync(focused_agent,question)
    print("\n  Top-p and panalties:")
    print(result_focused_agent.final_output)



if __name__ == "__main__":
    main()