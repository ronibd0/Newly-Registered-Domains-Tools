#~/usr/bin/python

import datetime
import smtplib
from email.mime.text import MIMEText

''' Query date  '''
date = datetime.date.fromordinal(datetime.date.today().toordinal()-3)

''' File read location '''
fileName = "/opt/scripts/tasty/%s.txt" % (date)

''' Primary matches + to total score '''
scoreMatch = [
	["google", 1.0],
	["gmail", 1.0],
	["microsoft", 1.0],
	["outlook", 1.0],
	["hotmail", 1.0],

	["maps", 0.5],
	["docs", 0.5],
	["drive", 0.5]
]

''' Blacklist of words - to total score '''
blacklist = [
	["driver", 0.3]
]

''' List used to save results '''
domainList = []

''' Email variables '''
toAddr = "<mailbox>@<domain>"
fromAddr = "<mailbox>@<domain>"
smtpServer = "<smtpserver>"
username = "<username>"
password = "<password>"

def sendEmail(data):

	print "[+] Found data, sending email to %s" % (toAddr)

	domainList = ""
	''' Write all domains to a variable '''
	for domain in data:
		domainList = domainList + str(domain[0]) + ": " + domain[1] + " - " + str(domain[2]) + "\n"

	''' Email body / subject '''
	emailBody = "Hi %s,\n\nThe following suspicious domains have been identified:\n%s" % (toAddr, domainList)
	emailSubject = "Public Domains Registered on %s" % (date)

	''' Email attributes '''
	msg = MIMEText(emailBody)
	msg["To"] = toAddr
	msg["From"] = fromAddr
	msg["Subject"] = emailSubject

	s = smtplib.SMTP(smtpServer)
	''' Authenticate '''
	s.login(username, password)
	''' Send email '''
	s.sendmail(fromAddr, toAddr, msg.as_string())
	s.quit()	

if __name__ == '__main__':

	print "[!} Starting Domain Finder..."

	''' Open the file '''
	with open(fileName) as f:

		''' Loop over a list of newly created domains '''
		for line in f:

			''' local variables '''
			findCount = 0
			matchedOn = []
			score = 0.0

			''' Loop over the keywords '''
			for keyword in scoreMatch:
				''' is the keyword in the domain? '''
				if keyword[0] in line:
					findCount = findCount + 1
					matchedOn.append(keyword[0])
					score = score + keyword[1]

			''' Loop over the blacklist '''
			for keyword in blacklist:
				''' is the keyword in the domain? '''
				if keyword[0] in line:
					findCount = findCount - 1
					score = score - keyword[1]

			''' Add results to list after '''
			if (findCount >= 2 and score >= 1.0) or (score >= 1.0):
				domainList.append([score, line.rstrip(), str(matchedOn)])


	if domainList:

		''' Order by score, then the domain name '''
		scoreOrder = sorted(domainList, key=lambda x: (-x[0], x[1]))

		''' Send email '''
		#sendEmail(scoreOrder)	

		''' Output to terminal '''
		for domain in scoreOrder:
			print str(domain[0]) + ": " + domain[1] + " - " + str(domain[2])

	else:
		print "[!] Domain search finished, nothing found."
