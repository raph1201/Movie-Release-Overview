import json, random

def sort_removed(data1, data2):
    to_remove_1 = []
    articles_1 = data1['articles']

    for i in range(0, len(articles_1)):
        if articles_1[i]['title'] == "[Removed]":
            to_remove_1.append(i)

    articles_1 = [item for index, item in enumerate(articles_1) if index not in to_remove_1]
    data1['articles'] = articles_1

    to_remove_2 = []
    articles_2 = data2['articles']

    for j in range(0, len(articles_2)):
        if articles_2[j]['title'] == "[Removed]":
            to_remove_2.append(j)

    articles_2 = [item for index, item in enumerate(articles_2) if index not in to_remove_2]
    data2['articles'] = articles_2

    return data1, data2


def sort_same(articles_list):
    to_remove = []

    for i in range(0, len(articles_list)):
        for j in range(i+1, len(articles_list)):
            if articles_list[i]['title'] == articles_list[j]['title'] and j not in to_remove:
                to_remove.append(j)

    articles_list = [item for index, item in enumerate(articles_list) if index not in to_remove]
    
    return articles_list


def merge_and_sample(data1, data2, sample_size):
    merged_data = {}
    merged_data['status'] = data1['status']
    merged_data['totalResults'] = sample_size

    articles_list = data1['articles'] + data2['articles']
    articles_list_sorted = sort_same(articles_list)

    merged_data['articles'] = articles_list_sorted[:125]
    return merged_data


def main():
    with open("./output/flower_moon_a.json", "r") as f:
        data1 = json.load(f)

    with open("./output/flower_moon_b.json", "r") as f:
        data2 = json.load(f)

    data1, data2 = sort_removed(data1, data2)
    dataset = merge_and_sample(data1, data2, 125)

    with open("./output/flower_moon_full_2.json", "w") as f:
        json.dump(dataset, f, indent=4)

if __name__ == '__main__':
    main()