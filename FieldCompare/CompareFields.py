'''****************************************************************
CompareFields.py
Author(s): Anders Olson
Usage: Run script using python IDE or similar
Description: 
        Script compares field names of two datasets and selects field
        names that are not a match/not found in both datasets.
        =^._.^=    
****************************************************************'''

import arcpy
import collections

##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##   
#================================#
# Configure logger 
#================================# 
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

def outputMessage(msg):
    print(msg)
    arcpy.AddMessage(msg)

def outputError(msg):
    print(msg)
    arcpy.AddError(msg)

##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##   
#================================#
# Define environment and messaging
#================================# 
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

# Set the overwriteOutput ON
arcpy.gp.overwriteOutput = True

# Set workspace to be in memory for faster run time
arcpy.env.workspace = "in_memory"

outputMessage("Workspace is: {}".format(arcpy.env.workspace))

##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##   
#================================#
# Define variables
#================================# 
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

#inData0 = r"U:\AOLSON\Working\temp\Water_Network.gdb\wMain"
#inData1 = r"U:\AOLSON\Working\temp\Water_Network.gdb\wNonPressurizedPipes"
inData0 = r"U:\AOLSON\Working\temp\Water_Network.gdb\wSystemValve"
inData1 = r"U:\AOLSON\Working\temp\Water_Network.gdb\wControlValves"

##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##   
#================================#
# Call Functions
#================================# 
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

# Populate a list of fields found in input dataset
fieldNames0 = [f.name for f in arcpy.ListFields(inData0)]
fieldNames1 = [f.name for f in arcpy.ListFields(inData1)] 

noMatchMains = [x for x in fieldNames0 if x not in fieldNames1]
noMatchPipes = [x for x in fieldNames1 if x not in fieldNames0]

outputMessage("Fields with no match in Dataset 1: {0}".format(noMatchMains))
outputMessage("Fields with no match in Dataset 2: {0}".format(noMatchPipes))

mainDomains = [f.domain for f in arcpy.ListFields(inData0) if f.domain != ""]
pipeDomains = [f.domain for f in arcpy.ListFields(inData1) if f.domain != ""]

#outputMessage("Domains for Mains: {0}".format(mainDomains))
#outputMessage("Domains for Pipes: {0}".format(pipeDomains))

noDomainMains = [x for x in mainDomains if x not in pipeDomains]
noDomainPipes = [x for x in pipeDomains if x not in mainDomains]

outputMessage("Domains with no match in Dataset 1: {0}".format(noDomainMains))
outputMessage("Domains with no match in Dataset 2: {0}".format(noDomainPipes))