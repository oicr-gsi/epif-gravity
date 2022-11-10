import gravity, time
from sys import exit

baseurl=""
consumer_key=""
consumer_secret=""

with open('.gravity') as f:
    for line in f:
        s=line.split("=")
        key=s[0].strip()
        if key == "consumer_key":
            consumer_key=s[1].strip()
        elif key == "consumer_secret":
            consumer_secret=s[1].strip()
        elif key=="baseurl":
            baseurl=s[1].strip()

if not baseurl or not consumer_key or not consumer_secret:
    print("FAIL: Unable to retrieve Gravity forms credentials from gravity file")
    sys.exit("Fix gravity credentiall file")

session = gravity.getsession(consumer_key,consumer_secret)
###############################################################################
# Get_forms
###############################################################################
result=gravity.get_forms(session,baseurl)
if not result:
    print("FAIL: get_forms test ID 3 does not have keys")
else:
    try:
        if result['3']['id'] == '3':
            print("PASS: get_forms test ID 3 is equal to stated ID 3")
        else:
            print("FAIL: get_forms test ID 3 is not equal to stated ID 3")
    except KeyError:
        print("FAIL: get_forms test ID 3 does not have keys")

###############################################################################
# get_form_entries
###############################################################################
result=gravity.get_form_entries(session,baseurl,'3')
totalentries=len(result)
if totalentries==0:
    print("FAIL: get_form_entries has no responses")
else:
    print("PASS: get_form_entries")

###############################################################################
# get_form_entries_created_since
###############################################################################
tt="2022-09-19 00:00:00"
result=gravity.get_form_entries_created_since(session,baseurl,'3',tt)
testtime=time.strptime(tt,"%Y-%m-%d %H:%M:%S")
createdentries=len(result)
if createdentries>=totalentries:
    print("FAIL: get_form_entries_created_since has just as many entries as total number")
else:
    ispass=True
    for entry in result:
        created=time.strptime(entry['date_created'],"%Y-%m-%d %H:%M:%S")
        if testtime>created:
            ispass=False
            print("-".join(["FAIL: get_form_entries_created_since created date is greater than test date",tt,entry['date_created']]))
    if ispass:
        print("PASS: get_form_entries_created_since")

###############################################################################
# get_form_entries_updated_since
###############################################################################
tt="2022-09-20 00:00:00"
result=gravity.get_form_entries_updated_since(session,baseurl,'3',tt)
updatedentries=len(result)

if updatedentries == 0:
    print("FAIL: get_form_entries_updated_since has no entries")
else:
    ispass=True
    for entry in result:
        created=time.strptime(entry['date_updated'],"%Y-%m-%d %H:%M:%S")
        if testtime>created:
            ispass=False
            print("-".join(["FAIL: get_form_entries_updated_since updated date is greater than test date",tt,entry['date_updated']]))
    if ispass:
        print("PASS: get_form_entries_updated_since")
#if updatedentries[0]['date_created']
