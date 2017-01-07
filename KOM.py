import requests
import secrets # api token 
import numpy as np

# define global variables
base_url='https://www.strava.com/api/v3/segments/'

class stravaSegment(object):

	def __init__(self,id):
		self.id=id # segment ID
		self.name=requests.get(base_url+str(id)+'?access_token='+secrets.apiToken).json()['name'] # segment name
		self.effortCount=requests.get(base_url+str(id)+'?access_token='+secrets.apiToken).json()['effort_count'] # # efforts
		self.athleteCount=requests.get(base_url+str(id)+'?access_token='+secrets.apiToken).json()['athlete_count'] # athletes 


	def getKOMs(self,start_year,start_month,start_day,end_year,end_month,end_day):
		perPage='100' # set the number of efforts printed 'per page'
		
		# set start and end dates for efforts investigated. user must provide start
		# and stop dates as function arguments (yr, mo, day...)
		startDate=str(start_year)+'-'+str(start_month)+'-'+str(start_day)+'T17:00:00Z'
		endDate=str(end_year)+'-'+str(end_month)+'-'+str(end_day)+'T17:00:00Z'

		efforts=[] # place segment efforts here
		
		for i in range(100): # loop through 100 pages per segment. this should be 
							 # improved to only access as many pages as exist
							 # per segment
			# build url call
			url= base_url+str(self.id)+'/all_efforts?access_token='+secrets.apiToken+'&start_date_local='+startDate+'&end_date_local='+endDate+'&per_page='+perPage+'&page='+str(i+1)
			# requests.get
			results=requests.get(url)
			# convert to json for manipulation
			jsonified_results=results.json()
			# add efforts to python list
			efforts.append(jsonified_results)
		
		best_times = [] # make empty list to put times in
		
		fastest_time=1+efforts[0][0]['elapsed_time'] # inital fastest 
													 # time is 1 second slower 
													 # than first ever time, 
													 # so the first time will always 
													 # be recorded as a 
													 # new fastest time.
		# go through a pages
		for a in range(len(efforts)):
			# go through the number of efforts per page
			for b in range(len(efforts[a])):
				# if time is fastest yet, then add to our list 
				# update the fact that new fastest time has changed
				if efforts[a][b]['elapsed_time']<fastest_time:
					oneRun = []
					oneRun.append(efforts[a][b]['elapsed_time'])
					oneRun.append(efforts[a][b]['start_date'])
					fastest_time=efforts[a][b]['elapsed_time']
					best_times.append(oneRun)   # put list from KOM effort
												# into list of KOM efforts
 		return best_times

# output
whirl = stravaSegment(673849) #had to look up this segment id on strava
koms = whirl.getKOMs(2016,5,1,2016,6,1)
# convert to np array for export
to_export=np.asarray(koms)
print to_export

np.savetxt('test.csv', to_export, delimiter=",",fmt='%s ')



