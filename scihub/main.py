from scihub import SciHub
import json
import sys
import requests
from pathlib import Path

input_path = ''
keys = ['ee','doi','url']

if len(sys.argv) > 1:
    input_path = sys.argv[1]

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
                #If it is avaliable at Arxiv, download from there
                if 'arxiv' in paper[key]:
                    
                    url = paper[key].replace('abs','pdf')
                    url = '{}.pdf'.format(url)
                    
                    filename = Path(out)
                    res = requests.get(url)
                    filename.write_bytes(res.content)

                else:
                    res = sh.download(paper[key],path=out)

                if 'err' not in res:
                    print('     [*] Downloaded successfully.')
                    break
                else:
                    print('     [Info] Triying to donwload with another method.')

        count += 1

except Exception as e:
    print('[!] An error ocurred while downloading you file. Triying next')
    print(e)



#res = sh.fetch('https://doi.org/10.2200/S00861ED1V01Y201806AIM039')

#print(res)
