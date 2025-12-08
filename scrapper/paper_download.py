from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
import re

from bs4 import BeautifulSoup

patterns = [
'https?://bib-pubdb1\.desy\.de/record/\d+'# add some kinda regex matching for big-known paper websites
]

def parse_photonscience_paper_urls(html):
    #function specific to https://photon-science.desy.de/

    # HTML nodes that contain URL+ Title
    soup = BeautifulSoup(html)
    nodes = soup.select('p.join2publist a.RichTextExtLink')

    url_title = []
    for n in nodes:
        print(n)
        url = n['href']
        title = n.find('span').string
        url_title.append((url,title))
    return url_title



def parse_relevant_paper_urls(html):
    filtered_urls = []
    for p in patterns:
        filtered_urls.extend(re.findall(p, html))
    return filtered_urls

def load_url(url):
    # set up ChromeOptions
    options = webdriver.ChromeOptions()
    options.unhandled_prompt_behavior = 'accept'
    print(options)
    options.add_argument("--headless=new") # This is being ignored
    driver = webdriver.Chrome()
    driver.get(url)
    #driver.implicitly_wait(5) # This is the proper way but it is being ignored when I run it
    time.sleep(3)

    return driver.page_source



def generate_csv_papers():
    source_urls = []
    # Load csv urls (data/scrapper/sources)
    with open('data/scrapper/sources.csv')as f:
        source_urls = f.read().split('\n')
    # Load each website for several seconds (the urls are dynamic)
    url_title=[]
    for url in source_urls[1:]: #skip csv header
        if 'photon-science' in url:
            print(f'Rendering url {url}')
            html = load_url(url)
            url_title.extend(parse_photonscience_paper_urls(html))
        else:
            # I think its good to just run a regex all over the HTML
            # to detect URLs for well-known 
            # public paper repositories. 
            pass 
    # Add paper title (when missing)
    # Save csv for url and paper
    with open('data/papers/list.csv','w') as f:
        out= 'URL,title\n'
        out += '\n'.join([f'{u},{t}' for u,t in url_title])
        f.write(out)
      



generate_csv_papers()
