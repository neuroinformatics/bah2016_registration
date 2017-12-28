#!/usr/bin/env python
#coding: UTF-8

#
# Brain Atlas Hackthon
# ---------------------------------------------------------
#

import os
import shutil
import sys
import math
import dircache


#HomeDir = "/home/ikeno/BAH/"
FijiBin = " /share/apps/registration/fiji/fiji-linux64"
FijiMacroDir = "/data/miyamoto/git/bah2016_registration/fiji_macros/"

InputFileDir1 = "./SB_bin/"
InputFileDir2 = "./work3/"

OutputFileDir = "./work5/"
PickedFileDir = "./work4_picked/"
GrayFileDir = "./work4/"
ColorFileDir = "./work3/"



# pickup arguments

argvs = sys.argv
argc = len(argvs)

# 

fileName1 = argvs[1]
outputDir = fileName1.split(".tif")

#
# ----- Execute
#

MetricFile = "summarize_metric.txt"

fin = open(MetricFile)
for line in fin:
    if fileName1 in line:
        slice = line.split(",")
        min_slice = slice[1]
        min_image = '%04d.tif' % int(slice[1])

print(outputDir[0] + ': ' + min_image)

shutil.copyfile(GrayFileDir+outputDir[0]+'/'+min_image, PickedFileDir + outputDir[0] + '.tif')

# registration color image
grayFilePath = GrayFileDir+outputDir[0]+'/'+min_image
colorFilePath = ColorFileDir+fileName1
outputFilePath = OutputFileDir+fileName1

fr = open(FijiMacroDir+"registColor.ijm.org", 'r')
lines = fr.readlines()
fr.close()

fw = open(FijiMacroDir+"registColor.ijm", 'w')
numOfLines = len(lines)
for i in range(0,numOfLines):
    line = lines[i].split()
    strLine = " ".join(line)

    strLine = strLine.replace("#GrayFilePath#", grayFilePath)
    strLine = strLine.replace("#ColorFilePath#", colorFilePath)
    strLine = strLine.replace("#OutputFilePath#", outputFilePath)
    strLine = strLine.replace("#ColorFileName#", fileName1)
    strLine = strLine.replace("#GrayFileName#", min_image)
    
    fw.write(strLine+"\n")
fw.close()


#
# ----- Execute macro
#

command = FijiBin+' -macro '+FijiMacroDir+'registColor.ijm'
os.system(command)

