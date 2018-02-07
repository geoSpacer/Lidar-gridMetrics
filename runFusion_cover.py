# ---------------------------------------------------------------------------
# dtm2raster.py
# Created on: 16 January 2009 - modified 30 January 2018
# Keith Olsen
#  This program will read FUSION generated dtm surface files and convert
#    them into arcGIS rasters with projection info.
# ---------------------------------------------------------------------------

# Import system modules
import sys, string, os, subprocess
import ascii2raster

def main():
    lidarRoot = "C:\\temp\\HJA_lidar\\"
    lidarListFile = "T:\\groups\\HJA_Lidar\\OLC_McKenzie_River_2016\\las_pointFile_list_utm.txt"
    projection = 'utm'

    for cellSize in [5]:
        for heightBreak in range(54,56):
            runName = "cov16_" + str(cellSize) + "all_" + str(heightBreak)
            print "Running Fusion Cover for " + runName + " with heightbreak " + str(heightBreak) + " and cellsize " + str(cellSize)

            subprocess.call("C:\\fusion\\cover /all " + lidarRoot + "hja2008_be_utm.dtm " + lidarRoot + "hja2016_cover\\" +
                      runName + ".dtm " + str(heightBreak) + " " + str(cellSize) + " m m 1 10 2 2 " + lidarListFile, shell=True)

            subprocess.call("C:\\fusion\\dtm2ascii /raster " + lidarRoot + "hja2016_cover\\" + runName + ".dtm", shell=True)

            # read ascii raster into ESRI file system raster and project
            ascii2raster.main(lidarRoot + "hja2016_cover\\", runName, projection)

    print "runFusion_cover Done."

if __name__ == '__main__':
    main()
