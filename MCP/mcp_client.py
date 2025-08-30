import asyncio
from fastmcp import FastMCP, Client

from MCP import mcp_server  

client=Client(mcp_server.mcp)

async def call_mcp_vital_sign(temp_c: float | None, hr: int | None, steps: int | None, intake_g: float | None, species: str = "dog"):
    async with client:
        results=await client.call_tool("pet_check",{"temp_c": temp_c,"hr": hr,"steps": steps,"intake_g": intake_g,"species": species })
        return results

async def call_mcp_vision(path:str|None):
    async with client:
        results=await client.call_tool("pet_vision",{"path": path })
        return results

async def call_mcp_rag(context:str|None):
    async with client:
        results=await client.call_tool("pet_rag",{"context": context})
        return results