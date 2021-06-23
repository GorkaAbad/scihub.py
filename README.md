scihub.py
[![Python](https://img.shields.io/badge/Python-3%2B-blue.svg)](https://www.python.org)
=========
This is a fork of [scihub.py](https://github.com/zaytoun/scihub.py), I use it as a library: <br/>
scihub.py is an unofficial API for Sci-hub. scihub.py can search for papers on Google Scholars and download papers from Sci-hub. It can be imported independently or used from the command-line.

This version enables bulk paper donwload.
Importing a JSON file from [dblp](https://dblp.org/),
or by using keywords from [Google Scholar](https://scholar.google.es/).

Setup
-----
```
pip install -r requirements.txt
```

Usage
------

```
usage: main.py [-h] [-dblp Path.] [-scholar [Keyword [Keyword ...]]] [-n N]

A simple bulk paper downloader. It can download papers from dblp exported as JSON or from Google Scholar. It will look them up in sci-hub and in arxiv, along with other abailable sources.

optional arguments:
  -h, --help            show this help message and exit
  -dblp Path.           Supply a json file containing the papers form dblp.
  -scholar [Keyword [Keyword ...]]
                        Supply keywords that must be used to donwload papers from
                        scholar.
  -n N                  Number of papers to download. Use with -scholar.

Example:
python3 main.py -dblp papers.json
python3 main.py -scholar machine learning -n 2
```

License
-------
MIT










