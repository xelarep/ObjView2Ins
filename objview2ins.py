# Read Export from ObjView generated tableExport.txt Multi Object List, and extract Multi Names
#
# ObjectView 0.98b beta by Brian Cowell, Mastering VAST forum --> https://forums.godlike.com.au
# Rename .FSE to .FOR, open and ignore version errors, select MULTI and export as TXT 
#
# BBB, 03-JUL-2021
#
# 09-JUL-2021 - removed Bank 9
# 08-JAN-2022 - added single line CSV for GP Script macro

from datetime import datetime
import os

fullINS = False										# build a complete file (True) or reduced (False)

patchnames = [] 									# create and empty list for multi Names
bankactive = []

# Create an empty list
#for idx in range (0, 1024 +128):     				# additional page for Multi 2048...
for idx in range (0, 1024):     				
	patchnames.append('-')							# marker for empty multi 
#for idx in range(0,10):
for idx in range(0,9):
	bankactive.append(fullINS)

with open('tableExport.txt') as inputfile:			# import ObjView output txt-file from ObjView 
	linesread = inputfile.readlines()
	inputfile.close()

	for cur_line in linesread:
		splittedline = cur_line.split(',')
		multi = splittedline[1]						# multi number (1025...2048) as string
		name = splittedline[2].replace('"','')		# get multi-name and kick out "
		
		if multi != 'ID#':							# skip table header...
			idx = int(multi)
			patchnames[idx-1024] = name

# Create ins.file
if fullINS == True:
	outfile = open (os.path.expanduser('~/Documents/Gig Performer/INS/forte-se-full.ins'),'w') 
else:
    outfile = open (os.path.expanduser('~/Documents/Gig Performer/INS/forte-se.ins'),'w')  

outfile.write(";Fortse SE Multi INS file\n")
outfile.write(datetime.now().strftime("%d.%m.%Y - %H:%M:%S")+"\n\n")

# Create Patch Names
outfile.write(".Patch Names\n")

#for patchbank in range(0,9):
for patchbank in range(0,8):
	if fullINS == False:									# check if selected bank got entries before writing the bank header...
		for idx in range(0,128):
			if patchnames[patchbank*128 + idx] != '-':
				bankactive[patchbank] = True

	if bankactive[patchbank] == True:
		outfile.write("\n[User " + str(patchbank+1) + " ("+str(patchbank*128  + 1024)+"-"+str(patchbank*128 +1024+127)+")]\n")
		for idx in range(0,128):
			if patchnames[patchbank*128 + idx] != '-' or fullINS == True:
				outfile.write(str(idx)+"="+str(patchbank*128 + idx + 1024)+": "+patchnames[patchbank*128 + idx]+"\n")

# Write instrument definition (we leave out the controllers)
outfile.write("\n.Instrument Definitions\n")
outfile.write("[Kurzweil Forte SE]\n")
outfile.write("BankSelectMethod=2  ; Controller 32 only\n")

#for idx in range(0,9):
for idx in range(0,8):
	if bankactive[idx] == True:
		outfile.write("Patch["+f'{idx+8:03}'+"]=User " + str(idx+1) + " ("+str(idx*128+1024)+"-"+str(idx*128+1024+127)+")\n")

outfile.close()

# create a single line CSV file for FindPresetName() GPscript function...
csvfile = open (os.path.expanduser('~/Documents/Gig Performer/INS/forte-se.csv'),'w')
for idx in range(0,1023):
    csvfile.write(f'{idx+1025:04}'+','+patchnames[idx+1]+',')

csvfile.write("2048,EOF\n")      # needed to determine last entry...
csvfile.close()
