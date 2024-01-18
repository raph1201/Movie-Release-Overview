import json, requests
from datetime import date
import argparse

'''
TASK

GOAL:
Collect 125 articles from the NewsAPI.org about the movie Killers of the Flower Moon.

PARAMETERS:
API_KEY and QUERY STRING are hard coded into the script. Change them before running the script.
'''

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~ ARGPARSE ~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def get_args():
    parser = argparse.ArgumentParser(description='Collect articles from NewsAPI.org')
    parser.add_argument('-o', '--output_file', type=str, help='Query string for NewsAPI.org')
    args = parser.parse_args()
    return args

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~ HYPER-PARAMETERS ~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
API_KEY = 'd2abbe0513984b9b9482468339ca750b'

#NEWS_QUERY_URL = "https://newsapi.org/v2/everything?qInTitle={}&from={}&to={}&language=en&apiKey={}"   # Search by keywords in title
NEWS_QUERY_URL = "https://newsapi.org/v2/everything?q={}&from={}&to={}&language=en&apiKey={}"           # Search by keywords in title and body

#QUERY_STRING = "Doona AND (Yang Se-jong OR Bae Suzy OR Lee Jung-hyo)"
QUERY_STRING = "\"Killers of the Flower Moon\" -movie -niro -dicaprio -scorsese -fraser -oscar"

START_DATE_1 = date(2023, 10, 31)       # October 31, 2023
END_DATE_1 = date(2023, 11, 2)          # November 2, 2023

START_DATE_2 = date(2023, 11, 3)        # November 3, 2023
END_DATE_2 = date(2023, 11, 6)          # November 6, 2023

START_DATE_3 = date(2023, 11, 7)        # November 5, 2023
END_DATE_3 = date(2023, 12, 7)          # December 5, 2023

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~ FUNCTIONS ~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Takes QUERY_STRING and makes it readable by NewsAPI.org
def format_string(string):
    for i in string:
        if i == " ":
            string = string.replace(i, "%20")
    return string

# Function to fetch news from newsapi.org
def fetch_latest_news(output_file):
    query_formatted = format_string(QUERY_STRING)

    # Generate HTTP request
    query_string = NEWS_QUERY_URL.format(query_formatted, START_DATE_3, END_DATE_3, API_KEY)

    # Send HTTP request
    response = requests.get(query_string)

    if response.status_code != 200:
        raise Exception('Error fetching news from newsapi.org')
    
    data = response.json()

    # Dump data is external file for analysis
    with open(f'coverage/{output_file}.json', 'w') as f:
        json.dump(data, f, indent=4)

    # Return list of dictionaries for each article 
    return data["articles"]

# Main
def main():
    args = get_args()
    fetch_latest_news(args.output_file)

# Usage: python3 article_collector.py -o output_file
if __name__ == '__main__':
    main()
