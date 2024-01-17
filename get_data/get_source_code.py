import json
import requests
from google.colab import userdata
from utils.dict_utils import find_content_in_dict

def get_source_code(token_address):
    """
    Obtains token source code/abi and saves in json format.

    Parameters
    ----------
    token_address: str
        token address in checksum format.
    out_path : (contract, language)
        returns the code of the contract and the language it's in
    """

    source_code_endpoint = "https://api.etherscan.io/api?" \
                           "module=contract" \
                           "&action=getsourcecode" \
                           f"&address={token_address}" \
                           f"&apikey={userdata.get('etherscan_api_key')}"
    source_code = json.loads(requests.get(source_code_endpoint).text)['result'][0]["SourceCode"]
    
    if "from vyper" in source_code:
        return (source_code, "Vyper")
    
    try:
        dict_contract = json.loads(source_code[1:-1])
        contract_content = dict_contract["sources"]
        contract_content_sol = find_content_in_dict(contract_content)
        print(contract_content_sol)
        return (contract_content_sol)
    except:
        return (None, None)