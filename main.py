import argparse
import csv
from bs4 import BeautifulSoup
import os
import pandas as pd

project_info = ["[SSOSM] Spam Filter\n",
        "Andrei Cristian\n",
        "andreicristian6@protonmail.com\n",
        "v.0.1\n"]

def print_info(path: str) -> None:
    try:
        file = open(path, "w")
        file.writelines(project_info)
        file.close()
    except Exception as e:
        print(e)
        print(f"Couldn't write to {path}")
        exit(1)

def is_html(content: str) -> bool:
    html=False
    try:
        html=bool(BeautifulSoup(content, "html.parser").find())
    except Exception as e:
        print(e)
        return False
    return html

def extract_from_html(content: str) -> str:
    try:
        soup = BeautifulSoup(content, features='lxml')
        return ''.join(soup.findAll(text=True))
    except Exception as e:
        print(e)
        exit(1)

def read_file(path: str) -> str:
    try:
        file_content = open(path, 'r', encoding='utf-8', errors='ignore').read()
        if is_html(file_content):
            file_content = extract_from_html(file_content)
        return file_content
    except Exception as e:
        print(e)
        exit(1)

def create_csv(path: str) -> bool:
    fields = ['Spam', 'Content']
    try:
        with open(path, 'w') as csvFile:
            csvWriter = csv.writer(csvFile)
            csvWriter.writerow(fields)
        return True
    except Exception as e:
        print(e)
        return False

def write_to_csv(path: str, spam: bool, content: str) -> bool:
    try:
        with open(path, 'a', newline='') as csvFile:
            csvWriter = csv.writer(csvFile)
            csvWriter.writerow([int(spam), content])
            return True
    except Exception as e:
        print(e)
        return False

def train(path: str, create_dataset = False):
    if create_dataset:
        create_csv('dataset.csv')
        lots = ['Lot1', 'Lot2']
        category = ['Clean','Spam']
        for lot in lots:
            for classification in category:
                directory = os.path.join(path, lot, classification)
                files = os.listdir(directory)
                for file in files:
                    file_path = os.path.join(directory, file)
                    if os.path.isfile(file_path):
                        file_content = read_file(file_path)
                        if not write_to_csv('dataset.csv', classification=='Spam', file_content):
                            print(file_content)
    df = pd.read_csv('dataset.csv')
    print(df.size)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='[SSOSM] Spam Filter')
    parser.add_argument('-info', nargs = 1, type = str,
        help = "<output_file> to write project info.py")
    parser.add_argument('-scan', nargs = 2, type = str,
        help = "<folder> <output_file>")
    parser.add_argument('-train', nargs = 1, type =str)
    args = parser.parse_args()
    if args.info:
        print_info(args.info[0])
    if args.train:
        train(args.train[0])
