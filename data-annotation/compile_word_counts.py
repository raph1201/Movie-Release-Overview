import argparse, json
import pandas as pd

'''
RULES:
- Get most common words for each of the six ponies (Twilight Sparkle, Applejack, Rarity, Fluttershy, Pinkie Pie, Rainbow Dash)
- Ignore lines with multiple ponies/approximate characters (Future Twilight Sparkle, Twilight and Rarity)
- Remove stop words (the, of, ...)
- Case insensitive (Apple = apple)
- Replace ( ) [ ] , - . ? ! : ; # & with space
'''

# Define hyper parameters
LABELS = ['Actors', 'Movie Review', 'Production', 'Scorsese', 'Financial Performance', 'Themes Covered', 'Other Movies', 'Unrelated']
PUNCTUATION = ['(', ')', '[', ']', ',', '-', '.', '?', '!', ':', ';', '#', '&']

# Get arguments from command line 
def get_args():
    parser = argparse.ArgumentParser(description='Extracts data from a file and saves it as a TSV')
    parser.add_argument('-o', '--output_file', help='Output file', required=True, type=str)
    parser.add_argument('-c', '--csv', help='CSV', required=True, type=str)
    return parser.parse_args()

# Removes Caps & Special Char
def normalize_line(line):
    # Iterate through each word
    for i in line:
        # CAPS --> Lower Case
        line = line.replace(i, i.lower())

        # Check if special char & Replace 
        if i in PUNCTUATION:
            line = line.replace(i, ' ')
    return line


# Get word count for each pony
def get_word_count(input_file):
    # STEP 1: Load dataframe
    df = pd.read_csv(input_file)

    # STEP 2: Create word dictionary
    word_count = {'Actors': {},
                  'Movie Review': {},
                  'Production': {}, 
                  'Scorsese': {}, 
                  'Financial Performance': {}, 
                  'Themes Covered': {}, 
                  'Other Movies': {}, 
                  'Unrelated': {}}

    # STEP 3: Iterate through each line of dataframe
    for i in range(len(df.index)):
        
        topic = df['Topics'][i]
        title = df['Title'][i]
        descripiton = df['Description'][i]

        print(f"{i}.")
        print(topic)
        print(title)
        print(descripiton)
        print()

        # Remove CAPS and Special char
        if pd.isna(title):
            title = ""
        else:
            title = normalize_line(title)

        if pd.isna(descripiton):
            descripiton = ""
        else:
            descripiton = normalize_line(df['Description'][i])

        # Split line
        words = title.split() + descripiton.split()

        # If word not in dict, init to 1. Else increment count of word.
        for word in words:
            # Only include words with only aplhanumeric values (letters)
            if word.isalnum():
                if word not in word_count[topic]:
                    word_count[topic][word] = 1
                else:
                    word_count[topic][word] += 1

    return word_count

# Remove stopwords
def prune_word_count(dict):
    # Store words from file to list
    stopwords = []
    with open("stopword.txt", "r") as f:
        for word in f:
            word = word.replace('\n', '')
            stopwords.append(word)

    # Iterate through each word of each pony
    for topic in dict:
        for word in dict[topic].copy():
            if word in stopwords:
                del dict[topic][word]

    return dict
    
    
def main(input_file, output_file):
    word_count = get_word_count(input_file)
    word_count_pruned = prune_word_count(word_count)

    # Write to JSON file
    with open(f'{output_file}', 'w') as f:
        json.dump(word_count_pruned, f, indent=4)

if __name__ == '__main__':
    args = get_args()
    main(args.csv, args.output_file)