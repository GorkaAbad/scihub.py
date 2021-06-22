from scihub import SciHub
import json
import sys
import requests
import argparse
from pathlib import Path
import webbrowser
import urllib 
from bs4 import BeautifulSoup
import random
import string

baseUrl = 'https://scholar.google.es/scholar?hl=es&as_sdt=0%2C5&q=allintitle%3A+'
finalUrl = '&btnG=&oq='

def searchScholar(keywords, n):
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}    
    url = baseUrl + '+'.join(keywords) + finalUrl
    req = urllib.request.Request(url, headers=hdr)
    #res = webbrowser.open(url)
    res = urllib.request.urlopen(req)
    if res.status == 200:
        soup = BeautifulSoup(res.read(), 'lxml')
        count = 1
        for paper in soup.find_all('div',{'class':'gs_r gs_or gs_scl'}):
                if count > n[0]: break      
 
                try:
                    print('[*] Donwloading... {}/{}.'.format(count,n[0]))
                    url = paper.a.get('href')
                    filename = paper.b.string
                    rand = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
                    getPDF(filename,url)
                except Exception as e:
                    print('[!] An error ocurred: {}'.format(e))

                count += 1

def getPDF(filename, url):

    rand = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    filename = filename + rand

    if None != url:
        out = '{}.pdf'.format(filename)
        filename = Path(out)
        print(filename)
        res = requests.get(url,verify=False)
        filename.write_bytes(res.content)
        
        print(' [*] Downloaded successfully.')


def sciBulk(input_path):

    keys = ['ee', 'doi', 'url']

    sh = SciHub()

    with open(input_path) as f:
        data = json.loads(f.read())
    try:
        hits = data['result']['hits']['@total']
        print('[*] {} papers to go.'.format(hits))
        count = 1

        for paper in data['result']['hits']['hit']:
            print('[*] Downloading... {}/{}'.format(count, hits))

            paper = paper['info']
            out = '{}pdf'.format(paper['title'])

            for key in keys:
                if key in paper:
                    # If it is avaliable at Arxiv, download from there
                    if 'arxiv' in paper[key]:
                        url = paper[key].replace('abs', 'pdf')
                        url = '{}.pdf'.format(url)

                        getPDF(paper['title'],url)
                        break

                    else:
                        res = sh.download(paper[key], path=out)

                        if 'err' not in res:
                            print(' [*] Downloaded successfully.')
                            break
                        else:
                            print(' [Info] Triying to download with another method.')

            count += 1

    except Exception as e:
        print('[!] An error ocurred while downloading you file. Triying next')
        print(e)
    

def init():
    parser = argparse.ArgumentParser()
    parser.add_argument('-dblp', help='Supply a json file containing the papers form dblp.',
                        metavar='Path.', type=Path)
    parser.add_argument('-scholar', help='Supply keywords that must be used to donwload papers from scholar.',
                        metavar='Keyword', type=str, nargs='*')
    
    parser.add_argument('-n', help='Number of papers to download. Use with -scholar.', type=int, nargs=1,default=1)
    args = parser.parse_args()
    return args


if __name__ == "__main__":

    args = init()
    if args.dblp:
        sciBulk(args.dblp)
    elif args.scholar and args.n:
        searchScholar(args.scholar,args.n)
