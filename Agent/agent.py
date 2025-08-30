import os
from dotenv import load_dotenv
import asyncio

load_dotenv()
API_KEY=os.getenv("API_KEY")

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import Swarm
from autogen_agentchat.conditions import HandoffTermination, TextMentionTermination
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.messages import HandoffMessage

from MCP import mcp_client

model_client = OpenAIChatCompletionClient(
    model="deepseek-chat", 
    api_key=API_KEY,
    base_url="https://api.deepseek.com",
    model_info={
        "family": "unknown",
        "function_calling": True,
        "json_output": False,
        "multiple_system_messages": True,
        "structured_output": True,
        "vision": False,
    },
)

def call_mcp_vital_sign(temp_c: float | None, hr: int | None, steps: int | None, intake_g: float | None, species: str = "dog"):
    results=asyncio.run(mcp_client.call_mcp_vital_sign(temp_c=temp_c,hr=hr,steps=steps,intake_g=intake_g,species=species))
    return results

def call_mcp_vision(path:str):
    results=asyncio.run(mcp_client.call_mcp_vision(path=path))
    return results

def call_mcp_rag(context:str):
    results=asyncio.run(mcp_client.rag(context=context))
    return results

general_agent=AssistantAgent(
    "general_agent",
    model_client=model_client,
    handoffs=["vital_sign_agent","vision_agent","rag_agent"],
    system_message="""
    You are a pet health status analyst who coordinates the status analysis by entrusting a professional agent.
    -vision_agent: Responsible for analyzing pet species and health status through pictures
    -vital_sign_agent: Responsible for analyzing the health status (body temperature, heart rate, number of steps, daily food intake) through the pet's vital signs.
    -rag_agent: Responsible for enhancing retrieval by collating all information using the knowledge base
    Always handoff to a single agent at a time.
    dont contain right parameters ,dont handoff to other agents.
    dont ask user!once the task complete ,use TERMINATE.
    use TERMINATE when analyse is complete."""
)

vital_sign_agent=AssistantAgent(
    "vital_sign_agent",
    model_client=model_client,
    tools=[call_mcp_vital_sign],
    handoffs=["general_agent"],
    system_message="""
    You are a pet vital signs analyst.
    check whether there are any features in body temperature, heart rate, step count, daily intake, species, 
    if so, must use the call_mcp_vital_sign tool, do not pass the parameters that do not exist.
    if not any features or parameter,handoff back to general_agent directly.
    And analyze the results, always handoff back to general_agent after completion
    dont ask user!
    """
)

vision_agent=AssistantAgent(
    "vision_agent",
    model_client=model_client,
    tools=[call_mcp_vision],
    handoffs=["general_agent"],
    system_message="""
    You are a health analyst based on pet pictures.
    If there is an address for the image,must use call_mcp_vision tool.
    Organize the returned results of MCP.
    if not any picture,handoff back to general_agent directly.
    Always handoff back to general_agent after completing a task.
    dont ask user!
    """
)


rag_agent=AssistantAgent(
    "rag_agent",
    model_client=model_client,
    tools=[call_mcp_rag],
    handoffs=["general_agent"],
    system_message="""
    You're a pet health analyst with contextual knowledge base augmented searches
    After organizing the context, you must use call_mcp_rag tools to search the knowledge base and organize and analyze the results
    if not any context,handoff back to general_agent directly.
    Always handoff back to general_agent after completing a task.
    dont ask user!
    """
)

text_termination = TextMentionTermination("TERMINATE")
termination = text_termination

analyse_team = Swarm(
    participants=[general_agent,vital_sign_agent, vision_agent, rag_agent], termination_condition=termination
)

async def run_agent(query:str) -> None:
    results=await Console(analyse_team.run_stream(task=query))
