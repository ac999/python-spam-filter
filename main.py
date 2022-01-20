import argparse
import csv
from bs4 import BeautifulSoup
import os

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
    except Exceptions as e:
        print(e)
        exit(1)
    return html

def extract_from_html(content: str) -> str:
    try:
        soup = BeautifulSoup(content)
        return ''.join(soup.findAll(text=True))
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
        files1_clean = os.listdir('{}/Lot1/Clean' % (path))
        files1_spam = os.listdir('{}/Lot1/Spam' % (path))
        files2_clean = os.listdir('{}/Lot2/Clean' % (path))
        files2_spam = os.listdir('{}/Lot2/Spam' % (path))
        try:
            for file in files1_clean:
                if os.path.isfile(file):
                    with open(os.path.join('{}/Lot1/Clean' % (path), file), 'r') as f:
                            write_to_csv('dataset.csv', '0', ''.join(f.readlines()))
            for file in files1_spam:
                if os.path.isfile(file):
                    with open(os.path.join('{}/Lot1/Spam' % (path), file), 'r') as f:
                            write_to_csv('dataset.csv', '1', ''.join(f.readlines()))
            for file in files2_clean:
                if os.path.isfile(file):
                    with open(os.path.join('{}/Lot2/Clean' % (path), file), 'r') as f:
                            write_to_csv('dataset.csv', '0', ''.join(f.readlines()))
            for file in files2_spam:
                if os.path.isfile(file):
                    with open(os.path.join('{}/Lot2/Spam' % (path), file), 'r') as f:
                            write_to_csv('dataset.csv', '1', ''.join(f.readlines()))
        except Exception as e:
            print(e)
            exit(1)


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
        train(args.train[0], True)
