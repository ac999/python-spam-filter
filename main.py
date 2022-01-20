import argparse
import csv
from bs4 import BeautifulSoup
import os
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
import pickle

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

# def train(path: str, create_dataset = False) -> None:
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
    df_data = df[['Spam', 'Content']]
    df_x = df_data['Content']
    df_y = df_data['Spam']
    corpus = df_x
    cv = CountVectorizer()
    X = cv.fit_transform(corpus)

    X_train, X_test, y_train, y_test = train_test_split(X, df_y, test_size=0.32, random_state=42)

    clf = MultinomialNB()
    clf.fit(X_train,y_train)

    print("Accuracy of Model",clf.score(X_test,y_test)*100,"%")

    clf.predict(X_test)

    comment = ["Check this out I will be giving 50% offer on your first purchase"]
    vect = cv.transform(comment).toarray()

    print(clf.predict(vect))

    pkl_clf_export=('naive_bayes_clf.pkl')
    with open (pkl_clf_export, 'wb') as pklExport:
        pickle.dump(clf, pklExport)
    pkl_cv_export=('naive_bayes_cv.pkl')
    with open (pkl_cv_export, 'wb') as pklExport:
        pickle.dump(cv, pklExport)

def write_to_file(file_path, content):
    try:
        with open(file_path, 'a') as file:
            file.write(content+'\n')
    except Exception as e:
        print(e)
        print("Couldn't write to file {}".format(file_path))
        exit(1)

def scan(directory: str, output_file: str) -> None:
    infected={0: "|cln", 1: "|inf"}
    try:
        if not os.path.isdir(directory):
            print('{} is not a directory'.format(directory))
            exit(1)
    except Exception as e:
        print(e)
        exit(1)

    try:
        with open ('naive_bayes_clf.pkl', 'rb') as pklImport:
            clf = pickle.load(pklImport)
    except Exception as e:
        print("Couldn't import 'naive_bayes_clf.pkl'. Make sure it is in the same directory you are running.")
        print("Make sure sklearn is installed correctly.")
        exit(1)
    try:
        with open ('naive_bayes_cv.pkl', 'rb') as pklImport:
            cv = pickle.load(pklImport)
    except Exception as e:
        print("Couldn't import 'naive_bayes_cv.pkl'. Make sure it is in the same directory you are running.")
        print("Couldn't load CountVectorizer(). Maybe sklearn not installed correctly.")
        exit(1)
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):
            try:
                file_content = read_file(file_path)
                vect = cv.transform([file_content]).toarray()
                write_to_file(
                    output_file,
                    file + infected.get(clf.predict(vect)[0])
                )
            except Exception as e:
                print('test')
                print(e)
                exit(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='[SSOSM] Spam Filter')
    parser.add_argument('-info', nargs = 1, type = str,
        help = "<output_file> to write project info.py")
    parser.add_argument('-scan', nargs = 2, type = str,
        help = "<folder> <output_file>")
    # parser.add_argument('-train', nargs = 1, type =str)
    args = parser.parse_args()
    if args.info:
        print_info(args.info[0])
    if args.scan:
        scan(args.scan[0], args.scan[1])
    # if args.train:
    #     train(args.train[0])
