#!/usr/bin/env python3
import struct
import sys
import random
import re
import argparse
import math

parser = argparse.ArgumentParser()
parser.add_argument("src", help="ply file")
parser.add_argument("-o", help="dest file")
parser.add_argument("--min",nargs=3,type=float,help="min axis")
parser.add_argument("--max",nargs=3,type=float,help="max axis")
parser.add_argument("--center",nargs=3,type=float,help="center axis")
#parser.add_argument("--scale",type=float,default=1,help="scale")
parser.add_argument("--rot",type=float,default=0,help="rotation Y")
parser.add_argument("--random",type=float,default=1,help="mabiki")
args = parser.parse_args()
#print(args) 

fp = open(args.src,"rb") ;

# read header
delimiter = "end_header\n" 
head = fp.read(2000) 
delimiter_index = head.find(delimiter.encode('utf-8'))+len(delimiter)
text_data = head[:delimiter_index]
heads = text_data.decode('utf-8').split("\n") 
hn = [] 
pack = "<" 
hs = 0 
evidx = 0
for idx, l in enumerate(heads[0:-1]):
	match = re.search('property ([^ ]+) (.+)',l)
	if match != None : 
		type,name = match.group(1,2)
		hn.append(name) 
		if type=="float": 
			pack += "f" 
			hs += 4 
		if type=="double": 
			pack += "d" 
			hs += 8
		if type=="uchar": 
			pack += "B" 
			hs += 1 
	elif re.search('^element vertex ',l):
		evidx = idx
print(f'Loading {args.src}')
#print(hn)
#print(hs) 

# read points data
fp.seek(delimiter_index)
tc = 0
ec = 0 
sx = sy = sz = 10000
ex = ey = ez = -10000
bd = bytearray()
while True:
	buf = fp.read(hs)
	if len(buf)<hs : break 
	tc+= 1 
	prop =  list(struct.unpack(pack,buf))
	x = prop[hn.index('x')]
	y = prop[hn.index('y')]
	z = prop[hn.index('z')]
#	print(prop[hn.index('scale_0')],prop[hn.index('scale_1')],prop[hn.index('scale_2')])

	if args.rot != 0:
		rad = math.radians(args.rot)
		xx = x * math.cos(rad) + z * math.sin(rad)
		z = x * -math.sin(rad) + z * math.cos(rad) 
		x = xx 
		# qwpx - qypz, qwpy + qypw, qypx + qwpz, -qypy + qwpw 
		qy = -math.sin(rad/2) 
		qw = math.cos(rad/2)  
		px = prop[hn.index('rot_0')]
		py = prop[hn.index('rot_1')]
		pz = prop[hn.index('rot_2')]
		pw = prop[hn.index('rot_3')]
		prop[hn.index('rot_0')] = qw*px - qy*pz
		prop[hn.index('rot_1')] = qw*py + qy*pw
		prop[hn.index('rot_2')] = qy*px + qw*pz
		prop[hn.index('rot_3')] = -qy*py + qw*pw 

	if args.center != None:
		x -= args.center[0]
		y -= args.center[1]
		z -= args.center[2]
		
		#	if args.scale != None:
		#		x *= args.scale 
		#		y *= args.scale 
		#		z *= args.scale 
		#		prop[hn.index('scale_0')] *= args.scale 
		#		prop[hn.index('scale_1')] *= args.scale 
		#		prop[hn.index('scale_2')] *= args.scale 

	
	if args.min != None:
		if(x<args.min[0] or  y<args.min[1]  or  z<args.min[2]  ): continue ;
	if args.max != None:
		if(x>args.max[0] or  y>args.max[1]  or  z>args.max[2]  ): continue ;
	if args.random!=1 and random.random()>args.random : continue ;
		
	if sx > x : sx = x 
	if sy > y : sy = y 
	if sz > z : sz = z 
	if ex < x : ex = x  
	if ey < y : ey = y 
	if ez < z : ez = z 

	prop[hn.index('x')] = x 
	prop[hn.index('y')] = y 
	prop[hn.index('z')] = z 		
	ob = struct.pack(pack,*prop)
	ec += 1 
	bd += ob

print("src points %d" % (tc) )
print("%f,%f,%f - %f,%f,%f  %f,%f,%f" % (sx,sy,sz,ex,ey,ez,ex-sx,ey-sy,ez-sz))

if args.o != None:
	print("out %s" % args.o)
	print("out points %d" % (ec) )	
	fop = open(args.o ,"wb")
	heads[evidx] = "element vertex %d" % ec 
#	print(heads)
	for l in heads[0:-1]:
		fop.write((l+"\n").encode("utf-8"))
# write points data
	fop.write(bd) 
	fop.close() 