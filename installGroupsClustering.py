#!/ust/bin/python

#import libraries
import random
import math
import turtle
import _tkinter

#Number of clusters
numK = 8
iterations = 7

#euclidD: Calculate the euclidian distance between point1 and point2
def euclidD(point1,point2):
    sum = 0
    for index in range(len(point1)):
        diff = (point1[index]-point2[index]) ** 2
        sum = sum + diff

    euclidDistance = math.sqrt(sum)
    return euclidDistance
    
#readFile: Reads the file and returns datadict (hash table of lat and lon)
def readFile(filename):
    #Opens the file
    datafile = open(filename,"r")

    #Creates new data dictionary (hash table)
    datadict = {}
    key = 0

    #Loops through file and adds each line to datadic
    for line in datafile:
        items = line.split()
        key = key + 1
        lat = float(items[0])
        lon = float(items[1])
        datadict[key] = [lon,lat]
        

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
    #What it does
    for apass in range(repeats):
        print("****PASS",apass,"****")

        #Creates a list of clusters and fills it with k lists
        clusters= []
        for i in range(k):
            clusters.append([])

        #What it does
        for key in datadict:
            distances= []

            #What it does
            for clusterIndex in range(k):
                    #Calculates the distance between a point and the centroid
                    dist = euclidD(datadict[key],centroids[clusterIndex])
                    #Add distance to distances list
                    distances.append(dist)

            mindist = min(distances)
            index = distances.index(mindist)
            
            clusters[index].append(key)

        #What now?
        dimensions = len(datadict[1])
        for clusterIndex in range(k):
            sums = [0]*dimensions
            for akey in clusters[clusterIndex]:
                datapoints = datadict[akey]
                for ind in range(len(datapoints)):
                    sums[ind] = sums[ind] + datapoints[ind]
            for ind in range(len(sums)):
                clusterLen = len(clusters[clusterIndex])
                if clusterLen != 0:
                    sums[ind] = sums[ind]/clusterLen


            centroids[clusterIndex] = sums

##      for c in clusters:
##          print("CLUSTER")
##          for key in c:
##              print(datadict[key], end=" ")
##          print()
    return clusters

##visualize: Plots clusters on the map

#Outputs an image of the map of the united states
#Dots are placed on branch locations. Their color corrolates
#with the region/install grourp cluster.
def visualizeBranches(dataFile):
    #Calls functions to create lists and data dictionaries
    datadict = readFile(dataFile)

    branchCentroids = createCentroides(numK, datadict)
    
    clusters = createClusters(numK, branchCentroids, datadict, iterations)

    #Turtle objects
    branchT = turtle.Turtle()
    branchWin = turtle.Screen()
    branchWin.colormode(255)
    branchWin.bgpic("worldmap3x.gif")

    #Used to convert lat lon into width and height on the image
    wFactor = (branchWin.screensize()[0]/2)/180
    hFactor = (branchWin.screensize()[1]/2)/90

    #List of different colors for the clusters
    colorlist = [(165,0,38),(215,48,39),(244,109,67),
                 (253,174,97),(254,224,144),(224,243,248),
                 (171,217,233),(116,173,209),(69,117,180),
                 (49,54,149),(234,124,159),(255,0,0),
                 (0,255,0),(0,0,255),(255,255,0),
                 (0,255,255)]

    sortList = {}

    #What it do: Sorts stuff... but why?
    for clusterIndex in range(numK):
        sortList[len(clusters[clusterIndex])] = clusterIndex
    sortKeys = list(sortList.keys())
    sortKeys.sort()
    sortKeys.reverse()
    print(sortList)


    for sKey in sortKeys:
        clusterIndex = sortList[sKey]
        branchT.color(colorlist[clusterIndex])
        for aKey in clusters[clusterIndex]:
            lon = datadict[aKey][0]
            lat = datadict[aKey][1]
            branchT.goto(lon*wFactor,lat*hFactor)
            branchT.dot()
    branchWin.exitonclick()

#visualizeQuake("cluster.txt")

def main():
    filename = input('What is the name of the file that contains the lat lon data?(branches.csv)')
    visualizeBranches(filename)
    

    return

main()



