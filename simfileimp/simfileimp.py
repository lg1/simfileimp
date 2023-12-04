

import gzip
import sys, os, subprocess
import numpy as np



ARG_VIDEO_FORMAT={'rb','rtxt'}




def readGZvideo(dir,prefix,start,stop,dimx,dimy,mult=1,format='rtxt'):

	if format not in ARG_VIDEO_FORMAT:
		raise ValueError("format arguments should be either %r." % ARG_VIDEO_FORMAT)


	directory = dir
	arrayvideo=np.empty([1,dimx,dimy])
	for i in range(start,stop,mult):
		if i<10:
 			file = prefix+"000"+str(i)+".gz"
 
		if i<100 and i>=10:
			file = prefix+"00"+str(i)+".gz"
 	
		if i<1000 and i>=100:
			file = prefix+"0"+str(i)+".gz"
		if i>1000:
			file = prefix+str(i)+".gz"
		filepath = directory + file
		if os.access(filepath, os.R_OK)==True:
			if format=='rtxt':	
				imgdatatxt=gzip.open(filepath,"r")
				imgdata=np.loadtxt(imgdatatxt).reshape(1,dimx,dimy)
				arrayvideo=np.append(arrayvideo,imgdata,axis=0)

			if format=='rb':
				with gzip.open(filepath, 'rb') as f:
					imgdata = np.frombuffer(f.read(), dtype=np.uint8).reshape(1,dimx,dimy)
				arrayvideo=np.append(arrayvideo,imgdata,axis=0)
		else: 
			print("the next dataimage is not found:", file)
			break		
	return arrayvideo[1:]

def readPoint(dir, filename="log_AP.txt"):
	
	signal=[]
	filepath=dir+filename

	if os.access(filepath, os.R_OK)==True:	
		imgdatatxt=open(filepath,"r")
		signal=np.loadtxt(imgdatatxt)

	return signal


		
def openinIJ(dir,start,stop,dimx,dimy,mult,pathscript,IJhandle="ImageJ-win64.exe",format='rb',prefix="PictureVoltageData"):

	if format not in ARG_VIDEO_FORMAT:
		raise ValueError("format arguments should be either %r." % ARG_VIDEO_FORMAT)

	scriptOptStr=" startparam="+str(start)+","+" "+"stopparam="+str(stop)+","+" "
	scriptOptStr=scriptOptStr+"multparam="+str(mult)+","+" "+"dimxparam="+str(dimx)+","+" "+"dimyparam="+str(dimy)+","+" "
	scriptOptStr=scriptOptStr+"pathparam="+"'"+dir+"'"+","+" "+"formatparam="+"'"+format+"'"+","+" "+"prefixparam="+"'"+prefix+"'"+" "

	options=[]
	options.extend([IJhandle]) 
	options.extend(["--ij2","--run"]) 
	options.extend([pathscript,scriptOptStr, "&"])
	subprocess.Popen(options)

