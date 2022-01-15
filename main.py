import argparse
from bs4 import BeautifulSoup

project_info = ["[SSOSM] Spam Filter\n",
        "Andrei Cristian\n",
        "andreicristian6@protonmail.com\n",
        "v.0.1\n"]

def print_info(path) -> None:
    try:
        file = open(path, "w")
        file.writelines(project_info)
        file.close()
    except Exception as e:
        print(e)
        print(f"Couldn't write to {path}")
        exit(1)

def is_html(content) -> bool:
    html=False
    try:
        html=bool(BeautifulSoup(content, "html.parser").find())
    except Exceptions as e:
        print(e)
        exit(1)
    return html

def extract_from_html(content) -> str:
    try:
        soup = BeautifulSoup(content)
        return ''.join(soup.findAll(text=True))
    except Exception as e:
        print(e)
        exit(1)
    
def main():

    print_info("./info.txt")

if __name__ == '__main__':
    main()
