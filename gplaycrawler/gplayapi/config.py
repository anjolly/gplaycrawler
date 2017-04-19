import json
import os.path

LANG            = None
ANDROID_ID      = None #GSF Google Service Framework
GOOGLE_LOGIN    = None
GOOGLE_PASSWORD = None
AUTH_TOKEN      = None

# separator used by search.py, categories.py, ...
SEPARATOR = ";"

def raw_input_with_default(name, default):
    print "{}[{}]: ".format(name, default)
    value = raw_input()
    return value.strip() if value.strip() != '' else default

if not os.path.isfile('auth.json'):
    with open('auth.json', 'wb') as f:
        LANG            = raw_input_with_default('LANG', 'en_US')
        ANDROID_ID      = raw_input_with_default('ANDROID_ID', 'xxxxxxxxxxxxxxxx')
        GOOGLE_LOGIN    = raw_input_with_default('GOOGLE_LOGIN', 'account@gmail.com')
        GOOGLE_PASSWORD = raw_input_with_default('GOOGLE_PASSWORD', '***')
        f.write(json.dumps(
        {
            'LANG':LANG,
            'ANDROID_ID':ANDROID_ID,
            'GOOGLE_LOGIN':GOOGLE_LOGIN,
            'GOOGLE_PASSWORD':GOOGLE_PASSWORD
        }
        ))
elif os.path.isfile('auth.json'):
    with open('auth.json', 'rb') as f:config = json.load(f)
    LANG            = config['LANG']
    ANDROID_ID      = config['ANDROID_ID']
    GOOGLE_LOGIN    = config['GOOGLE_LOGIN']
    GOOGLE_PASSWORD = config['GOOGLE_PASSWORD']
    AUTH_TOKEN      = None

if any([each == None for each in [ANDROID_ID, GOOGLE_LOGIN, GOOGLE_PASSWORD]]):
    raise Exception("Config not set. Delete auth.json and run config.py again.")
