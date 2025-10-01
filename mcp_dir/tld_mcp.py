from mcp.server.fastmcp import FastMCP
import os

mcp = FastMCP("Internal_TLD_Check")

    
@mcp.tool()
def tld_check(tlds: list) -> list:
    """Checks if provided TLDs are supported internally and returns a list of supported TLDs."""
    
    if tlds:
        # correcting TLDs by adding "." in front
        for idx, val in enumerate(tlds):
            if '.' != val[0]:
                temp_tld = ''.join(char for char in val if char.isalpha())
                tlds[idx] = '.' + temp_tld
        
        # Loading valid TDL list
        base_dir = os.path.dirname(__file__)
        file_path = os.path.join(base_dir, "supported_tlds.txt")
        with open(file_path, 'r') as f:
            VALID_TLDS = set(line.strip().lower() for line in f)
            
        tlds = set(map(str.lower, tlds))
        
        return list(tlds & VALID_TLDS)
    else:
        return []

if __name__ == "__main__":
    mcp.run(transport="stdio")