import numpy as np
import csv
import sys
import random
reload(sys)
sys.setdefaultencoding('utf-8')

class fqd_elem:
    def __init__(self, word):
        self.w = word
        self.mean_kor = list()
        self.mean_eng = list()
        self.exam_stc = list()
        self.num_ref = 0
        self.num_rem = 0		

	def namew(self, word):
		self.w = word
    
    def ref_inc(self):
        self.num_ref += 1
 
    def rem_half(self):
		self.num_rem = self.num_rem / 2
	
	def rem_inc(self):
		self.num_rem += 1

    def inf_add(self, part, info):
        if part == "KOR":
            self.mean_kor.append(info)
        elif part == "ENG":
            self.mean_eng.append(info)
        elif part == "STC":
            self.exam_stc.append(info)
    
    def inf_mod(self, part, ind, info):
        if part == "KOR":
            self.mean_kor[ind] = info
        elif part == "ENG":
            self.mean_eng[ind] = info
        elif part == "STC":
            self.exam_stc[ind] = info
    
    def num_ref_mod(self, num):
        self.num_ref = num

    def num_rem_mod(self, num):
        self.num_rem = num
        
    def info_print(self):
        print ("\nWORD : " + self.w)
        print ("Num. of ref : %d"%(self.num_ref))
        for i in range(len(self.mean_kor)):
            print ("KOR %d: %s"%(i+1, self.mean_kor[i]))
        for i in range(len(self.mean_eng)):
            print ("ENG %d: %s"%(i+1, self.mean_eng[i]))
        for i in range(len(self.exam_stc)):
            print ("STC %d: %s"%(i+1, self.exam_stc[i]))
        print ("\n")
    
class fqdict:
    
    def __init__(self):
        self.filename = "fqdata.txt"
        self.fqdict = dict()
    
    def currentfile(self):
        print ("Currently %s is loaded"%(self.filename))
        
    def write_save(self, fn = ""):
        if fn == "":
            fn = self.filename
        opendir = "./" + fn
        f = open(opendir, 'w')
        for w in list(self.fqdict.keys()):
            f.write('#####\n')
            f.write('$WRD %s\n'%(w))
            f.write('$REF %d\n'%(self.fqdict[w].num_ref))
			f.write('$REM %d\n'%(self.fqdict[w].num_rem))
            for i in range(len(self.fqdict[w].mean_kor)):
                f.write('$KOR %s\n'%(self.fqdict[w].mean_kor[i]))
            for i in range(len(self.fqdict[w].mean_eng)):
                f.write('$ENG %s\n'%(self.fqdict[w].mean_eng[i]))
            for i in range(len(self.fqdict[w].exam_stc)):
                f.write('$STC %s\n'%(self.fqdict[w].exam_stc[i]))
        f.close()
    
    def chk_noword(self, nw):
        if nw == "":
            print ("No $WRD found!\nThis may cause error afterwards.")
            
    def chk_ask(self, qst):
        ask = ""
        while ask != 'y' and ask != 'n' and ask != 'Y' and ask != 'N':
            ask = raw_input(qst)
#            ask = ask[:-1]
        return ask
    
    def read_load(self, fn = ""):
        if fn == "":
            fn = self.filename
        try:
            opendir = "./" + fn
            f = open(opendir, 'r')
            newword = ""
            for line in f:
                if line[0] == '#':
                    newword = ""
                elif line[0:4] == '$WRD':
                    newword = line[5:-1]
                    print ("Found %s"%(newword))
                    if len(newword) > 0:
                        self.fqdict[newword] = fqd_elem(newword)
				elif line[0:4] == '$REM':
					self.chk_noword(newword)
                    newinfo = line[5:-1]
                    if len(newinfo) > 0:
                        self.fqdict[newword].num_rem_mod(int(newinfo))
                elif line[0:4] == '$KOR':
                    self.chk_noword(newword)
                    newinfo = line[5:-1]
                    if len(newinfo) > 0:
                        self.fqdict[newword].inf_add("KOR", newinfo)
                elif line[0:4] == '$ENG':
                    self.chk_noword(newword)
                    newinfo = line[5:-1]
                    if len(newinfo) > 0:
                        self.fqdict[newword].inf_add("ENG", newinfo)
                elif line[0:4] == '$STC':
                    self.chk_noword(newword)
                    newinfo = line[5:-1]
                    if len(newinfo) > 0:
                        self.fqdict[newword].inf_add("STC", newinfo)
                elif line[0:4] == '$REF':
                    self.chk_noword(newword)
                    newinfo = line[5:-1]
                    if len(newinfo) > 0:
                        self.fqdict[newword].num_ref_mod(int(newinfo))
                else:
                    print ("End of the line or something else happened??")
            f.close()
        except:
            print ("\nNo %s found, so created one.\nIf you already have database with different name,\nuse LOAD.\n"%(fn))
            opendir = "./" + fn
            f = open(opendir, 'w')
            f.close()
    
    def newload(self):
        self.write_save()
        self.filename = raw_input("what is the name of the file?: ")
        self.fqdict = dict()
        self.read_load()
    
    def fqsearch(self):
        word = raw_input("Search: ")
        if word in self.fqdict:
            self.fqdict[word].ref_inc()
            self.fqdict[word].info_print()
            addinfo = self.chk_ask("Add info to %s?(y/n): "%(word))
            if addinfo == 'y' or addinfo == 'Y':
                while(True):
                    addinfo = raw_input("KOR mean(Q to skip): ")
                    if addinfo == 'Q':
                        break
                    else:
                        self.fqdict[word].inf_add("KOR", addinfo)
                while(True):
                    addinfo = raw_input("ENG mean(Q to skip): ")
                    if addinfo == 'Q':
                        break
                    else:
                        self.fqdict[word].inf_add("ENG", addinfo)
                while(True):
                    addinfo = raw_input("Example sentence(Q to skip): ")
                    if addinfo == 'Q':
                        break
                    else:
                        self.fqdict[word].inf_add("STC", addinfo)
        else:
            print ("Word %s not found in the dataset"%(word))
            addword = self.chk_ask("\nInsert %s into the dataset?(y/n): "%(word))
            if addword == 'y' or addword == 'Y':
                print ("")
                self.fqdict[word] = fqd_elem(word)
                while(True):
                    addinfo = raw_input("KOR mean(Q to skip): ")
                    if addinfo == 'Q':
                        break
                    else:
                        self.fqdict[word].inf_add("KOR", addinfo)
                while(True):
                    addinfo = raw_input("ENG mean(Q to skip): ")
                    if addinfo == 'Q':
                        break
                    else:
                        self.fqdict[word].inf_add("ENG", addinfo)
                while(True):
                    addinfo = raw_input("Example sentence(Q to skip): ")
                    if addinfo == 'Q':
                        break
                    else:
                        self.fqdict[word].inf_add("STC", addinfo)
                        
fqd = fqdict()
fqd.read_load()
while(True):
    print ("\n### freqlearner ###")
    fqd.currentfile()
    print ("###################")
    print ("1: Search / Insert word / Add info to a word")
    print ("2: Save")
    print ("3: Save current & Load")
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
        
        
