import pandas as pd
import os

def open_csv():
    csv_dfs = []
    for filename in os.listdir('csv'):
        path = './csv/' + filename
        df = pd.read_csv(path)
        print(f"Adding {filename} with shape {len(df)}")
        csv_dfs.append(df)

    full_csv = pd.concat(csv_dfs)
    full_csv.to_csv('./output/full_articles.csv', index=False)

def main():
    open_csv()

if __name__ == '__main__':
    main()