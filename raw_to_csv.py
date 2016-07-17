import pandas as pd
import json
import argparse

def get_df(filename):
    with open(filename) as f:
        data = f.readlines()
        data = [i.strip() for i in data]
        data_2 = [json.loads(line) for line in data]
    dataframe = pd.DataFrame(data_2)
    return dataframe.drop_duplicates('link')



def change_url(string):
    if string.startswith('//'):
        return string[2::]
    else:
        return string

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_file', type=str, default='data/artists.json',
                       help='data containing raw file')
    parser.add_argument('--save_file', type=str, default='data/cleaned_data.csv',
                           help='data file to save')
    args = parser.parse_args()

    df = get_df(args.data_file)
    df.link = df.link.apply(change_url)
    df.to_csv(args.save_file)
    print ('saved file')



if __name__ == '__main__':
    main()
