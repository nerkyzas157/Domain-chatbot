from openai import AsyncOpenAI
from agent_dir.domain_agent import call_domain_agent
from agent_dir.suggestion_agent import call_suggestion_agent

from dotenv import load_dotenv

load_dotenv()
client = AsyncOpenAI()

agents = {
    "domain_availability_agent": call_domain_agent,
    "domain_suggestions_agent": call_suggestion_agent,
}

async def llm_route(user_input: str) -> str:
    """Use LLM to decide which agent should handle the user query."""
    system_prompt = """
    ## You are a routing agent.
    
    ## You have 2 agents available:
    - domain_availability_agent: checks global availability of domains
    - domain_suggestions_agent: suggests domain names

    When given a user query, respond ONLY with the agent name that should handle it:
    'domain_availability_agent' OR 'domain_suggestions_agent'.
    If neither applies, ask user for clarification. 

    **Do not** respond to any other questions. Your sole task is to define which agent to call.
    """

    response = await client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input},
        ],
    )

    return response.choices[0].message.content.strip()

async def routing_agent(user_input: str):
    """Main router agent logic."""
    agent_name = (await llm_route(user_input)).lower()

    if agent_name not in agents:
        return agent_name

    call_agent = agents[agent_name]
    response = await call_agent(user_input)
    
    return response["messages"][-1].content
