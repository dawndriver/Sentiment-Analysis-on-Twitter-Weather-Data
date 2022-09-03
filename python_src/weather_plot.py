import matplotlib.pyplot as plt
import sys

forcast_db = sys.argv[1]
forcast_country = sys.argv[2]

with open(forcast_db, 'r') as fs:
    contents = fs.readlines()

def getDaysFromDate(dateStr):
    y = int(dateStr.split('-')[0]) 
    m = int(dateStr.split('-')[1]) 
    d = int(dateStr.split('-')[2])
    big_months = [1,3,5,7,8,10,12]
    small_months = [4,6,9,11]
    feb_month = 2
    def countDays(m):
	if m-1==0:
	    return 0
	elif m-1 in big_months: 
	    return 31 + countDays(m-1)  
	elif m-1 in small_months:
	    return 30 + countDays(m-1)
	elif m-1 == feb_month:
	    if y%4==0:
		return 29 + countDays(m-1) 
	    else: 
		return 28 + countDays(m-1)
    return countDays(m)+d 

days = [k+1 for k in range(366)]
temp_lsts = [[] for k in range(366)] 
temps = []

for c in contents:
    segs = c.split('\t')
    country = segs[4]
    if country.lower() == forcast_country.lower():
	temp_str = segs[0].split(' ')[1] 
	if temp_str == '-':
	    continue
	dateStr = segs[5].split(' ')[0]
	day_idx =  getDaysFromDate(dateStr)-1
        temp_lsts[day_idx].append(float(temp_str))	

for temp_lst in temp_lsts:
    temp_sum = 0 
    for t in temp_lst: 
	temp_sum += t 
    if temp_sum==0:
	temp_avg = 0 
    else:
	temp_avg = temp_sum / len(temp_lst)
    temps.append(temp_avg)

plt.plot(days, temps)
plt.show()

   # wind_speed = float(segs[1].split(' ')[1]) 
   # rain_level = float(segs[2].split(' ')[1])
   #  humidity = segs[3].split(' ')[1]
    
