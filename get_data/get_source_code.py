import asyncio
import pandas as pd
import json
import aiohttp
import os
from dotenv import load_dotenv
from utils.dict_utils import find_content_in_dict
from utils.rate_limiter import check_limit

async def etherscan_calls_main(eth_tokens_df):
    token_contracts_df = pd.DataFrame(columns=['Token', 'Language', 'Contract Code'])
    # Process the addresses in batches of 5
    counter = 0
    token_contract_addresses = eth_tokens_df["contract"]
    for i in range(0, len(token_contract_addresses), 5):
        batch = token_contract_addresses[i:i+5]
        results = await process_batch(batch)
        counter += 1
        if not counter % 100:
            print("We have gone through these tokens ", counter)
        # Append results to the DataFrame
        for language, token, contract_code in results:
            # if token == '0x21413c119b0c11c5d96ae1bd328917bc5c8ed67e':
                # print(contract_code)
            token_contracts_df.loc[len(token_contracts_df)] = [token, language, contract_code]

        # Wait for 1 second before the next batch to respect the rate limit
        await asyncio.sleep(1)

    return token_contracts_df


async def process_batch(batch):
    tasks = []
    for address in batch:
        check_limit()  # Enforce rate limit before each call
        task = get_source_code(address)
        tasks.append(task)
    results = await asyncio.gather(*tasks)
    return results


async def get_source_code(token_address):
    
    # Load the environment variables from the .env file
    load_dotenv()

    etherscan_api_key = os.getenv('ETHERSCAN_API_KEY')
    source_code_endpoint = f"https://api.etherscan.io/api?module=contract&action=getsourcecode&address={token_address}&apikey={etherscan_api_key}"

    async with aiohttp.ClientSession() as session:
        async with session.get(source_code_endpoint) as response:
            if response.status == 200:
                data = await response.text()
                source_code = json.loads(data)['result'][0]["SourceCode"]
                
                if "from vyper" in source_code:
                    print("")
                    return ["Vyper", token_address, source_code]
                
                else:
                    contract_content_sol = source_code
                    if source_code == '':
                        print(token_address)
                        
                    elif source_code[0] == '{':
                        try: 
                            json_stripped = json.loads(source_code[1:-1])
                            standard_solidity_input = find_content_in_dict(json_stripped)
                            if standard_solidity_input:
                                contract_content_sol = standard_solidity_input
                        except:
                            pass
                    return ["Solidity", token_address, contract_content_sol]
            else:
                print("Got another type of response, ", response.status)
                # Handle non-200 responses here
                return None






