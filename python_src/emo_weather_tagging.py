import sys


if len(sys.argv) < 3:
    print 'Usage: python emo_weather_tagging.py <emotion dict> <emotion associtation file>'
    exit()

import emoji_assoc_mining as assoc
import emo_words_tagging as tagging

with open('../../mini_dataset/weather_talking','r') as fs:
    talkings = fs.readlines()

assoc.pos_emojis.extend(assoc.very_pos_emojis)
assoc.neg_emojis.extend(assoc.very_neg_emojis)
weather_dict = assoc.buildWeatherDict('../../dictionary/weather.txt') 

output = ''
for talk in talkings:
    segs = talk.split('\t') 
    msg = segs[0]
    wl = segs[1].split(',')

    weather = ''	
    for w in wl:
	if w in weather_dict.keys():
	    weather += ',' + weather_dict[w]    	
    weather = weather[1:]
  
    sentiment = assoc.getSentiment(msg)
    if sentiment == 'neutral':
	matched_values = assoc.getMatchedValues(wl,tagging.emo_dict)
	word = tagging.getAssocWord(matched_values)
	if word:
	    if isinstance(word,tuple):
		sentiment = tagging.two_word_emo_dict[word]		
	    else:
		sentiment = tagging.one_word_emo_dict[word]
	else:
	    sentiment = 'neutral'	
    
    output += talk.strip()+'\t'+sentiment+'\t'+weather+'\n'

with open('weather_tagged','w') as fs:
    fs.write(output) 
