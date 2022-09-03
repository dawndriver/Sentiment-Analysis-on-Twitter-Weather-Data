# -*- coding: utf-8 -*-
import sys,re

def getWeatherWords():
    word_list = []
    with open('../../dictionary/weather.txt', 'r') as fs:
	contents = fs.readlines()
	for c in contents:
	    words = c.split('\t')[2].split(',')
	    if not c.split('\t')[1] == 'forcast':
		for w in words:
		    word_list.append(w)    
    return word_list
 
with open('../../mini_dataset/weather', 'r') as fr:
    contents = fr.readlines()


talking_contents = [] 
forcast_f = open('../weather_forcast', 'w')
for c in contents:
    segs = c.split('\t')
    msg = segs[0].lower()
    location = segs[2]
    time = segs[3]
    decimal_regex = '-?[0-9]*[\.,]?[0-9]+'
    match = re.search('temperature|temp|\st:|c\s\(h:|c/hr\shigh\s|^current\sweather:\s', msg)
    forcast_str = ''
    if match: 
        s_idx = match.end() 
        e_idx = s_idx+25 
        s = msg[s_idx:e_idx]
	match = re.search(decimal_regex, s)
        if match:
	    num_str = s[match.start():match.end()].replace(',', '.')  
            num_float = float(num_str)
	    rest_temp = s[match.end():].strip()
            if rest_temp.find('f')==0 or \
               rest_temp.find('f')==1 or \
               rest_temp.find('f')==2:
		num_float = round((num_float-32)/1.8,2) 
            elif rest_temp.find('c')==0 or \
		 rest_temp.find('c')==1 or \
                 rest_temp.find('c')==2 or \
                 rest_temp.find('&deg;c')==0:
		pass
	    else: # cannot find temperature measure, so this is not a forcast 
		talking_contents.append(c)
                continue
	      
	    if num_float < -50 or num_float > 70: # it is not talking about weather
		forcast_str += 'Temperature - \t' 
	    else:  
		forcast_str += 'Temperature ' + str(num_float)  + ' °C\t'
             
	    match = re.search('wind\s|wind:', msg)
            num_str = '-'
	    if match:
		s_idx = match.end() 
                e_idx = s_idx+20
                s = msg[s_idx:e_idx]
		match = re.search(decimal_regex, s)
                if match:
		    num_str = s[match.start():match.end()].replace(',', '.') 
		    num_float = float(num_str)
		    match = re.search('m/h|m/s|km/h|mph|kmph|kts|kph', s)
		    if match:
			measure_str = s[match.start():match.end()] 
			if measure_str=='km/h' or \
                           measure_str=='kph' or \
                           measure_str=='m/h' or \
                           measure_str=='kmph':
			    num_str = str(round(num_float*1000/3600, 2))	
			elif measure_str=='mph':
			    num_str = str(round(num_float*0.45, 2)) 
			elif measure_str=='kts':
			    num_str = str(round(num_float*0.514, 2))
	    forcast_str += 'Wind ' +  num_str + ' m/s\t'
	    	
	    idx = msg.find('rain') 
            num_str = '-'
	    if idx >= 0:
                s_idx = idx+len('rain')
                e_idx = s_idx+20
                s = msg[s_idx:e_idx]
		match = re.search(decimal_regex, s) 
                if match:
		    num_str = s[match.start():match.end()].replace(',', '.')
		    num_float = float(num_str)
		    match = re.search('in', s)
                    if match:
			num_str = str(round(num_float*25.4, 2))
	    forcast_str += 'Rain ' + num_str + ' mm\t'
	     
	    match = re.search('humidity|rh:|hum:',msg)
            humidity_str = '-'
	    if match:
                s_idx = match.start()-10
                e_idx = match.end()+5
                if s_idx < 0:
		    s_idx = match.end() 
                s = msg[s_idx:e_idx]
		match = re.search(decimal_regex+'%', s)
                if match:
		    humidity_str = s[match.start():match.end()]
            forcast_str += 'Humidity ' + humidity_str + '\t' 
	     
	    forcast_f.write(forcast_str + location + '\t' + time)   
        else:
	    talking_contents.append(c)
    else:
	 talking_contents.append(c)
forcast_f.close()


# further filter out some data non-related to weather
# mostly are those data starting with capital letters 
with open('../weather_talking', 'w') as weather_talking_fs:
    weather_words =  getWeatherWords()
    for c in talking_contents:
	tweets_wl = c.split('\t')[1].split(',')
	for w in tweets_wl: 
	    if w in weather_words:
		weather_talking_fs.write(c)	
		break

