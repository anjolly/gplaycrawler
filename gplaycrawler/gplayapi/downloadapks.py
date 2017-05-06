import sys
import time
from google.protobuf import text_format

from config import *
from googleplay import GooglePlayAPI

if (len(sys.argv) is 2):
    if (sys.argv[1] == "failed.txt"):
		print "This file name is reserved and cannot be used."
		print "Please rename file or copy contents to a new file."
		sys.exit(0)
else:
	pkgFile = "pkgnames.txt"

exceptions = 0
	
#read in packages
with open(pkgFile, "rb") as file:
	for line in file:
		try:
			#authenticate
			api = GooglePlayAPI(ANDROID_ID)
			api.login(GOOGLE_LOGIN, GOOGLE_PASSWORD, AUTH_TOKEN)

			#download apks
			fileName = "%s.apk" % (line)
			data = api.download(line)
			with open("apks\%s" % (fileName), "wb") as f:
				f.write(data)

			time.sleep(20) #reduces frequency of requests to avoid being blocked
		except Exception as e:
			print "'%s' thrown for %s" % (e, line)
			exceptions += 1
			with open('failed.txt', 'a') as f:
				f.write(line)
print "File successfully completed."
print "Number of exceptions thrown: %s" % (exceptions)