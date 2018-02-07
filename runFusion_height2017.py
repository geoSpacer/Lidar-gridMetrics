# ---------------------------------------------------------------------------
# runFusion_height2017.py
# Created on: 28 December 2009 (13 March 2012 - updated for arcGIS 10)
# Updated on: 5 February 2018
# For use with Python 2.7
# Keith Olsen
#  This program will start FUSION gridmetrics at a specified cell size and
#    process the results into a merged raster surface for the HJA research forest
# ---------------------------------------------------------------------------

# Import system modules
import sys, string, os, subprocess
import ascii2raster
import clip_raster
import importTif

def main():
    projection = 'utm'
    lidarDataset = 'hja2016'
#    deliveryArea = 'HJA2008_Olsen_Metrics'
    deliveryArea = 'OLC_McKenzie_River_2016'
    cellSize = 5
    heightbreak = 1
    runIndex = ["max", "mn", "p95", "cv"]
#    runIndex = ["pfr", "par", "tfr", "tar", "crr"]
    osGeoRoot = "C:\\OSGeo4W\\"
    lidarRoot = "C:\\temp\\HJA_lidar\\"
    beDTMfile = "hja2008_be_utm.dtm"
#    beDTMfile = lidarDataset + "_be_utm.dtm"
    tileNameFile = "T:\\Groups\\HJA_LIDAR\\" + deliveryArea + "\\las_pointFile_list_utm.txt"
    lidarReturns = "f"
    csvReturns = "_first_"
#    csvReturns = "_all_"
    outputGdb = "T:\\Groups\\HJA_LIDAR\\" + deliveryArea + "\\gridMetrics_" + lidarDataset + ".gdb"
    outputPrefix = lidarDataset + "_" + str(cellSize) + lidarReturns + "_hb" + str(heightbreak) + "_"

    # minimum height for points set to 2 meters

    if lidarDataset == 'hja2014':
        # HJA Raster Extents - snap (2014)
        llx_base = 557417.5
        lly_base = 4893937.5
        llx_max = 571997.5
        lly_max = 4903762.5
    elif lidarDataset == 'hja2008' or lidarDataset == 'hja2016':
        # HJA Raster Extents - snap (2008)
        llx_base = 557732.5
        lly_base = 4894117.5
        llx_max = 571852.5
        lly_max = 4903562.5
    else:
        llx_base = 0.0
        lly_base = 0.0
        llx_max = 0.0
        lly_max = 0.0

    # Blue River Raster Extents - snap
    ##llx_base = 553210
    ##lly_base = 4894790
    ##llx_max = 569380
    ##lly_max = 4909850

    windowSize = 800

    if projection == 'stateplane':
        cellSize /= 0.3048
        heightbreak /= 0.3048
        windowSize /= 0.3048
        beDTMfile = lidarDataset + "_be_lam.dtm"
        tileNameFile = "T:\\Groups\\HJA_LIDAR\\" + deliveryArea + "\\las_pointFile_list.txt"

        # HJA Raster Extents (Oregon Lambert)
        llx_base = 846187.5
        lly_base = 896773.5
        llx_max = 893098.5
        lly_max = 927583.5


    llx_base = llx_base - (cellSize / 2.0)
    lly_base = lly_base - (cellSize / 2.0)
    llx_current = llx_base
    lly_current = lly_base

    if not os.path.exists(lidarRoot + "height_rasters" + str(int(cellSize))):
        os.mkdir(lidarRoot + "height_rasters" + str(int(cellSize)))

    rasterRoot = lidarRoot + "height_rasters" + str(int(cellSize)) + "\\"

    tileNum = 1
    while (lly_current + cellSize) < lly_max:
        while (llx_current + cellSize) < llx_max:
            runName = "ht" + str(int(cellSize)) + lidarReturns + str(tileNum)
            print "Running Fusion Gridmetrics (elevation) for " + runName + " with cellsize " + str(cellSize)

            if csvReturns == "_first_":
                subprocess.call("C:\\fusion\\gridmetrics /first /minht:" + str(heightbreak) + " /gridxy:" + str(llx_current) + "," + str(lly_current) + "," + str(llx_current + windowSize) + "," +
                      str(lly_current + windowSize) + " " + lidarRoot + beDTMfile + " " + str(heightbreak) + " " + str(cellSize) + " " + lidarRoot +
                      runName + " " + tileNameFile, shell=True)
            else:
                subprocess.call("C:\\fusion\\gridmetrics /gridxy:" + str(llx_current) + "," + str(lly_current) + "," + str(llx_current + windowSize) + "," +
                      str(lly_current + windowSize) + " " + lidarRoot + beDTMfile + " " + str(heightbreak) + " " + str(cellSize) + " " + lidarRoot +
                      runName + " " + tileNameFile, shell=True)

            if os.path.isfile(lidarRoot + runName + csvReturns + "returns_elevation_stats.csv"):
                for colName in runIndex:
                    if colName == "max":
                        colNum = 7
                    elif colName == "mn":
                        colNum = 8
                    elif colName == "std":
                        colNum = 10
                    elif colName == "cv":
                        colNum = 12
                    elif colName == "p25":
                        colNum = 28
                    elif colName == "p50":
                        colNum = 31
                    elif colName == "p75":
                        colNum = 34
                    elif colName == "p80":
                        colNum = 35
                    elif colName == "p90":
                        colNum = 36
                    elif colName == "p95":
                        colNum = 37
                    elif colName == "pfr":
                        colNum = 49
                    elif colName == "par":
                        colNum = 50
                    elif colName == "tfr":
                        colNum = 64
                    elif colName == "tar":
                        colNum = 65
                    elif colName == "crr":
                        colNum = 68
                    else:
                        colNum = 0
                        sys.exit(1)

                    subprocess.call("C:\\fusion\\csv2grid " + lidarRoot + runName + csvReturns + "returns_elevation_stats.csv " + str(colNum) +
                               " " + rasterRoot + runName + "_" + colName + ".asc", shell=True)

                    ascii2raster.main(rasterRoot, runName + "_" + colName, projection)

                    boundStr = str(llx_current + (0.5 * cellSize)) + " " + str(lly_current + (0.5 * cellSize)) + " "
                    boundStr += str(llx_current + windowSize - (0.5 * cellSize)) + " " + str(lly_current + windowSize - (0.5 * cellSize))

                    clip_raster.main(rasterRoot, runName + "_" + colName, boundStr)

                subprocess.call("del " + lidarRoot + runName + csvReturns + "returns_elevation_stats*.*", shell=True)
                subprocess.call("del " + lidarRoot + runName + csvReturns + "returns_intensity_stats*.*", shell=True)

            llx_current += windowSize - cellSize
            tileNum += 1

        llx_current = llx_base
        lly_current += windowSize - cellSize

    for varName in runIndex:
        # List all rasters that are part of 'varName' and write them to a text file.
        # the /b switch gets rid of extraneous info from 'dir' and the /s switch
        # looks at subdirectories. There are no subdirectories, but it appends the file path
        subprocess.call("dir " + rasterRoot + "*_" + varName + "c /b /s > " + rasterRoot + "mergeList.txt", shell=True)

        callReturn = subprocess.call(osGeoRoot + "OSGeo4W " + osGeoRoot + "bin\\python.exe " + osGeoRoot + "bin\\gdal_merge.py" + " -init -9999 -o " +
            lidarRoot + "ht" + str(int(cellSize)) + lidarReturns + "_" + varName + ".tif --optfile " + rasterRoot + "mergeList.txt", shell=True)

        if callReturn == 0:
            importTif.main(lidarRoot, "ht" + str(int(cellSize)) + lidarReturns + "_" + varName, outputGdb, outputPrefix)

    print "runFusion_height Done."

if __name__ == '__main__':
    main()
