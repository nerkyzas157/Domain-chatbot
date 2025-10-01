from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
import os
from dotenv import load_dotenv

load_dotenv()

async def call_domain_agent(user_input: str) -> str:
    tld_mcp_path = os.path.abspath("mcp_dir/tld_mcp.py")
    domain_mcp_path = os.path.abspath("mcp_dir/domain_mcp.py")

    client = MultiServerMCPClient(
        {
            "Internal_TLD_Check": {
                "transport": "stdio",
                "command": "python",
                "args": [tld_mcp_path],
            },
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
        tools,
    )
    
    SYSTEM_PROMPT = f"""
    ## You are a Domain Availability Agent.  

    ## You have access to two tools:  
    1. **TLD Checker** - verifies whether a TLD is supported in the system.  
    - Returns an array of supported TLDs.
    2. **Domain Availability Checker** - checks if a domain is available.  
    - Returns a key-value map of available and not available domains.

    ## Your task:  
    1. First, check if the TLDs are supported with **TLD Checker**.  
    - If it's not supported respond: "Sorry, the TLD is not supported in our system." in your response, replace TLD with the provided TLDs. Stop there and do not call **Domain Availability Checker**.  
    - If supported respond: "Yes, TLDs are supported." in your response, replace TLD with the provided TLDs. Proceed to step 2.  

    2. Check if the full domain is available with **Domain Availability Checker**.  
    - If the domain is not available respond: "The domain is taken." in your response, replace domain with the provided domains. 
    - If available respond: "The domain is available!"  in your response, replace domain with the provided domains. 

    ## Response requirements:  
    - Always confirm the TLD status first.  
    - Only report domain availability if the TLD is supported.  
    - Keep the response simple and clear.  

    The user question: {user_input}
    """
    
    response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": SYSTEM_PROMPT}]}
    )

    return response
