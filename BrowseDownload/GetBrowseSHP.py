import urllib2
import shutil
import os
from Tkinter import *
from tkFileDialog import askopenfilename
import arcpy
from arcpy import env


urlPrefix = "http://pw00busapp030.digitalglobe.com:6080/arcgis/rest/services/Browse/ImageServer/exts/DownloadService/DownloadTiffbyCatID?Catalog_Identifier=%27"
urlSuffix = "%27&f=tiff"

# get shp containing catIDs 
inputFeatureClass = arcpy.GetParameterAsText(0)

# get catID field
catIDField = arcpy.GetParameterAsText(1)

# Make the catID list
try:
    arcpy.AddMessage("Creating CatID List...")
    with arcpy.da.SearchCursor(inputFeatureClass, catIDField) as Scursor:
        catIdList = []
        for row in Scursor:
            catIdList.append(row[0])
except:
    arcpy.AddMessage("Failed to create CatID list.")
    arcpy.AddMessage(arcpy.GetMessages())
	
# get the directory as the target for browses
directory =  arcpy.GetParameterAsText(2)

# get browse imagery
arcpy.AddMessage("Fetching Browse Imagery...")
for catIdentifier in catIdList:
    browseFileName = directory + '/' + catIdentifier.strip('\n') + '.tif'
    url = urlPrefix + catIdentifier.strip('\n') + urlSuffix
    #print url
    try:
        request = urllib2.urlopen(url)
        #print request.info()['Content-Type']
        #Check the Content-Type to make sure we are getting a tiff back
        #When the image service can't find a catID, Content-Type is application/octet-stream
        if request.info()['Content-Type'] == 'image/tiff':   
            with open(browseFileName, 'wb') as fp:
                shutil.copyfileobj(request, fp)
        else:
            #print "CatID %s could not be found" % catIdentifier.strip('\n')
            arcpy.AddMessage("CatID %s could not be found" % catIdentifier.strip('\n'))

    except urllib2.HTTPError, e:
        #print "HTTP error: %d" % e.code
        arcpy.AddMessage("HTTP error: %d" % e.code)
		
    except urllib2.URLError, e:
        #print "Network error: %s" % e.reason.args[1]
        arcpy.AddMessage("Network error: %s" % e.reason.args[1])
else:
    print("no valid filename selected")