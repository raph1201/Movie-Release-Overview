import json
import pandas as pd

def main():
    with open("./output/flower_moon_full.json", "r") as f:
        data = json.load(f)

    df = pd.DataFrame(columns=['title', 'description', 'content'])
    df['title'] = [article['title'] for article in data['articles']]
    df['description'] = [article['description'] for article in data['articles']]
    df['content'] = [article['content'] for article in data['articles']]

    df.to_csv('./output/flower_moon_raph.csv', index=False)

if __name__ == '__main__':
    main()