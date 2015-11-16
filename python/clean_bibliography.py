#! /usr/bin/python
import sys
import os
import argparse

#######################################################################################
# Modify a bibtex file created by Mendeley. Remove fields of choosing (such as month,
# issue number) and replace journal titles with journal abbreviations
# Arguments:
#	file1 - name of bibtex file you want to change
#	file2 - name of journal abbreviation file. Each line should contain the journal title
#			followed by one tab and the journal abbreviation. An example of this file is located
#			in /home/pjanowsk/.local/share/data/Mendeley Ltd./Mendeley Desktop/journalAbbreviations/default.txt
#			Also copy in ~/scripts/python
# Return:
#	 Clean bibtex file in the same directory as file1 and name file1name_clean.bib
########################################################################################

parser = argparse.ArgumentParser()
parser.add_argument("file1", help="name of file bibtex file (extension .bib)")
parser.add_argument("file2", help="name of journal abbreviation file")
args = parser.parse_args()

########################################################################
# CREATE JOURNAL TITLE AND ABBREVIATION DICTIONARY                     #
########################################################################
abbrev_dict={}
abbrev_file=open(args.file2, 'r')
for line in abbrev_file:
	line=line.strip().split('\t')
	abbrev_dict[line[0].lower()]=line[1]
abbrev_file.close()


########################################################################
# OPEN FILES        			                                       #
########################################################################
fin=open(args.file1,'r')
fout=args.file1[:-4]
fout=fout+'_clean.bib'
fout=open(fout,'w')

########################################################################
# CREATE NEW FILE								                       #
########################################################################
for line in fin:
	# REMOVE FIELDS YOU DON'T WANT
	if line.startswith('month =') or line.startswith('number ='):
		continue
	# REPLACE JOURNAL TITLES WITH ABBREVIATIONS	
	if line.startswith('journal ='):
		brk1=line.index('{')
		brk2=line.index('}')
		title_old=line[brk1+1:brk2].lower()
		if title_old in abbrev_dict.keys():
			title_new=abbrev_dict[title_old]
			line=line[:brk1+1]+title_new+line[brk2:]
		#IF JOURNAL TITLE NOT IN ABBREVIATION LIST, PRINT IT ON THE COMMAND LINE
		else:
			print title_old
	fout.write(line)
	
########################################################################
# CLOSE FILES        			                                       #
########################################################################
fin.close()
fout.close()
