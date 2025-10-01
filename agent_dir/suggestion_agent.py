from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
import os
from dotenv import load_dotenv

load_dotenv()

async def call_suggestion_agent(user_input: str) -> str:
    domain_mcp_path = os.path.abspath("mcp_dir/domain_mcp.py")
    client = MultiServerMCPClient(
        {
            "Global_Availability_Check_Tool": {
                "transport": "stdio", 
                "command": "python",
                "args": [domain_mcp_path]
            }
        }
    )

    tools = await client.get_tools()
    agent = create_agent(
        "openai:gpt-4.1",
        tools
    )
    
    SYSTEM_PROMPT = f"""
    ## You are a Domain Suggestions Agent.  

    ## You have access to:  
    1. **Domain Availability Checker** - checks if a domain is available.  
    - Returns a key-value map of available and not available domains with their TLDs.

    ## Your task:  
    1. Based on the user input, generate 3-5 creative and relevant alternative domain name suggestions **without TLDs**.  
    2. Use the Domain Availability Checker to ensure that all suggested domains are available.  
    - Do not provide TLDs to **Domain Availability Checker**, instead provide an empty array.
    - If a domain is not available, do not include it in the final response.  

    ## Response requirements:  
    - Always provide between 3 and 5 available domain suggestions.  
    - Your response must contain only the available domain names with their TIDs. 
    - Keep the response simple and clear.  
    
    ## Response structure:
    - You must start with "Here are some suggestions:"
    - List the available domains with their TLDs below the initial text. 
    
    ### Response example:
    Here are some suggestions:
     - mycoffeeshop.com
     - coffeelovers.net
     - bestcoffee.org

    The user question: {user_input}
    """
    
    response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": SYSTEM_PROMPT}]}
    )

    return response
