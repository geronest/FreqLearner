import random

class fqd_elem:
	def __init__(self, word):
		self.w = word
		self.mean_kor = list()
		self.mean_eng = list()
		self.exam_stc = list()
		self.num_ref = 0
		self.num_rem = 0		
		self.num_fgt = 0

	def namew(self, word):
		self.w = word
	
	def ref_inc(self):
		self.num_ref += 1
 
	def ref_half(self):
		self.num_ref = self.num_ref / 2
	
	def rem_inc(self):
		self.num_rem += 1
	
	def rem_zero(self):
		self.num_rem = 0
	
	def fgt_inc(self):
		self.num_fgt += 1

	def fgt_dec(self):
		self.num_fgt -= 1

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
	
	def num_fgt_mod(self, num):
		self.num_fgt = num
		
	def info_print(self, wd = True, nums = True, kor = True, eng = True, stc = True):
		if wd:	
			print ("\nWORD : " + self.w)
		if nums:
			print ("Num. of ref: %d"%(self.num_ref))
			print ("Num. of successive remembrance: %d"%(self.num_rem))
			print ("Num. of failed remembrance: %d"%(self.num_fgt))
		if kor:
			for i in range(len(self.mean_kor)):
				print ("KOR %d: %s"%(i+1, self.mean_kor[i]))
		if eng:
			for i in range(len(self.mean_eng)):
				print ("ENG %d: %s"%(i+1, self.mean_eng[i]))
		if stc:
			for i in range(len(self.exam_stc)):
				print ("STC %d: %s"%(i+1, self.exam_stc[i]))
		print ("\n")
	
class fqdict:
	
	def __init__(self):
		self.filename = "fqdata.txt"
		self.filedir = "./fqdata/"
		self.fqdict = dict()
	
	def currentfile(self):
		print ("Currently %s is loaded"%(self.filename))
	
	def currentwords(self):
		print ("Currently %d words are saved"%(len(self.fqdict.keys())))
		
	def write_save(self, fn = ""):
		if fn == "":
			fn = self.filename
		opendir = self.filedir + fn
		f = open(opendir, 'w')
		for w in list(self.fqdict.keys()):
			f.write('#####\n')
			f.write('$WRD %s\n'%(w))
			f.write('$REF %d\n'%(self.fqdict[w].num_ref))
			f.write('$REM %d\n'%(self.fqdict[w].num_rem))
			f.write('$FAI %d\n'%(self.fqdict[w].num_fgt))
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
#			ask = ask[:-1]
		return ask
	
	def read_load(self, fn = ""):
		if fn == "":
			fn = self.filename
		try:
			opendir = self.filedir + fn
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
				elif line[0:4] == '$FAI':
					self.chk_noword(newword)
					newinfo = line[5:-1]
					if len(newinfo) > 0:
						self.fqdict[newword].num_fgt_mod(int(newinfo))
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
			opendir = self.filedir + fn
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

	def review(self):
	
		def howmanyw():
			wnum = input("How many words?: ")
			return wnum
		
		def q_word(word, rtype):
			self.fqdict[word].info_print(nums = False, eng = False, kor = False)	
			ans = self.chk_ask("Do you remember this word?(y/n): ")
			if ans == 'y' or ans == 'Y':
				print ("Congratulations! you remembered this word")
				if rtype == 'REF' or rtype == 'RAN':
					self.fqdict[word].rem_inc()
					if self.fqdict[word].num_rem > 4:
						self.fqdict[word].ref_half()
						self.fqdict[word].rem_zero()
				elif rtype == 'MEM':
					if self.fqdict[word].num_fgt > 0:
						self.fqdict[word].fgt_dec()

			elif ans == 'n' or ans == 'N':
				print ("You need to check meanings.")
				self.fqdict[word].info_print(nums = False)
				if rtype == 'REF' or rtype == 'RAN':
					self.fqdict[word].rem_zero()
					self.fqdict[word].ref_inc()
				elif rtype == 'MEM':
					self.fqdict[word].fgt_inc()

		def listwds(wl, rtype):
			print ("*** List of words you will review ***")
			for i in range(len(wl)):
				if rtype == 'REF' or rtype == 'MEM':
					print wl[i][0]
				elif rtype == 'RAN':
					print wl[i]
			print("**************************************")
			ans = raw_input("Press ENTER to continue")

		def reffreq():
			print ("\n# REF.FREQ based REVIEW #")
			wn = howmanyw()
			wlist = list()
			for wd in list(self.fqdict.keys()):
				print wlist
				if len(wlist) == 0: wlist.append([wd, self.fqdict[wd].num_ref])
				for i in range(len(wlist)):
					if wlist[i][1] <= self.fqdict[wd].num_ref:
						wlist.insert(i, [wd, self.fqdict[wd].num_ref])
						if wn < len(wlist):
							wlist.pop()
						break
			listwds(wlist, 'REF')
			for wd in wlist:
				q_word(wd[0], 'REF')
				ans = raw_input('Press ENTER to continue')
			
			print ("\n# REVIEW FINISHED #")

		def memfail():
			print ("\n# MEM.FAIL based REVIEW #")
			wn = howmanyw()
			wlist = list()
			for wd in list(self.fqdict.keys()):
				if len(wlist) == 0: wlist.append([wd, self.fqdict[wd].num_fgt])
				for i in range(len(wlist)):
					if wlist[i][1] <= self.fqdict[wd].num_fgt:
						wlist.insert(i, [wd, self.fqdict[wd].num_fgt])
						if wn < len(wlist):
							wlist.pop()
						break

			listwds(wlist, 'MEM')
			for wd in wlist:
				q_word(wd[0], 'MEM')
				ans = raw_input('Press ENTER to continue')
			
			print ("\n# REVIEW FINISHED #")
		
		def ranword():
			print ("\n# RAN.WORD based REVIEW #")
			wn = howmanyw()
			wlist = list()
			klist = list(self.fqdict.keys())
			random.shuffle(klist)
			for i in range(wn):
				wlist.append(klist[i])
			listwds(wlist, 'RAN')
			for wd in wlist:
				q_word(wd, 'RAN')
				ans = raw_input('Press ENTER to continue')
			
			print ("\n# REVIEW FINISHED #")

		while(True):
			print ("\n### REVIEW MODE ###")
			print ("1: Reference frequency based")
			print ("2: Words you often failed to memorize")
			print ("3: Random words")
			print ("Q: Quit review mode")
			command = raw_input("\nWhat mode do you want?: ")

			if command == "Q":
				break
			elif command == "1":
				reffreq()
			elif command == "2":
				memfail()
			elif command == "3":
				ranword()

			
