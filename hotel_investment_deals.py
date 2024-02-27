import pandas as pd
import requests
import os

#excel_file = "Deals_New.xlsx"
#df = pd.read_excel(excel_file)

download_dir = "Deals_downloads"

if not os.path.exists(download_dir):
    os.makedirs(download_dir)


def download_file():
    for index, row in df.iterrows():
        url = row["Link"]
        filename = f"file_{index}.xlsx"
        response = requests.get(url)

        if response.status_code == 200:
            with open(os.path.join(download_dir, filename), 'wb') as f:
                f.write(response.content)
                print(f"Download success, file: {filename}")
        else:
            print(f"Unable to download, file: {filename}")

#concatenate file

def join_excel_files():
    dfs = []
    all_files = [file for file in os.listdir(download_dir) if file.endswith('.xlsx')]

    for file in all_files:
        try:
            df = pd.read_excel(os.path.join(download_dir, file))
            dfs.append(df)
            print(f"Read {file} successfuly")
        except Exception as e:
            print(f"Error reading {file}: {str(e)}")

    combined_df = pd.concat(dfs, ignore_index=True)
    combined_df.to_excel("Master_Excel_deals.xlsx", index=False)

#download_file()
join_excel_files()
