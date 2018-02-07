# ---------------------------------------------------------------------------
# clip_raster.py
# Created on: 24 December 2009
# Keith Olsen
#  This program will read arc GRID rasters and clip the buffer area in pre-
#   paration for merging into single surface
# ---------------------------------------------------------------------------

# Import system modules
import sys, string, os, arcpy

def main(rootDir, rasterName, clipBounds):
    arcpy.env.workspace = rootDir
    arcpy.pyramid = "NONE"

    try:
        # delete raster if it already exists
        if arcpy.Exists(rootDir + rasterName + "c"):
            arcpy.Delete_management(rootDir + rasterName + "c")
            print "\n" + arcpy.GetMessages()

        # clip raster to remove buffer area necessary for correct FUSION analysis
        print "Clip Raster: " + rasterName + " with bounds " + clipBounds
        arcpy.Clip_management(rasterName, clipBounds, rasterName + "c")
        print "\n" + arcpy.GetMessages()

        # Delete unclipped raster
        if arcpy.Exists(rasterName):
            arcpy.Delete_management(rasterName)
            print "\n" + arcpy.GetMessages()


    except:
        # Print error message if an error occurs
        print arcpy.GetMessages()

    print "\nclip_raster Done.\n\n"

if __name__ == '__main__':
        # Test for correct number of arguments
    if len(sys.argv) != 4:
        print "Usage: clip_raster <rootDir w/trailing \\> <rasterName> <xmin ymin xmax ymax>"
        sys.exit(1)

    try:
        main(sys.argv[1], sys.argv[2], sys.argv[3])

    except Exception, e:
        print "\n\n" + sys.argv[2] + ": " + e.args[0]

    except:
        print "unhandled Error!!"
