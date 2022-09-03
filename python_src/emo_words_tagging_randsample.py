import sys,os
import random
import emoji_assoc_mining as assoc
import emo_words_tagging as tagging

if len(sys.argv) != 5:
    print 'usage: python emotion_assoc_random_sample.py <emotion dict> <emotion_assoc file> <emotion testing dataset> <output folder_name>'
    exit()

one_word_assoc_dict = {} # word : tweets messages
two_word_assoc_dict = {} # word1,word2 : tweets messages

emo_dict = tagging.emo_dict

with open(sys.argv[2],'r') as fs:
    contents = fs.readlines()
    for c in contents:
	words = c.split(':')[0].split('->')[0].strip().split(',')
	if len(words) == 1:
	    one_word_assoc_dict[words[0]] = []	
	elif len(words) == 2:
	    two_word_assoc_dict[(words[0],words[1])] = [] 
	else:
	    raise Exception('more than 3 words assoc not supported yet!')	

with open(sys.argv[3],'r') as fs:
    contents = fs.readlines()
    for c in contents:
	msg = c.split('\t')[0]
	words =  c.split('\t')[1].split(',')
	matched_values = assoc.getMatchedValues(words, emo_dict)
	word = tagging.getAssocWord(matched_values)	
	if word:
	    if isinstance(word, tuple):
		two_word_assoc_dict[word].append(msg)
	    else: 
	    	one_word_assoc_dict[word].append(msg)

out_dir = sys.argv[4]
if not os.path.exists(out_dir):
    os.mkdir(out_dir)

def writeMsgs(word,msgs,emo_dict):
    if isinstance(word, tuple):
	fname = word[0]+'-'+word[1]+'_'+emo_dict[word]+'.txt'
    else:
	fname = word+'_'+emo_dict[word]+'.txt'
    with open(os.path.join(out_dir,fname),'w') as fs:
	if len(msgs) < 50:
	    for msg in msgs:
		fs.write(msg+'\t'+emo_dict[word]+'\n')
	else:
	    for i in random.sample(range(len(msgs)), 50):
		fs.write(msgs[i]+'\t'+emo_dict[word]+'\n')

for word,msgs in one_word_assoc_dict.items():
    writeMsgs(word,msgs,tagging.one_word_emo_dict) 

for word,msgs in two_word_assoc_dict.items():
    writeMsgs(word,msgs,tagging.two_word_emo_dict)

