import sys
import random
from fqm_dist import *
reload(sys)
sys.setdefaultencoding('utf-8')
		
fqd = fqdict()
fqd.read_load()
while(True):
	print ("\n### freqlearner ###")
	fqd.currentfile()
	fqd.currentwords()
	print ("###################")
	print ("1: Search / Insert word / Add info to a word")
	print ("2: Save")
	print ("3: Save current & Load another dataset")
	print ("4: Review")
	print ("Q: Quit after Saving")
	print ("qq: Quit WITHOUT saving")
	command = raw_input("\nChoose what to do: ")
	
	if command == "Q":
		fqd.write_save()
		break
	elif command == '1':
		fqd.fqsearch()
	elif command == '2':
		fqd.write_save()
	elif command == '3':
		fqd.newload()
	elif command == '4':
		fqd.review()
	elif command == 'qq':
		break
	else:
		print ("Wrong input, try again\n")
		
		
