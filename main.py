import requests
from bs4 import BeautifulSoup
import urllib.parse
import os

url = 'https://rhythm-lab.com/breakbeats/'
response = requests.get(url, allow_redirects=True)
content = response.text
soup = BeautifulSoup(content, 'lxml')
session = requests.Session()
links = []


def quoted_url(unquoted_url):
    url_quoted = urllib.parse.quote(unquoted_url)
    return url_quoted


for link in soup.find_all('a', href=True):
    if str(link['href']).endswith('.WAV') or str(link['href']).endswith('.wav'):
        stringed_link = str(link['href'])
        quote_url = quoted_url(stringed_link)
        replace_percent_3A = quote_url.replace('%3A', ":")
        links.append(replace_percent_3A)
        print(links)


def download_files(url_to_download, directory):
    remove_20_percent = url_to_download.replace('%20', ' ')
    remove_27_percent = remove_20_percent.replace('%27', "'")
    remove_28_percent = remove_27_percent.replace('%28', "")
    remove_29_percent = remove_28_percent.replace('%29', "")
    remove_2_percent = remove_29_percent.replace('%2C', "")
    remove_26_percent = remove_2_percent.replace('%26', " ")
    filename = remove_26_percent
    basename = os.path.basename(filename)
    filename = os.path.join(directory, basename)
    request_response = session.get(url_to_download)
    if request_response.status_code != 200:
        print('mega_fail')
    else:
        with open(filename, 'wb+') as f:
            f.write(request_response.content)
            print(f"download success '{filename}'")


for path_to_download in links:
    # print(path_to_download)
    download_files(path_to_download, '/home/breezus/Documents/breaks')
