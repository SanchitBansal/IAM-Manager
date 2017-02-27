from getIamUsersDetail import getIamUsersDetail
import json
import argparse
import boto
import config
from datetime import datetime

def setInactive(date0, date1, include_unused=1):
    '''
    function to set Access key as inactive.. It will first fetch users data from aws and then based on the dates provided it will set keys as inactive

    date0: start date above which users will be filtered
    date1: end date below which users will be filtered
    include_unused: whether you want to set all keys which are never used as inactive 
    '''

    ## Connecting to iam service
    iam = boto.connect_iam(config.ACCESS_KEY,config.SECRET_KEY)

    data = getIamUsersDetail(output='json')
    data = json.loads(data)

    for index,output in data["output"].iteritems():
	if output["status"] == "Active" and ((output["AccessKeyLastUsed"] and output["AccessKeyLastUsed"].split("T")[0]<date1 and output["AccessKeyLastUsed"].split("T")[0]>date0) or (not output["AccessKeyLastUsed"] and include_unused)):
	    print "Deleting %s access_key of user %s" % (output["Access_key"],output["user"])
	    iam.update_access_key(output["Access_key"],"Inactive")

def valid_date(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-d0","--date0", type=valid_date, help="start date above which users will be filtered - format YYYY-MM-DD", required=True)
    parser.add_argument("-d1","--date1", type=valid_date, help="end date below which users will be filtered - format YYYY-MM-DD", required=True)
    parser.add_argument("-i", "--include_unused", type=int, choices=set((0, 1)), help="It is to include all the keys which are never used",required=True)

    args = parser.parse_args()
    date0 = args.date0
    date1 = args.date1
    include_unused = args.include_unused

    if date0>=date1:
	raise Exception("date0 should be less than date1")
    setInactive(date0, date1, include_unused)



