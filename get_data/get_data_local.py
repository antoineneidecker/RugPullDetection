import pandas as pd

def import_data_local(file_path):
    # Read the CSV file into a DataFrame
    token_meta_df = pd.read_csv(file_path)
    token_meta_df['createdAt'] = pd.to_datetime(token_meta_df['createdAt'])
    token_meta_df = token_meta_df.replace('Unknown', 'NaN')
    token_meta_df[['decimals']] = token_meta_df[['decimals']].astype(int)
    token_meta_df[['decimals', 'totalSupply']] = token_meta_df[['decimals', 'totalSupply']].astype(float)

    return token_meta_df