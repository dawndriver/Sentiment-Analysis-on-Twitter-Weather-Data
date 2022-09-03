import sys
import random
import emoji_assoc_mining as assoc

"""
negation_words = ['not', 'never', 'none', 'nothing', 'hardly', 'neither', 'nor', 'won\'t', 'wont', 'aren\'t', 'arent', 'ain\'t', 'aint', 'isn\'t', 'isnt', 'don\'t', 'dun', 'dunt', 'dont', 'doesn\'t', 'doesnt', 'haven\'t', 'havent', 'hasn\'t', 'hasnt', 'wouldn\'t', 'wouldnt', 'can\'t', 'cant', 'cannot', 'couldn\'t', 'couldnt', 'shouldn\'t', 'shouldnt', 'didn\'t', 'didnt']
"""

one_word_emo_dict = {}
one_word_confidence = {}
two_word_emo_dict = {}
two_word_confidence = {}

emo_dict = assoc.buildEmotionDict(sys.argv[1])

with open(sys.argv[2],'r') as fs:
    contents = fs.readlines()
    for c in contents:
	words = c.split(':')[0].split('->')[0].strip().split(',')
	confidence = c.split(':')[1].strip().split(' ')[2]
	sentiment = c.split(':')[0].split('->')[1].strip()
	if len(words) == 1:
	    one_word_emo_dict[words[0]] = sentiment 
	    one_word_confidence[words[0]] = float(confidence)
	elif len(words) == 2:
	    two_word_emo_dict[(words[0],words[1])] = sentiment 
	    two_word_confidence[(words[0],words[1])] = float(confidence)
	else:
	    raise Exception('more than 3 words assoc not supported yet!')

def matchTwoWordAssoc(matched_values):
    matched = (None, 0)
    for i in range(len(matched_values)):
	for j in range(len(matched_values)): 
	    c1 = matched_values[i]
	    c2 = matched_values[j]
	    if (c1,c2) in two_word_emo_dict.keys():
		# Select the words with higher confidence
		if two_word_confidence[(c1,c2)] > matched[1]:
		    matched = ((c1,c2),two_word_confidence[(c1,c2)])
    return matched 

def matchOneWordAssoc(matched_values):
    matched = (None, 0)   
    for c in matched_values:
	if c in one_word_emo_dict.keys():
	    if one_word_confidence[c] > matched[1]:
		matched = (c,one_word_confidence[c]) 	
    return matched

# return one_word or two_word or None
def getAssocWord(matched_values):
    (two_word, two_word_c) = matchTwoWordAssoc(matched_values)
    (one_word, one_word_c) = matchOneWordAssoc(matched_values)
    if one_word and two_word:
	if one_word not in two_word: # if matched two_word does not contain matched one_word
	    if one_word_c > two_word_c:
		return one_word
	    else:
		return two_word
	else:  # otherwise, use two-word in priority
	    return two_word
    elif one_word: # only has one_word matched
	return one_word
    elif two_word: # only has two_word matched
	return two_word 
    else:
	return None

if __name__ == '__main__':

    if len(sys.argv) != 5:
	print 'usage: python emotion_assoc_random_sample.py <emotion dict> <emotion_assoc file> <emotion testing dataset> <output filename>'
	exit()

    with open(sys.argv[3],'r') as fs:
	contents = fs.readlines()

    with open(sys.argv[4],'w') as fs:
	for c in contents:
	    msg = c.split('\t')[0]
	    words =  c.split('\t')[1].split(',')
	    matched_values = assoc.getMatchedValues(words, emo_dict)
	    word = getAssocWord(matched_values)
	    if word:
		if isinstance (word, tuple):
		    emotion = two_word_emo_dict[word]
		else:
		    emotion = one_word_emo_dict[word]
		fs.write(c.strip()+'\t'+emotion+'\n')	

