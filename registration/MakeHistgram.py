# -*- coding: utf-8 -*-
"""
Created on Sat Jul 23 22:21:47 2016

@author: nebula
"""
import os
# import Image, ImageDraw
from PIL import Image
# from PIL import ImageDraw
import matplotlib.pyplot as plt


def makeHist(inpath, outfile):
    img = Image.open(inpath)
    print(img.size)
    rawimage = img.getdata()

    hist = {'red': [], 'green': [], 'blue': [], 'sum': [], 'processed': []}
    for pix in rawimage:
        hist['red'].append(pix[0])
        hist['green'].append(pix[1])
        hist['blue'].append(pix[2])
        hist['sum'].append((pix[0] + pix[1] + pix[2]) / 3)

        processed_pix = (pix[2] * 2 - (pix[0] + pix[1])) * 2
        # if processed_pix < 0:
        #    processed_pix = 0
        hist['processed'].append(processed_pix)
    # hist = img.histogram()
    # print hist

    plt.hist(hist['red'], histtype='step', bins=128, alpha=0.5, color='red', range=(1, 255))
    plt.hist(hist['green'], histtype='step', bins=128, alpha=0.5, color='green', range=(1, 255))
    plt.hist(hist['blue'], histtype='step', bins=128, alpha=0.5, color='blue', range=(1, 255))
    plt.hist(hist['sum'], histtype='step', bins=128, alpha=0.5, color='gray', range=(1, 255))
    plt.savefig(outfile)
    plt.show()

    out_img = Image.new('L', img.size)
    out_img.putdata(hist['processed'])
    # out_img.save(outfile)

    # plt.hist(hist['processed'], histtype='step', bins=128, alpha=0.5, color='gray', range=(1,255))
    # plt.show()


if __name__ == '__main__':
    workdir = os.path.join('..', 'private', 'work3')
    outdir = os.path.join('..', 'private', 'processed')

    files = os.listdir(workdir)
    for filename in files:
        infile = os.path.join(workdir, filename)
        root, ext = os.path.splitext(filename)
        outfile = os.path.join(outdir, root + '.png')

        print(infile, outfile)
        makeHist(infile, outfile)

        # samplepath = os.path.join('..', 'private', 'work3', 'CD00002-IS-BR-21.tif')
        # makeHist(samplepath, 'result.png')
