import sys,re


weather_f = open('../emotion_new.csv', 'w')
weather_str = 'location,time,emotion,cat\n'

weather_f.write(weather_str)

with open('../weather_tagged', 'r') as fr:
    contents = fr.readlines()

for c in contents:
    flag_dict = {'temp' : False, 'rain' : False, 'humid' : False, 'wind' : False}

    segs = c.split('\t')
    location = segs[2]
    time = '01-' + segs[3][5:7] + '-' + segs[3][0:4]
    emotion = segs[4]
    cats = segs[5].strip().split(',')
    for cat in cats:
        ## For temperature
        if cat in ('cold', 'warm', 'hot','snow', 'storm'):
            if (not flag_dict['temp']):
                weather_str = location+','+time + ',' + emotion + ',' + 'temp' + '\n'
                flag_dict['temp'] = True
                weather_f.write(weather_str)
                #print flag_dict['temp']

        ## For rain
        if cat in ('rain', 'storm'):
            if (not flag_dict['rain']):
                weather_str = location+','+time + ',' + emotion + ',' + 'rain' + '\n'
                flag_dict['rain'] = True
                weather_f.write(weather_str)

        ## For humid
        if cat in ('humid'):
            if (not flag_dict['humid']):
                weather_str = location+','+time + ',' + emotion + ',' + 'humid' + '\n'
                flag_dict['humid'] = True
                weather_f.write(weather_str)

        ## For wind
        if cat in ('wind', 'storm'):
            if (not flag_dict['wind']):
                weather_str = location+','+time + ',' + emotion + ',' + 'wind' + '\n'
                flag_dict['wind'] = True
                weather_f.write(weather_str)

        if (not flag_dict['rain'] and not flag_dict['rain'] and not flag_dict['rain'] and not flag_dict['rain']):
            weather_str = location+','+time + ',' + emotion + ',' + cat + '\n'
            weather_f.write(weather_str)
