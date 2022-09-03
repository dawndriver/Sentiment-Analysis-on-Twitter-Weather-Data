import sys
import emoji_assoc_mining as assoc

emo_dict = assoc.buildEmotionDict(sys.argv[1])

with open(sys.argv[2],'r') as fs:
    contents = fs.readlines()

with open(sys.argv[3],'w') as fs:
    for c in contents:
	msg = c.split('\t')[0]
	sentiment = assoc.getSentiment(msg)
	if sentiment == 'neutral':
	    continue
	fs.write(c.strip()+'\t'+sentiment+'\n')	

