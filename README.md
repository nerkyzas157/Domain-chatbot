# Domain Chat Bot with MCP Agents

This chatbot was built with **Model Context Protocol (MCP) agents**. The system allows structured, context-aware conversations where multiple specialized agents interact via MCP to produce accurate and coherent responses.

---

## Table of Contents

- [Overview](#overview)  
- [Setup Instructions](#setup-instructions)  
- [Agents and MCP Tools](#agents-and-mcp-tools)  
- [Limitations](#limitations)  
- [Example Conversations](#example-conversations)  
- [Further documentation](#further-documentation)  
- [License](#license)  

---

## Overview

The Domain Chat Bot leverages **MCP agents**, which are modular components that communicate via the **Model Context Protocol** to share reasoning and collaborate on responses. MCP defines a structured way for agents to exchange information, ensuring that each agent can contribute effectively to the user needs.

Key features:

- Simple yet elegant LangChain setup
- Streamlit frontend
- Multi-agent collaboration within a single container  
- Easily extendable with new domain or other type of agents  
- Example workflows and queries included  

---

## Setup Instructions

Follow these steps to set up the project:

1. **Clone the repository**  
```bash
git clone https://github.com/nerkyzas157/Domain-chatbot.git
cd Domain-chatbot
```

2. **Configure environment variables**
Create a .env file in the root directory with necessary keys:
```ini
OPENAI_API_KEY=your_api_key_here
HOSTINGER_API_KEY=your_api_key_here
WHOIS_API_KEY=your_api_key_here
```

3. **Build and run the container**
```bash
docker-compose up --build
```
This will:
- Build the Docker image for the chatbot
- Start a single container running all MCP agents
- Expose the chatbot interface as configured

4. **Access the chatbot**  
[HERE](http://localhost:8501/)
Adjust port and/or set domain if there is a need.

5. **Stop the container**
```bash
docker-compose down
```

## Agents and MCP Tools

Inside the single container, the chatbot contains two LangChain-OpenAI MCP agents, each responsible for different tools and reasoning tasks.


### Agents

* **Domain Availability Agent**  
    Set up on GPT-4.1 for it's attention to prompt details.  
    Uses two MCP tools:  
    * Internal TLD Check Tool → checks if the TLD is supported in our system (e.g., .com , .ai ).  
    * Global Availability Check Tool → checks if the full domain (like example.com ) is available globally through Hostinger or WhoisJSON API.  


* **Domain Suggestions Agent**  
    Set up on GPT-4.1 for it's attention to prompt details.  
    Suggests 3–5 alternative domains based on a keywords.  
    Uses one MCP tool to chech generated domain availability:  
    * Global Availability Check Tool → checks if the full domain (like example.com ) is available globally through Hostinger or WhoisJSON API.

* **Routing Agent**  
    Set up on GPT-4.1-nano for it's price to quality ratio.  
    Routes user query based on its context, to an agent with ability to handle it.

### MCP Tools

MCP (Model Context Protocol) tools allow agents to:

* Check if TLDs are supported internally by reading a text file and comparing its content with user inputed TLDs.

* Check if domain names are available globally by calling Hostinger global domain avilability API endpoint. If Hostinger API fails, re-routes to WhoisJSON API.

## Limitations

Hostinger API endpoint has rate limit of 10 requests per minute. 
If WhoisJSON API client is not set up, message responses regarding domain availability will fail.  
WhoisJSON API provides only a month long free trial.  
  
Context memory is not saved for continuous conversation. Due to this reason, follow-up questions are not possible.  

## Example Conversations

Example 1: Supported TLD and Available
```makefile
User: Is startupzone.com available?
Bot: Yes, the .com TLD is supported. The domain startupzone.com is taken.
```

Example 2: Supported TLD but Taken
```makefile
User: Is faststartup.ai available?
Bot: Yes, .ai is supported. The domain faststartup.ai is available!
```

Example 3: Unsupported TLD
```makefile
User: Is mycooldomain.xyzabc available?
Bot: Sorry, the TLD xyzabc is not supported in our system.
```

Example 4: Domain Suggestions
```makefile
User: Suggest me some domains for hobby shop
Bot: Here are some suggestions:
    - hobbycrate.net
    - hobbyvault.org
    - hobbybazaar.net
    - craftycorner.biz
    - pastimeplace.net
```

## Further documentation
[Hostinger API](https://developers.hostinger.com/#tag/domains-availability)

[WhoisJSON API](https://www.whoisjson.com/documentation)

[LangChain MCP](https://docs.langchain.com/oss/python/langchain/mcp)

[Streamlit](https://docs.streamlit.io/develop/tutorials/chat-and-llm-apps/build-conversational-apps)

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---
