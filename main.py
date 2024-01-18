import asyncio
import pandas as pd
from get_data.get_data_local import import_data_local
from get_data.get_source_code import etherscan_calls_main


async def main(cache = True):
    token_data_path = "/Users/antoine/Merkle/RugPullDetection/data/tokens_v4.csv"
    token_contracts_cache = "/Users/antoine/Merkle/RugPullDetection/data/token_contracts.csv"
    
    token_meta_df = import_data_local(token_data_path)
    eth_tokens_df = token_meta_df[token_meta_df["chainId"] == 1]
       
    # Get the current event loop and run the main coroutine
    if cache == False:
        all_contracts = await etherscan_calls_main(eth_tokens_df)
    else:
        all_contracts = pd.read_csv(token_contracts_cache)

    # clean_data()

    # all_contracts.to_csv('./data/token_contracts.csv', index=False)


    # Your DataFrame is now populated
    print("Finished going over etherscan contracts")

if __name__ == "__main__":
    asyncio.run(main())