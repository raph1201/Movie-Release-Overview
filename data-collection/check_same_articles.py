import json

def main():
    with open("./output/flower_moon_full_2.json", "r") as f:
        data = json.load(f)

    same = 0
    for i in range(0, 125):
        for j in range(i+1, 125):
            if data['articles'][i]['title'] == data['articles'][j]['title']:
                same += 1
                print(data['articles'][i]['title'])
                print(data['articles'][j]['title'])
                print()
    print(f"Same: {same}")

if __name__ == '__main__':
    main()