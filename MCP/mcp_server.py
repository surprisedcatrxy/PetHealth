from fastmcp import FastMCP

import ollama

from MCP import check_pet_tool
from VB import vector_database

mcp=FastMCP("mcp_server")

@mcp.tool
def pet_check(temp_c: float | None, hr: int | None, steps: int | None, intake_g: float | None, species: str = "dog"):
    return check_pet_tool.health_summary(temp_c,hr,steps,intake_g,species)

@mcp.tool
def pet_vision(path:str|None):
    response = ollama.generate(
        model="qwen2.5vl:7b",
        prompt=f"I need to know the type of pet (cat/dog) in this image:path={path} and analyze the pet's health status based on the image",
        images=[path],
    )
    return response["response"]

@mcp.tool
def pet_rag(context:str|None):
    return vector_database.query(context)


if __name__ == "__main__":
    mcp.run()
