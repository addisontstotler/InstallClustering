#!/ust/bin/python

#import libraries
import random
import math
import turtle
import _tkinter

#Number of clusters
numK = 8
iterations = 20

#euclidD: Calculate the euclidian distance between point1 and point2
def euclidD(point1,point2):
    sum = 0
    for index in range(len(point1)-1):
        diff = (point1[index]-point2[index]) ** 2
        sum = sum + diff

    euclidDistance = math.sqrt(sum)
    return euclidDistance
    
#readFile: Reads the file and returns datadict (hash table of lat, lon, and branchName)
    #Lat and Lon are used for clustering and branchName is only used for the output file.
def readFile(filename):
    #Opens the file
    datafile = open(filename,"r")
    #Creates new data dictionary (hash table)
    datadict = {}
    key = 0

    #Loops through file and adds each line to datadic
    for line in datafile:
        line.replace("\n",'')
        items = line.split(',')
        key = key + 1
        lat = float(items[0])
        lon = float(items[1])
        branchName = items[2]
        datadict[key] = [lon,lat,branchName]

    datafile.close()

    return datadict

#createCentroids: Creats k number of centroids with data from datadict(lat lon)
def createCentroides(k, datadict):
    #Creates centroid lists and count  
    centroids=[]
    centroidCount = 0
    centroidKeys = []

    #Makes k randomly placed centroids
    while centroidCount < k:
        rkey = random.randint(1,len(datadict))
        if rkey not in centroidKeys:
            #Makes a centroid with data from the datadict(lat lon)
            centroids.append(datadict[rkey])
            #Adds to the keys list (so we don't reuse that key)
            centroidKeys.append(rkey)
            centroidCount = centroidCount + 1
    return centroids

#createClusters:
def createClusters(k, centroids, datadict, repeats):
    for apass in range(repeats):
        print("****PASS",apass,"****")

        #Creates a list of clusters and fills it with k lists
        clusters= []
        for i in range(k):
            clusters.append([])

        for key in datadict:
            #Creates a temporary list of distances
            distances= []

            #Fills the list with distances
            for clusterIndex in range(k):
                    #Calculates the distance between a point and the centroid
                    dist = euclidD(datadict[key],centroids[clusterIndex])
                    #Add distance to distances list
                    distances.append(dist)

            #Finds the smallest distance between branches and adds it to the cluster.
            mindist = min(distances)
            index = distances.index(mindist)
            clusters[index].append(key)

        #What now?
        dimensions = len(datadict[1])-1
        for clusterIndex in range(k):
            sums = [0]*dimensions
            for akey in clusters[clusterIndex]:
                datapoints = datadict[akey]
                for ind in range(len(datapoints)-1):
                    sums[ind] = sums[ind] + datapoints[ind]
            for ind in range(len(sums)):
                clusterLen = len(clusters[clusterIndex])
                if clusterLen != 0:
                    sums[ind] = sums[ind]/clusterLen


            centroids[clusterIndex] = sums

#Test output
#-------------------------------------------
#      for c in clusters:
#          print("CLUSTER")
#          for key in c:
#              print(datadict[key], end=" ")
#          print()
#-------------------------------------------
    return clusters


#clusterBranches: Lists the clusters of branches

def clusterBranches(dataFile):
    #Calls functions to create lists and data dictionaries
    datadict = readFile(dataFile)

    branchCentroids = createCentroides(numK, datadict)
    
    clusters = createClusters(numK, branchCentroids, datadict, iterations)

    sortList = {}

    #What it do: Sorts stuff... but why?
    #numK is the number of clusters
    for clusterIndex in range(numK):
        sortList[len(clusters[clusterIndex])] = clusterIndex
        
    sortKeys = list(sortList.keys())
    sortKeys.sort()
    sortKeys.reverse()
    print(sortList)


    #Outputs the results of the clustering
    for sKey in sortKeys:
        clusterIndex = sortList[sKey]
        for aKey in clusters[clusterIndex]:
            lon = datadict[aKey][0]
            lat = datadict[aKey][1]
            print(datadict[aKey][2].replace('\n',''))
        print()

    return

def main():
    #Filename of a csv formated as: "lat,lon,branchName"
    latLonFileName = input('What is the name of the file that contains the lat lon data?(zipcodes_locations.csv)')
    clusterBranches(latLonFileName)
    
    
    return

main()



