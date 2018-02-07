# ---------------------------------------------------------------------------
# create_index3.py
# Created on: 1 Feb 2018
# Description:
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy
from arcpy.sa import *

def main():
    # Check out the ArcGIS Spatial Analyst extension license
    arcpy.CheckOutExtension("Spatial")
    tempDir = "C:\\temp\\HJA_lidar\\hja2016_cover\\"
    outGdb = "T:\\groups\\HJA_Lidar\\OLC_McKenzie_River_2016\\Cover_rasters_2016_be08.gdb"
    cellSize = "5"

    outRaster = Raster(outGdb + "\\cov16_5all_1")
    for htBreak in range(2,65):
        print "running height break " + str(htBreak)
        outRaster = outRaster + (htBreak * Raster(tempDir + "cov16_5all_" + str(htBreak)))

    outRaster.save(outGdb + "\\hja2016_be08_index3")

    print "\nIndex3 Done.\n\n"

if __name__ == '__main__':
    main()
