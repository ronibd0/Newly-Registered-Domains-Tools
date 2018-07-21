#~/usr/bin/python

import requests
import re
import datetime
import math

daysBehind = 2

''' Query date '''
date = datetime.date.fromordinal(datetime.date.today().toordinal()-daysBehind).strftime('%Y-%-m-%-d')

''' Output location '''
fileName = "/opt/scripts/tasty/%s.txt" % (datetime.date.fromordinal(datetime.date.today().toordinal()-daysBehind))

''' Taste Reports Query URL '''
url = "https://domain-status.it/archives/" + str(date) + "/"

''' Regex '''
reNumOfPages = r"page\s1\son\s(.*),"
reDomains = r'<li>.*">(.*)</a>'

''' Request Headers '''
headers = {
        "Host" : "domain-status.it",
	"User-Agent" : "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0",
        "Connection" : "close",
        "Upgrade-Insecure-Requests" : "1",
        "Cache-Control" : "no-cache, no-store, must-revalidate",
        "Pragma" : "no-cache",
        "Expires" : "0"
}

''' Used for debug '''
'''
	http_proxy = "http://127.0.0.1:8080"
	https_proxy = "https://127.0.0.1:8080"
	
	proxyDict = {
	        "http" : http_proxy,
	        "https" : https_proxy
	}

	example:
	r = requests.post(url, data="", headers=headers, proxies=proxyDict, verify=False)
'''

if __name__ == '__main__':
	print "[!] Starting Tasty Downloader..."

	baseURLs = [
		"https://domain-status.it/archives/%s/org/registered/%s",
		"https://domain-status.it/archives/%s/name/registered/%s",
		"https://domain-status.it/archives/%s/biz/registered/%s", 
		"https://domain-status.it/archives/%s/it/registered/%s",
		"https://domain-status.it/archives/%s/net/registered/%s",
		"https://domain-status.it/archives/%s/aero/registered/%s",
		"https://domain-status.it/archives/%s/us/registered/%s"
	]

	''' Perform the web request '''

	for baseURL in baseURLs:
		url = baseURL % (date, 1)

		r = requests.get(url, data="", headers=headers)

		''' Get the number of domains '''
		numOfPages = re.findall(reNumOfPages, r.text)

		if str(numOfPages) == "[]":
			numOfPages = [1]

		for i in range(1, int(str(numOfPages[0])) + 1):
			url = baseURL % (date, i)

			print url

			r = requests.get(url, data="", headers=headers)
			domains = re.findall(reDomains, r.text)
			
			f = open(fileName, 'a')

			for d in domains:
				f.write(d.encode('utf8') + "\n")

			f.close()
