#!/usr/bin/env python

from korg import LineGrokker, PatternRepo

if __name__ == '__main__':
	# load the pattern map
	#pr = PatternRepo(['./patterns/'])
	pr = PatternRepo([])
	lg = LineGrokker('%{COMBINEDAPACHELOG}', pr)

	# now grok the apache access log
	with open("/home/mark/devel/aogaeru/korg/research/access_petsy_2013_php.log.1") as infile:
	    for line in infile:
	        print lg.grok(line)['response']
