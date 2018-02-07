# ---------------------------------------------------------------------------
# dtm2raster.py
# Created on: 16 January 2009
# Keith Olsen
#  This program will read FUSION generated dtm surface files and convert
#    them into arcGIS rasters with projection info.
# ---------------------------------------------------------------------------

# Import system modules
import sys, string, os, arcpy

def main(rootDir, rasterName, projection):

    if projection == 'utm':
        cs = "PROJCS['NAD_1983_UTM_Zone_10N',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-123.0],PARAMETER['Scale_Factor',0.9996],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]"
    elif projection == 'stateplane':
        cs = "PROJCS['NAD_1983_2011_Oregon_Statewide_Lambert_Feet_Intl',GEOGCS['GCS_NAD_1983_2011',DATUM['D_NAD_1983_2011',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Lambert_Conformal_Conic'],PARAMETER['false_easting',1312335.958005249],PARAMETER['false_northing',0.0],PARAMETER['central_meridian',-120.5],PARAMETER['standard_parallel_1',43.0],PARAMETER['standard_parallel_2',45.5],PARAMETER['latitude_of_origin',41.75],UNIT['Foot',0.3048]]"
    else:
        cs = "error!!"

    arcpy.env.workspace = rootDir

    # Process DTM file to raster

    try:
        # Process: ASCII to Raster...
        if arcpy.Exists(rootDir + rasterName):
            arcpy.Delete_management(rootDir + rasterName)
            print "\n" + arcpy.GetMessages()

        print "ASCII2Raster " + rasterName
        arcpy.ASCIIToRaster_conversion(rootDir + rasterName + ".asc", rasterName, "FLOAT")
        print "\n" + arcpy.GetMessages()

        # Process: Define Projection...
        print "DefineProject " + rasterName
        arcpy.DefineProjection_management(rasterName, cs)
        print "\n" + arcpy.GetMessages()

    except:
        # Print error message if an error occurs
        print arcpy.GetMessages()

    os.system("del " + rootDir + rasterName + ".asc")

    print "\nascii2raster Done.\n\n"


if __name__ == '__main__':
        # Test for correct number of arguments
    if len(sys.argv) != 4:
        print "Usage: ascii2raster <rootDir w/trailing \\> <rasterName> <proj utm/stateplane>"
        sys.exit(1)

    try:
        main(sys.argv[1], sys.argv[2], sys.argv[3])

    except Exception, e:
        print "\n\n" + sys.argv[2] + ": " + e.args[0]

    except:
        print "unhandled Error!!"
