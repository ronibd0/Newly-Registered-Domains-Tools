# Newly-Registered-Domains-Tools
Python scripts used to scrape newly registered domains names and search through them

## tasty_downloader.py
Basic python application for downloading newly registered domains

### Usage
```
python tasty_download.py
```

This creates an output file. An example of the output file is below:
```
newdomain1.it
newdomain2.it
newdomain3.it
newdomain4.it
...
```

## domain_finder.py
Basic python application used to search through a list of domains and match keywords. Keywords contain a score and if the score is over 1.0 it will output the results or send an email. 

### Usage
```
python domain_finder.py
...
```

This logs output to the terminal or can send an email. An example of the output is below:

```
[!] Starting Domain Finder...
<score>: <dodgydomain>.it - ['<keywordmatched>']
<score>: <dodgydomain>.it - ['<keywordmatched>']
<score>: <legitimatedomain>.it - ['<keywordmatch>']
<score>: <dodgydomain>.it - ['<keywordmatch>']
...
```
