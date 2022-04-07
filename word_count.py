import requests
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('stopwords')
from collections import Counter
    
#URL = "https://www.geeksforgeeks.org/data-structures/"
#req = requests.get(URL)
#print(req.content)
#soup = BeautifulSoup(req.content, 'html5lib')
#print(soup.prettify())

def process_html(url):
    req = requests.get(url)
    html = req.content
    soup = BeautifulSoup(html, "html.parser")
    
    for data in soup(['style', 'script']):
        data.decompose()
        
    return ' '.join(soup.stripped_strings)


def tokenzie_text(text):
    tokenizer = nltk.RegexpTokenizer(r"\w+")
    words = tokenizer.tokenize(text)
    stop_words = stopwords.words('english')
    removing_stop_words = [w.lower() for w in words if w.lower() not in stop_words]
    return removing_stop_words


def word_count_json(url):
    text = process_html(url)
    num_words = {}
    words = tokenzie_text(text)
    counts = Counter(words)
    for w in words:
        num_words[w] = counts[w]

    sorted_dict = {}
    sorted_keys = sorted(num_words, key=num_words.get, reverse=True)  # [1, 3, 2]

    for w in sorted_keys:
        sorted_dict[w] = num_words[w]


    return sorted_dict

def scrape_for_all_links(url):
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    allText = []
    urls = []
    allText.append(process_html(url))
    urls.append(url)

    for link in soup.find_all('a'):
        href = link.get('href')
        if(href is not None and url in href and href not in urls):
            urls.append(href)
            print(href)
            allText.append(process_html(href))
    
    text = ' '.join(allText)
    num_words = {}
    words = tokenzie_text(text)
    counts = Counter(words)
    for w in words:
        num_words[w] = counts[w]

    sorted_dict = {}
    sorted_keys = sorted(num_words, key=num_words.get, reverse=True)  # [1, 3, 2]

    for w in sorted_keys:
        sorted_dict[w] = num_words[w]

    return sorted_dict