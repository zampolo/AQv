#import dicom
import pydicom as dicom
import os
import numpy
from matplotlib import pyplot, cm
PathDicom = "./MyHead/"
lstFilesDCM = []  # create an empty list
for dirName, subdirList, fileList in os.walk(PathDicom):
    for filename in fileList:
        if ".dcm" in filename.lower():  # check whether the file's DICOM
            lstFilesDCM.append(os.path.join(dirName,filename))
# Get ref file
RefDs = dicom.read_file(lstFilesDCM[0])

# Load dimensions based on the number of rows, columns, and slices (along the Z axis)
ConstPixelDims = (int(RefDs.Rows), int(RefDs.Columns), len(lstFilesDCM))

# Load spacing values (in mm)
ConstPixelSpacing = (float(RefDs.PixelSpacing[0]), float(RefDs.PixelSpacing[1]), float(RefDs.SliceThickness))
x = numpy.arange(0.0, (ConstPixelDims[0]+1)*ConstPixelSpacing[0], ConstPixelSpacing[0])
y = numpy.arange(0.0, (ConstPixelDims[1]+1)*ConstPixelSpacing[1], ConstPixelSpacing[1])
z = numpy.arange(0.0, (ConstPixelDims[2]+1)*ConstPixelSpacing[2], ConstPixelSpacing[2])
# The array is sized based on 'ConstPixelDims'
ArrayDicom = numpy.zeros(ConstPixelDims, dtype=RefDs.pixel_array.dtype)

# loop through all the DICOM files
for filenameDCM in lstFilesDCM:
    # read the file
    ds = dicom.read_file(filenameDCM)
    # store the raw image data
    ArrayDicom[:, :, lstFilesDCM.index(filenameDCM)] = ds.pixel_array
pyplot.figure(dpi=300)
pyplot.axes().set_aspect('equal', 'datalim')
pyplot.set_cmap(pyplot.gray())
pyplot.pcolormesh(x, y, numpy.flipud(ArrayDicom[:, :, 80])) # Note that just the slice 80 is shown here !!!! To verify this point, just change the variable sliceNumber below to 80

# Retrieving some information and Testing what happens when we try to show just one slice
sliceNumber = 3 # any integer between 0 and len(lstFilesDCM)
imageSlice = dicom.read_file( lstFilesDCM[ sliceNumber ] )
print('======================')
print('Number of bits per pixel: ')
print('Method 1: ', imageSlice.pixel_array.dtype )
print('Method 2: ', imageSlice.BitsAllocated)
print('Thus, 16 bits/pixel' )
print('======================')
print('Testing what happens when we try to show just one slice (file) dcm')
pyplot.figure()
pyplot.imshow( imageSlice.pixel_array, cmap = 'bone')
print('Image is displayed correctly !!!')
print('======================')

pyplot.show()
