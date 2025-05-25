import urllib.request
import bs4
from bs4 import BeautifulSoup

def check_dynamic(text: str) -> bool:
    return len(text.replace("\n", "")) < (len(text) * 0.9)

def delete_all(tag_name: str, document: BeautifulSoup) -> None:
    tags = document.find_all(tag_name)
    for tag in tags:
        tag.decompose()


def find_main_body(html: BeautifulSoup | bs4.PageElement, original_length: int, distribution_ratio: int = 0.9) -> str:
    text_lengths = []

    for child in list(html.children):
        text_lengths.append(len(child.text))

    passes = list(filter(lambda x: x > (original_length*distribution_ratio), text_lengths))
    if len(passes) > 0:
        return find_main_body(list(html.children)[text_lengths.index(max(passes))], original_length)

    else:
        return html.text


def scrape(link):

    del_list = ["script", "style", "head", "iframe", "nav", "header", "footer"]
    try:
        raw = urllib.request.urlopen(link.replace("%3A", ":").replace("%2F", "/"))
        html = BeautifulSoup(raw, "html.parser")
    
        for item in del_list:
            delete_all(item, html)
        text = find_main_body(html, len(html.text))
    
        if check_dynamic(text):
            text = link
    except:
        print("Error processing raw ", link, " - falling back to gemini google search")
        text = link
    
    return text


