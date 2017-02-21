import csv

def createcsv(filename, data):
    '''
    function to create csv from the data list
    '''
    with open(filename, 'w') as fp:
	a = csv.writer(fp, delimiter=',')
    	a.writerows(data)
