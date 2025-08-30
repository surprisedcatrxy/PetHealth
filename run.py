print("loading...\n")

from Agent import agent
import asyncio

def main():
    
    asyncio.run(agent.run_agent(input("query:\n").replace('\\','/',100)))

if __name__ == "__main__":
    main()


