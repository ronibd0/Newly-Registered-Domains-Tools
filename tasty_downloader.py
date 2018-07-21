#~/usr/bin/python

import requests
import re
import datetime
import math

''' Query date '''
date = datetime.date.fromordinal(datetime.date.today().toordinal()-3)

''' Output location '''
fileName = "/opt/scripts/tasty/%s.txt" % (date)

''' Taste Reports Query URL '''
url = "http://tastereports.it/archives.html?type=added&stat_date=" + str(date) + "&registrar_id=all&Submit=Go&keyword="

''' Regex '''
regexDomain = r'\"domain\.html\?domain=([a-zA-Z0-9-.]{1,255})\"'
regexNumOfDomains = r'\(([0-9,]{0,10})\sdomain'

''' Request Headers '''
headers = {
        "Host" : "tastereports.it",
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

''' Perform HTTP requests '''
def getDomains(pageNum):
	newUrl = url + "&start=" + str(pageNum * 100)
	req = requests.post(newUrl, data="", headers=headers, verify=False)
	print "[+] Data retrieved from: %s, Status code: %s" % (newUrl, req.status_code) 
	return req.text


if __name__ == '__main__':
	print "[!] Starting Tasty Downloader..."

	''' Perform the web request '''
	r = requests.get(url, data="", headers=headers, verify=False)

	''' Get the number of domains '''
	numOfDomains = re.findall(regexNumOfDomains, r.text)

	''' Remove "," if there is a large number of domains '''
	records = numOfDomains[0].replace(",", "")

	print "[+] Found %s domains, starting download..." % (records)

	''' Can only get 100 records at a time '''
	webRequests =  math.ceil(float(records) / float(100))

	''' Loop through all entries, than can be multithreaded later '''
	for i in range(int(webRequests)):
		data = getDomains(i)
		domains = re.findall(regexDomain, data)

		print "[+] Got: %s valid domains" % (len(domains))	

		f = open(fileName, 'a')

		''' Create / write domains to a text file '''
		for domain in domains:
			f.write(domain + "\n")
		f.close()
