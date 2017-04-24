import sys
import urlparse
import json
import codecs
import os
from google.protobuf import text_format
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from config import *
from googleplay import GooglePlayAPI
from helpers import sizeof_fmt

# list of all categories
categories = ['ANDROID_WEAR', 'ART_AND_DESIGN', 'AUTO_AND_VEHICLES', 'BEAUTY', 'BOOKS_AND_REFERENCE',
            'BUSINESS', 'COMICS', 'COMMUNICATION', 'DATING', 'EDUCATION', 'ENTERTAINMENT', 'EVENTS',
            'FINANCE', 'FOOD_AND_DRINK', 'HEALTH_AND_FITNESS', 'HOUSE_AND_HOME', 'LIBRARIES_AND_DEMO',
            'LIFESTYLE', 'MAPS_AND_NAVIGATION', 'MEDICAL', 'MUSIC_AND_AUDIO', 'NEWS_AND_MAGAZINES',
            'PARENTING', 'PERSONALIZATION', 'PHOTOGRAPHY', 'PRODUCTIVITY', 'GAME', 'GAME_ACTION',
            'GAME_ADVENTURE', 'GAME_ARCADE', 'GAME_BOARD', 'GAME_CARD', 'GAME_CASINO', 'GAME_CASUAL',
            'GAME_EDUCATIONAL', 'GAME_MUSIC', 'GAME_PUZZLE', 'GAME_RACING', 'GAME_ROLE_PLAYING',
            'GAME_SIMULATION', 'GAME_SPORTS', 'GAME_STRATEGY', 'GAME_TRIVIA', 'GAME_WORD', 'FAMILY',
            'FAMILY_ACTION', 'FAMILY_BRAINGAMES', 'FAMILY_CREATE', 'FAMILY_EDUCATION',
            'FAMILY_MUSICVIDEO', 'FAMILY_PRETEND']

if (len(sys.argv) < 2):
    print "Usage: %s output.json [num_results] [offset]" % sys.argv[0]
    print "Please specify an output file."
    print "Max num_results is 100."
    sys.exit(0)

# create initial output file
with open(sys.argv[1], 'w') as f:
    json.dump([], codecs.getwriter('utf-8')(f), ensure_ascii=False)

item = {}
retry = 0 # used to retry category if ValueError thrown
attempt = 0 # used to re-attempt to login
i = 0
while i < len(categories):
    try:
        cat = categories[i]
        ctr = "apps_topselling_free"
        nb_results = None
        offset = None

        if (len(sys.argv) >= 3):
            nb_results = sys.argv[2]
        if (len(sys.argv) >= 4):
            offset = sys.argv[3]

        try:
            api = GooglePlayAPI(ANDROID_ID)
            api.login(GOOGLE_LOGIN, GOOGLE_PASSWORD, AUTH_TOKEN)
        except Exception as e:
            print "googleplay.LoginError: %s" % (e)
            if (attempt < 3):
                attempt += 1
                print "Attempting to login again (%s)..." % (attempt)
                continue

        try:
            message = api.list(cat, ctr, nb_results, offset)
        except:
            print "Error: HTTP 500 - one of the provided parameters is invalid"

        doc = message.doc[0]
        for c in doc.child:

            # permissions
            detailsResponse = api.details(c.docid)
            permissions = detailsResponse.docV2.details.appDetails.permission
            permList = []
            for permission in permissions:
                permList.append(permission)

            item['Title'] = c.title
            item['PackageName'] = c.docid
            item['Developer'] = c.creator
            item['SuperDev'] = len(c.annotations.badgeForCreator)
            item['Price'] = c.offer[0].formattedAmount
            item['OfferType'] = c.offer[0].offerType
            item['VersionCode'] = c.details.appDetails.versionCode
            item['Size'] = sizeof_fmt(c.details.appDetails.installationSize)
            item['Rating'] = "%.2f" % c.aggregateRating.starRating
            item['Downloads'] = c.details.appDetails.numDownloads
            item['Description'] = detailsResponse.docV2.descriptionHtml
            item['Permissions'] = permList

            with open(sys.argv[1], 'r+') as f:
                f.seek(os.stat(sys.argv[1]).st_size - 1)
                f.write(",{}]".format(json.dump(item, codecs.getwriter('utf-8')(f), ensure_ascii=False,
                        sort_keys=True, indent=4)))
    except ValueError as e:
        print "ValueError: %s thrown for category %s" % (e, categories[i])
        if (retry < 3):
            retry += 1
            print "Retrying attempt %s..." % (retry)
            continue
    except Exception as e:
        print "%s thrown for category %s" % (e, categories[i])
        if (retry < 3):
            retry += 1
            print "Retrying attempt %s..." % (retry)
            continue
    if (retry < 3 and attempt < 3):
        print "Finished %s" % (categories[i])
    else:
        print "Skipping %s" % (categories[i])
    retry = 0 # reset retry
    attempt = 0 # reset attempt
    i += 1 # move to next category

# workaround to fix bug where 'None' is input after every entry (will load file into memory)
with open(sys.argv[1], 'r') as f:
    olddata = f.read()
newdata = olddata.replace("},None", "},")
with open(sys.argv[1], 'w') as f:
    f.write(newdata)
