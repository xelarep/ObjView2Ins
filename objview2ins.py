# Read Export from ObjView generated tableExport.txt Multi Object List, and extract Multi Names
#
# BBB, 03-JUL-2021

from datetime import datetime

insname = [] 						# create and empty list for multi Names
for idx in range (0, 1024+128):     # additional page for Multi 2048...
	insname.append('-')				# marker for empty multi 

with open('tableExport.txt') as inputfile:
	mylines = inputfile.readlines()
	inputfile.close()

	for cur_line in mylines:
		splitline = cur_line.split(',')
		multi = splitline[1]					# multi number (1025...2048) 
		name = splitline[2].replace('"','')		# read name and kick out "
		
		if multi != 'ID#':
			idx = int(multi)
			insname[idx-1024] = name

# Create ins.file
outfile = open ('fortese.ins','w') 
outfile.write(";Fortse SE Multi INS file\n")
outfile.write(datetime.now().strftime("%d.%m.%Y - %H:%M:%S")+"\n\n")

# Create Patch Names
outfile.write(".Patch Names\n")

midx = 1024
for banks in range(0,9):
	outfile.write("\n[User " + str(banks+1) + " ("+str(midx)+"-"+str(midx+127)+")]\n")
	for ridx in range(0,128):
		outfile.write(str(ridx)+"="+str(midx)+": "+insname[midx-1024]+"\n")
		midx = midx + 1

# Write instrument definition (we leave out the controllers)
outfile.write("\n.Instrument Definitions\n")
outfile.write("[Kurzweil Forte SE]\n")
outfile.write("BankSelectMethod=2  ; Controller 32 only\n")

midx = 1024
for idx in range(0,9):
	outfile.write("Patch["+f'{idx+8:03}'+"]=User " + str(idx+1) + " ("+str(midx)+"-"+str(midx+127)+")\n")
	midx = midx + 128

outfile.close()
