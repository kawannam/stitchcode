#!/usr/bin/env python
#######################################
#
# renders an EXP embroidery file as a PNG image
#
# author:(c) Michael Aschauer <m AT ash.to>
# www: http:/m.ash.to
# licenced under: GPL v3
# see: http://www.gnu.org/licenses/gpl.html
#
#######################################

from PIL import Image
import stitchcode
import getopt
import sys

def usage():
	print """
usage: svg2exp.py [options] -i SVG-FILE -o EXP-FILE

renders an EXP embroidery file as a PNG image

options:
    -h, --help              print usage
    -i, --input=FILE        input SVG file
    -o, --output=FILE       output EXP file
    -z, --zoom=FACTOR       zoom in/out
"""

infile = "";
outfile = "";
zoom = 1
show_stitches = False

def process_args():
	global infile, outfile, zoom, show_stitches
	
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hi:o:z",
			["help", "input=","output=","zoom="])
	except getopt.GetoptError, err:
		# print help information and exit:
		print str(err) # will print something like "option -a not recognized"
		usage()
		sys.exit(2)

	for o, a in opts:
		if o in ("-h", "--help"):
			usage()
			sys.exit()
		elif o in ("-o", "--output"):
			outfile = a
		elif o in ("-i", "--input"):
			infile = a
		elif o in ("-z", "--zoom"):
			zoom = float(a)
		else:
			usage()
			sys.exit()

	if len(infile) == 0:
		print "options required."
		usage()
		sys.exit(2)
		

if __name__ == '__main__':
	process_args()
	
	if not outfile:
		outfile = "%s.exp" % infile[:-4] 
	emb = stitchcode.Embroidery()
	emb.import_svg(infile)
	emb.scale(zoom)
	emb.save_as_exp(outfile)

		
