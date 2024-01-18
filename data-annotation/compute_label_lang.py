import argparse, json, math, collections, itertools
import pandas as pd

# Get arguments from command line 
def get_args():
    parser = argparse.ArgumentParser(description='Extracts data from a file and saves it as a TSV')
    parser.add_argument('-i', '--input_json', help='Input JSON', required=True, type=str)
    parser.add_argument('-o', '--output_file', help='Output file', required=True, type=str)
    return parser.parse_args()

# Calculate tf-idf of word
def tf_idf(word, label, dict):
    return tf(word, dict[label]) * idf(word, dict)

# Calculate tf of word
def tf(word, label_dict):
    return label_dict[word]

# Calculate idf of word
def idf(word, dict):
    num_labels = len(dict)
    num_labels_using_word = 0
    for pony in dict:
        for w in dict[pony]:
            if word == w:
                num_labels_using_word += 1
                break

    if num_labels_using_word == 0:
        return 0
    else: 
        return math.log(num_labels/num_labels_using_word)


# Get TF-IDF Score for each word of each pony
def get_word_tf_idf(dict):
    word_dict = dict

    for label in dict:
        for word in dict[label]:
            word_dict[label][word] = tf_idf(word, label, dict)
    
    return word_dict

# Sort each words by tf-idf score from lowest to highest
def get_sorted_tf_idf(dict):
    for label in dict:
        sorted_x = sorted(dict[label].items(), key=lambda kv: kv[1], reverse=True)
        dict[label] = collections.OrderedDict(sorted_x)
    return dict

# Keep N words with best tf-idf score
def get_top_tf_idf(dictionary, n):
    top_dict = {}
    for label in dictionary:
        top_words = dict(list(dictionary[label].items())[:n])
        top_dict[label] = top_words
    return top_dict

def main(input_file, output_file):
    # Open file from task 1
    with open(f'{input_file}', 'r') as f:
        label_dict = json.load(f)

    word_dict = get_word_tf_idf(label_dict)

    sorted_tf_idf = get_sorted_tf_idf(word_dict)

    # Write sorted tf-idf words to JSON file
    with open('td-idf.json', 'w') as f:
        json.dump(sorted_tf_idf, f, indent=4)

    top_tf_idf = get_top_tf_idf(sorted_tf_idf, 10)

    # Write 10 best tf-idf words JSON file
    with open(output_file, 'w') as f:
        json.dump(top_tf_idf, f, indent=4)
    

if __name__ == '__main__':
    args = get_args()
    main(args.input_json, args.output_file)