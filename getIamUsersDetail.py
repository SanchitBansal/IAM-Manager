import boto
import commands,json
import config
from createcsv import createcsv

'''
this module is to fetch iam users detail along with their access keys and 
their creation date, last access date etc.
'''

## Connecting to iam service
iam = boto.connect_iam(config.ACCESS_KEY,config.SECRET_KEY)

## Fetching all users detail from iam
users = iam.get_all_users('/',max_items=10)
users = users['list_users_response']['list_users_result']['users']

## CSV Headers
data = [["User Name","Password last used","Access Key","status","Creation Date","AccessKey Last used"]]

for i in users:
    ## Fetching all access keys for particular iam user
    keys = iam.get_all_access_keys(user_name=i['user_name'])['list_access_keys_response']['list_access_keys_result']['access_key_metadata']

    for j in keys:
	## Using awscli to get access key's last used detail
        key_last_used = json.loads(commands.getoutput("aws iam get-access-key-last-used --access-key-id %s" % j['access_key_id']))
	info = [i['user_name'],i.get('password_last_used'),j['access_key_id'],j['status'],j['create_date'],key_last_used["AccessKeyLastUsed"].get("LastUsedDate")]
	#print info

	## saving the information in list to write it in csv
        data.append(info)

print "Please find iamuser.csv file containing required data"
## Calling csv module to write data in csv
createcsv("iamuser.csv",data)
