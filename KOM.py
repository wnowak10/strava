import requests
import secrets 
import numpy as np


class stravaSegment(object):

	def __init__(self,id):
		self.id=id
		self.name=requests.get('https://www.strava.com/api/v3/segments/'+str(id)+'?access_token='+secrets.apiToken).json()['name']
		self.effortCount=requests.get('https://www.strava.com/api/v3/segments/'+str(id)+'?access_token='+secrets.apiToken).json()['effort_count']
		self.athleteCount=requests.get('https://www.strava.com/api/v3/segments/'+str(id)+'?access_token='+secrets.apiToken).json()['athlete_count']


	def getKOMs(self,start_year,start_month,start_day,end_year,end_month,end_day):
		# set the number of efforts printed 'per page'
		perPage='100'
		# set start and end dates for efforts investigated. user must provide start
		# and stop dates as function arguments
		startDate=str(start_year)+'-'+str(start_month)+'-'+str(start_day)+'T17:00:00Z'
		endDate=str(end_year)+'-'+str(end_month)+'-'+str(end_day)+'T17:00:00Z'
		# go through all of the pages. 
		efforts=[]
		for i in range(100):
			# build url call
			url= 'https://www.strava.com/api/v3/segments/'+str(self.id)+'/all_efforts?access_token='+secrets.apiToken+'&start_date_local='+startDate+'&end_date_local='+endDate+'&per_page='+perPage+'&page='+str(i+1)
			# get
			a=requests.get(url)
			# convert to json
			jsonifiedData=a.json()
			# add efforts to python list
			efforts.append(jsonifiedData)
		# make empty list to put times in
		times = []
		# an initial, very slow fastest time
		fastestTime=100000
		# go through a pages
		for a in range(len(efforts)):
			# go through the number of efforts per page
			for b in range(len(efforts[a])):
				# if time is fastest yet, then add to our list 
				# update the fact that new fastest time has change
				if efforts[a][b]['elapsed_time']<fastestTime:
					oneRun = []
					oneRun.append(efforts[a][b]['elapsed_time'])
					oneRun.append(efforts[a][b]['start_date'])
					fastestTime=efforts[a][b]['elapsed_time']
					times.append(oneRun)
		return times

# output
whirl = stravaSegment(673849)
koms = whirl.getKOMs(2016,5,1,2016,6,1)
# convert to np array for export
b=np.asarray(koms)
print b

np.savetxt('test.csv', b, delimiter=",",fmt='%s ')



