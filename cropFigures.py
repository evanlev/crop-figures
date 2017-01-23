#!/anaconda/bin/python
import numpy as np
import argparse
import matplotlib.image as mplimg
import os
import sys
import imp
egl = imp.load_source('eglUtils', '/Users/evanlevine/bin/egl_scripts/eglUtils.py');
        
# --- Settings --------
imageExtensions = {'.png', '.jpg', '.JPG', '.jpeg', '.bmp', '.tif', '.tiff'}
border = 2
# --------------------

def usage(argv0):
    print("%s" % argv0)
    print("-a,--all\tcrop all images in this directory")
    print("--border=NUM\tadd a border with this size")
    print("<image file>: crop this image file")
    exit()

# imgPath = /path/to/image.png
def cropAndSave(imgPath, border = 0):
    # Read image
    im = mplimg.imread(imgPath);

    # Crop image
    im_cropped = cropImage2(im, border)

    # Save output
    fileparts = os.path.splitext(imgPath);
    imgPathRect = fileparts[0] + "_cropped" + fileparts[1]
    print("Saving output to %s..." % imgPathRect)
    mplimg.imsave(imgPathRect,im_cropped)

def getWhiteBounds(im):
    N = im.shape[0]
    M = im.shape[1]
    C = im.shape[2]
    white = np.ones(C).flatten(1)

    xmax = N-1
    xmin = 0
    ymax = M-1
    ymin = 0
    # xmin
    allWhite = True
    while allWhite and xmin < N-1:
        # Loop over columns
	for y in range(M):
            # If this pixel is not white
            if (im[xmin,y,:].flatten(1) != white).any():
                allWhite = False
                break
	xmin = xmin + 1

    # ymin
    allWhite = True
    while allWhite and ymin < M-1:
        # Loop over columns
	for x in range(N):
            # If this pixel is not white
            if (im[x,ymin,:].flatten(1) != white).any():
                allWhite = False
                break
	ymin = ymin + 1

    # ymax
    allWhite = True
    while allWhite and ymax >= 0:
        # Loop over columns
	for x in range(N):
            # If this pixel is not white
            if (im[x,ymax,:].flatten(1) != white).any():
                allWhite = False
                break
	ymax = ymax - 1

    # xmax
    allWhite = True
    while allWhite and xmax >= 0:
        # Loop over columns
	for y in range(M):
            # If this pixel is not white
            if (im[xmax,y,:].flatten(1) != white).any():
                allWhite = False
                break
	xmax = xmax - 1

    return xmin, xmax, ymin, ymax



# INPUTS: 
#   im  = N x M x C 3D numpy array with C color channels
# OUTPUTS:
#   imc = n x m x C array, with outer white region cropped
def cropImage2(im, border = 0):
    assert( im.ndim == 3 )
    N = im.shape[0]
    M = im.shape[1]
    C = im.shape[2]

    # Get bounds of this figure
    xmin,xmax,ymin,ymax = getWhiteBounds(im)

    print("Cropping to %d:%d, %d:%d (%f x size), border: %d" % (xmin,xmax,ymin,ymax,float(xmax-xmin)*float(ymax-ymin)/float(M*N), border))
    n = xmax - xmin + 1
    m = ymax - ymin + 1
    imPad = np.ones((2*border + n, 2*border + m, C))
    imPad[border:border+n-1,border:border+m-1,:] = im[xmin:xmax,ymin:ymax,:]
    return imPad

# Read input files
if len(sys.argv) == 1:
    usage(sys.argv[0])
else:
    # Parse arguments
    parser=argparse.ArgumentParser(
                description='''My Description. And what a lovely description it is. ''',
                    epilog="""All's well that ends well.""")
    parser.add_argument('--border', type=int, default=0, help='add a border of white pixels')
    #parser.add_argument('-a', type=bool, default=False, help='crop all files')
    parser.add_argument('-a', dest='a', action='store_true')
    parser.add_argument('-i', type=str, default='', help='image file to crop')
    #parser.add_argument('bar', nargs='*', default=[1, 2, 3], help='BAR!')
    args=parser.parse_args()

    if False:
        allFiles = False
        imgFile = ''
        border = 0
        for arg in sys.argv[1:]:
            if arg == '-a' or arg == '-all':
                allFiles = True
            elif len(arg) > len('--border=') and arg[0:len('--border=')] == '--border=':
                border = int(arg[len('--border='):])
            else:
                imgFile = arg

        if imgFile != '' and allFiles:
            usage(sys.argv[0])

    if args.i != '' and args.a:
        usage(sys.argv[0])

    # Crop images
    if args.a:
        files = [f for f in os.listdir('.') if os.path.isfile(f) and len(f) > 4 and f[-4:] in imageExtensions]
        for f in files:
            cropAndSave(f, args.border)
    else:
        if len(args.i) > 4 and args.i[-4:] in imageExtensions:
            cropAndSave(args.i, args.border);
        else:
            print("Image with unrecognized extension: %s" % args.i)


