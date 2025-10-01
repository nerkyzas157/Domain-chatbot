from mcp.server.fastmcp import FastMCP
import http.client
import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP("Global_Availability_Check_Tool")

HOSTINGER_API_KEY = os.getenv("HOSTINGER_API_KEY")
WHOIS_API_KEY = os.getenv("WHOIS_API_KEY")


def whois_domain_check(domains: list, tlds_input: list) -> dict:
    '''Checks global domain availability on WhoisJSON servers. \n
    Option B if Hostinger fails.'''

    response = {'available_domains':[], 'unavailable_domains':[]}  
    
    url = "https://whoisjson.com/api/v1/whois"
    whois_headers = {
        "Authorization": f"Token={WHOIS_API_KEY}"
    }
    for d in domains:
        for t in tlds_input:
            params = {
                "domain": d + t
            }

            resp = requests.get(url, headers=whois_headers, params=params)
            resp.raise_for_status()
            data = resp.json()
            
            if not data['registered']:
                    response['available_domains'].append(data['name'])
                    break
            else:
                    response['unavailable_domains'].append(data['name'])
        return response


@mcp.tool()
def domain_check(domains: list, tlds_input: list) -> dict:
    """Checks if provided domains are globally available. Returns a dict of available and not available domains."""
    
    # Verifying and correcting hallucinated domains inputs
    for idx, val in enumerate(domains):
        if '.' in val:
            domains[idx] = val.split('.')[0]
    
    
    # Loading valid TDL list
    base_dir = os.path.dirname(__file__)
    file_path = os.path.join(base_dir, "supported_tlds.txt")
    with open(file_path, "r") as f:
        VALID_TLDS = list(line.strip().lower() for line in f)
    
    
    if tlds_input:
        # correcting TLDs by adding "." in front
        for idx, val in enumerate(tlds_input):
            if '.' != val[0]:
                temp_tld = ''.join(char for char in val if char.isalpha())
                tlds_input[idx] = '.' + temp_tld
    
        tlds_set = set(map(str.lower, tlds_input))
        tlds = list(tlds_set & set(VALID_TLDS))
    else:
        tlds = VALID_TLDS
    
    
    conn = http.client.HTTPSConnection("developers.hostinger.com")
    hostinger_headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {HOSTINGER_API_KEY}"
    }
    
    response = {'available_domains':[], 'unavailable_domains':[]}  
      
    for d in domains:
        payload = {"domain": d, "tlds": tlds, "with_alternatives": False}
        payload_bytes = json.dumps(payload).encode("utf-8")
        conn.request("POST", "/api/domains/v1/availability", payload_bytes, hostinger_headers)
        res = conn.getresponse()
        data = res.read()
        response_temp = json.loads(data.decode("utf-8"))
        
        
        # API error handling
        try:
            if 'errors' in response_temp.keys():
                return whois_domain_check(domains, tlds) # re-routing to WhoisJSON API
        except AttributeError:
            for i in response_temp:
                if 'errors' in i.keys():
                    return whois_domain_check(domains, tlds)# re-routing to WhoisJSON API
        
        if type(response_temp) == dict: # an error or too many attempts response
            return whois_domain_check(domains, tlds) # re-routing to WhoisJSON API
        
        
        for i in response_temp:
            if i['is_available']:
                response['available_domains'].append(i['domain'])
            else:
                response['unavailable_domains'].append(i['domain'])
        
    return response


if __name__ == "__main__":
    mcp.run(transport="stdio")