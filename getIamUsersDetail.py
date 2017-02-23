import boto
import commands,json
import config
from createcsv import createcsv


def getIamUsersDetail(output='csvFormat'):
    '''
    this module is to fetch iam users detail along with their access keys and 
    their creation date, last access date etc.
    Default output format is csv, but you can specify output as json

    output: csvFormat/ json
    '''
    if output not in ['csvFormat','json']:
	print "Invalid output format choosen.."
	return json.dumps({"status":False,"message":"Invalid output format choosen..","output":None})

    ## Connecting to iam service
    iam = boto.connect_iam(config.ACCESS_KEY,config.SECRET_KEY)

    ## Fetching all users detail from iam
    users = iam.get_all_users('/',max_items=1000)
    users = users['list_users_response']['list_users_result']['users']

    ## CSV Headers
    data_list = [["User Name","Password last used","Access Key","status","Creation Date","AccessKey Last used"]]
    data_json = {}

    for i in users:
    	## Fetching all access keys for particular iam user
    	keys = iam.get_all_access_keys(user_name=i['user_name'])['list_access_keys_response']['list_access_keys_result']['access_key_metadata']

	data_json[users.index(i)] = {"user":i['user_name'],
					"password_last_used":i.get('password_last_used')}		

    	for j in keys:
	    ## Using awscli to get access key's last used detail
            key_last_used = json.loads(commands.getoutput("aws iam get-access-key-last-used --access-key-id %s" % j['access_key_id']))
	    info = [i['user_name'],i.get('password_last_used'),j['access_key_id'],j['status'],j['create_date'],key_last_used["AccessKeyLastUsed"].get("LastUsedDate")]
	    #print info

	    ## saving the information in list to write it in csv
            data_list.append(info)

	    ## saving information in dictionary format
	    data_json[users.index(i)]["Access_key"] = j['access_key_id']
	    data_json[users.index(i)]["status"] = j['status']
	    data_json[users.index(i)]["create_date"] = j["create_date"]
	    data_json[users.index(i)]["AccessKeyLastUsed"] = key_last_used["AccessKeyLastUsed"].get("LastUsedDate")
						
    if output == "json":
	return json.dumps({"status":True, "message":"Result got successfull","output":data_json})
    else:
	## Calling csv module to write data in csv
	createcsv("iamuser.csv",data_list)
	return json.dumps({"status":True, "message":"Result got successfull and saved in iamuser.csv filee","output":None})

if __name__=="__main__":
    print getIamUsersDetail()
