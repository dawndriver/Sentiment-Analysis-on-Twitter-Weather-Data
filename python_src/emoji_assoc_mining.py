import sys

# very positive emoji icons
very_pos_emojis = [':))', ': ))', ':) )', ':-))', ':-) )', ':):)', ':) :)', ':-):-)', ':-) :-)', ';))', '; ))', ';) )', ';-))', ';-) )', ';);)', ';) ;)', ';-);-)', ';-) ;-)', ':dd', ':DD', ';dd', ';DD', ':-dd', ':-DD', ';-dd', ';-DD', ':-pp', ':-PP', ';-pp', ';-PP', '^___^', '^____^', '^_____^', '<33']

# positive emoji icons
pos_emojis = [':)', ': )', ':-)', ';)', '; )', ';-)',':>', ': >', ':->', ';>', '; >', ';->', ':]', ': ]', ':-]', ';]', '; ]', ';-]', ':*', ':-*', ';*', ';-*', ':D', ':-D', ';D', ';-D', ':d', ':-d', ';d', ';-d', ':P', ':-P', ';P', ';-P', ':p', ':-p', ';p', ';-p', ':V', ':-V', ';V', ';-V', ':v', ':-v', ';v', ';-v', '^_^', '^__^', '<3']

# negative emoji icons
neg_emojis = [':(', ': (', ':-(', ':\'(', ':\'-(', ':<', ':c', ':[', ': [', ':-[', ':o', ':O', ':-o', ':-O', ':\\', ': \\', ':-\\', ':/', ': /', ':-/', '<_<', '>_>']

# very negative emoji icons
very_neg_emojis = [':((', ': ((', ':( (', ':-((', ':-( (', ':cc', ':oo', ':OO', ':\\\\', '://', ':-//', ':-\\\\']  

useWeatherDict = False
useEmotionDict = False

cut_count = 10
cut_confidence = 0.5
output_tweets = False 
useFourSentiments = False

# add some enhanced emojis for -__- 
for i in range(1,21):
    mid = ''
    for j in range(i):
	mid += '_'
    if i <= 2:
	neg_emojis.append('-'+mid+'-') 
    else:
	very_neg_emojis.append('-'+mid+'-')

# add some enhaced emojis for o_O, O_O, O_o, o_o
for i in range(1,6):
    mid = ''
    for j in range(i):
	mid += '_'
    if i <= 2:
	neg_emojis.append('O'+mid+'O')
	neg_emojis.append('o'+mid+'O')
	neg_emojis.append('O'+mid+'o')
	neg_emojis.append('o'+mid+'o')
    else:
	very_neg_emojis.append('O'+mid+'O')
	very_neg_emojis.append('o'+mid+'O')
        very_neg_emojis.append('O'+mid+'o')
	very_neg_emojis.append('o'+mid+'o')
 
# Get derived words from given word
def derivedWords(word):
    wordList = [word] 	
    # noun -> adj
    if word.endswith('un'):
	wordList.append(word+'ny')
    elif word.endswith('og'):
	wordList.append(word+'gy')
    elif word.endswith('e'):
	wordList.append(word[0:len(word)-1]+'y')
    else:
	wordList.append(word+'y')

    # for nouns
    if word.endswith('s') or \
       word.endswith('x') or \
       word.endswith('z') or \
       word.endswith('sh') or \
       word.endswith('ch'):
	wordList.append(word+'es')
    elif word.endswith('y'):
	wordList.append(word[0:len(word)-1]+'ies')
    else:
	wordList.append(word+'s')

    # adj -> adv
    if word.endswith('y'):
	wordList.append(word[0:len(word)-1]+'ily')
    else:
	wordList.append(word+'ly')
			
    # verb -> past verb
    if word.endswith('e'):
	wordList.append(word+'d')
    elif word.endswith('y'):
	wordList.append(word[0:len(word)-1]+'ied')
    else:
	wordList.append(word+'ed')
			
    # verb -> ing verb
    if word.endswith('e'):
	wordList.append(word[0:len(word)-1]+'ing')
    else:
	wordList.append(word+'ing')

    # repetive last letters, such as 'happyyyyyy, noooooo, waaaaaaa, etc.'
    for i in range(1,10):
	lastLetters = word[len(word)-1] * i  
	wordList.append(word+lastLetters)
	
    return wordList;

def buildEmotionDict(dict_file):
    # build emotion dictionary from file
    emotion_dict = {}
    with open(dict_file, 'r') as fs:
	lines = fs.readlines()
	for line in lines:
	    words = line.split('\t')[2].split(',')
	    for w in words:
		for dw in derivedWords(w.strip()): # get a list of derived words 
		    emotion_dict[dw] = w.strip() # map derived words to word itself 
    return emotion_dict


def buildWeatherDict(dict_file):
    # build weather dictionary from file
    weather_dict = {}
    with open(dict_file, 'r') as fs:
	lines = fs.readlines()
	for line in lines:
	    category = line.split('\t')[1] 
	    if not category == 'forcast':
		words = line.split('\t')[2].split(',')
		for w in words:
		    weather_dict[w.strip()] = category 
    return weather_dict

# Get sentiment based on emoji found in the given tweet message
def getSentiment(msg): 
    sentiment = '' 
    sentiment_idx = 0 	
    for emoji in pos_emojis:
	if msg.find(emoji) != -1:
	    sentiment = 'positive'     
	    sentiment_idx += 1 # increase sentiment
	    if useFourSentiments:
		for emoji in very_pos_emojis:
		    if msg.find(emoji) != -1:
			sentiment = "very_positive"	
			break
	    break
    for emoji in neg_emojis:
	if msg.find(emoji) != -1:
	    sentiment = 'negative'
	    sentiment_idx -= 1 # decrease sentiment 
	    if useFourSentiments:
		for emoji in very_neg_emojis:
		    if msg.find(emoji) != -1:
			sentiment = "very_negative"
			break
	    break
    if sentiment_idx == 0: # it has both positive and negative sentiment
	return 'neutral'
    else:
	return sentiment

def getMatchedValues(words,word_dict):
    # for each tweets message, get the matched words against dictionary	
    matched_values = []
    for i in range(len(words)-1):
	if words[i].lower() in word_dict.keys():
	    value = word_dict[words[i].lower()] 
	    if value not in matched_values: 
		matched_values.append(value)
    # must be sorted alphatically, so that (c1,c2) and (c2,c1) can be the same
    matched_values.sort() 
    return matched_values

if __name__ == '__main__':

    # start parsing command line parameters
    # must provide at least 3 parameters: dict_type, dict_file and dataset_file
    # can have 4 more optional parameters: 
    #   - 0(default) to use (positive, negative), 1 to use enhanced ones (add very_*) 
    #   - cut count of assoc items (default is 10)  
    #   - cut confidence of assoc rules (default is 0.5)
    #   - 0(default) just output assoc rules, 1 to output tweets msg tegother as well
    if len(sys.argv) < 4:
	print 'Usage: python assoc_mining.py <w|e, w for weather dictionary, e for emotion dictionary> <emotion dict> <data> <0|1, whether to use two|four categories of sentiment> <count of assoc to cut> <assoc condifence to cut (provide in decimal num)> <0|1, output tweets message or not>'
	exit()

    if sys.argv[1] == 'w':
	useWeatherDict = True
    elif sys.argv[1] == 'e':
	useEmotionDict = True
    else:
	raise Exception('4th command line parameter must be \'w\' or \'e\'!')

    dict_file = sys.argv[2]
    dataset_file = sys.argv[3]

    if len(sys.argv) > 4:
	if sys.argv[4] == '1':
	    useFourSentiments = True
	else:
	    pos_emojis.extend(very_pos_emojis)
	    neg_emojis.extend(very_neg_emojis)
    if len(sys.argv) > 5:
	cut_count = int(sys.argv[5])
    if len(sys.argv) > 6:
	cut_confidence = float(sys.argv[6])
    if len(sys.argv) > 7:
	if sys.argv[7] == '1':
	    output_tweets = True

       
    word_dict = {} 
    if useWeatherDict:
	word_dict = buildWeatherDict(dict_file)
    elif useEmotionDict:
	word_dict = buildEmotionDict(dict_file)

    # start mining the associativities based on emoji and emotion dictionary

    one_assoc_dict = {} # (c1,c2) : c1->c2 assoc count 
    one_msg_dict = {} # (c1,c2) : all messages with this associativity inside
    one_count_dict = {} # c1 : c1 count, used to calculate the confidence
     
    two_assoc_dict = {} # ((c1,c2), c3) : c1,c2->c3 assoc count 
    two_msg_dict = {} # ((c1,c2),c3) : all messages with this associativity inside 
    two_count_dict = {} # (c1,c2) : c1,c2 count, used to calculate the confidence 

    """
    three_assoc_dict = {}
    three_msg_dict = {}
    three_count_dict = {}
    """

    with open(dataset_file, 'r') as fs:
	lines = fs.readlines()
	 
	for line in lines:
	    words = line.split('\t')[1].split(',')	
	    sentiment = getSentiment(line.split('\t')[0]) 
	    
	    if sentiment == 'neutral':
		continue
	    
	    matched_values = getMatchedValues(words,word_dict)
	     
	    # mining the one word associativity rules
	    for c in matched_values:
		if c in one_count_dict.keys():
		    one_count_dict[c] = one_count_dict[c] + 1
		else:
		    one_count_dict[c] = 1	
		assoc = (c,sentiment)
		if assoc in one_assoc_dict.keys():
		    one_assoc_dict[assoc] += 1
		else:
		    one_assoc_dict[assoc] = 1 
		if output_tweets:
		    # get the messages releted to this associativity
		    if assoc in one_msg_dict.keys():
			one_msg_dict[assoc].append(line.split('\t')[0])
		    else:
			one_msg_dict[assoc] = [line.split('\t')[0]]

	    # mining the two word associativity rules 
	    for i in range(len(matched_values)):
		for j in range(i+1, len(matched_values)):
		    c1 = matched_values[i]
		    c2 = matched_values[j]	
		    if (c1,c2) in two_count_dict.keys():
			two_count_dict[(c1,c2)] = two_count_dict[(c1,c2)]+1	    
		    else:
			two_count_dict[(c1,c2)] = 1
		    assoc = ((c1,c2),sentiment)
		    if assoc in two_assoc_dict.keys():
			two_assoc_dict[assoc] = two_assoc_dict[assoc] + 1	
		    else:
			two_assoc_dict[assoc] = 1
		    if output_tweets:
			# store the messages related to this associativity
			if assoc in two_msg_dict.keys():
			    two_msg_dict[assoc].append(line.split('\t')[0]) 
			else:
			    two_msg_dict[assoc] = [line.split('\t')[0]]

	    """
	    # mining the three word associativity rules 
	    for i in range(len(matched_values)):
		for j in range(i+1, len(matched_values)):
		    for k in range(j+1, len(matched_values)):
			c1 = matched_values[i]
			c2 = matched_values[j]	
			c3 = matched_values[k]
			if (c1,c2,c3) in three_count_dict.keys():
			    three_count_dict[(c1,c2,c3)] = three_count_dict[(c1,c2,c3)]+1	    
			else:
			    three_count_dict[(c1,c2,c3)] = 1
			assoc = ((c1,c2,c3),sentiment)
			if assoc in three_assoc_dict.keys():
			    three_assoc_dict[assoc] = three_assoc_dict[assoc] + 1	
			else:
			    three_assoc_dict[assoc] = 1
			# store the messages related to this associativity
			if assoc in three_msg_dict.keys():
			    three_msg_dict[assoc].append(line.split('\t')[0]) 
			else:
			    three_msg_dict[assoc] = [line.split('\t')[0]]
	    """

    # print out the results
    for assoc,count in one_assoc_dict.items():
	confidence = count*1.0/one_count_dict[assoc[0]]
	if count > cut_count and confidence > cut_confidence:
	    print assoc[0]+' -> '+assoc[1]+': '+str(count)+' '+ \
		  str(one_count_dict[assoc[0]])+' '+('%.2f' % confidence)
	    if output_tweets:
		print '============================================='
		for msg in one_msg_dict[assoc]:
		    print msg

    for assoc,count in two_assoc_dict.items():
	confidence = count*1.0/two_count_dict[(assoc[0])]
	if count > cut_count and confidence > cut_confidence:
	    print assoc[0][0]+','+assoc[0][1]+' -> '+assoc[1]+': '+ \
		  str(count)+' '+str(two_count_dict[assoc[0]])+' '+('%.2f' % confidence)
	    if output_tweets:	
		print '=============================================='
		for msg in two_msg_dict[assoc]:
		    print msg

    """
    for assoc,count in three_assoc_dict.items():
	confidence = count*1.0/three_count_dict[(assoc[0])]
	if count > cut_count and confidence > cut_confidence:
	    print assoc[0][0]+','+assoc[0][1]+assoc[0][2]+' -> '+assoc[1]+': '+ \
		  str(count)+' '+str(three_count_dict[assoc[0]])+' '+str(confidence)
	    if output_tweets:	
		print '=============================================='
		for msg in three_msg_dict[assoc]:
		    print msg
    """
