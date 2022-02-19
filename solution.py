from os import listdir
from os.path import isfile, join
from urllib import request
from classes import Video, Cache, Requests, Endpoint, CacheLatency
from typing import List, Tuple, Dict

mypath = './input'
fileNames = [f for f in listdir(mypath) if isfile(join(mypath, f))]

videos: List[Video] = []



def resolveFile(file):
    [videoCount, endpointCount, requestCount, cacheCount, cacheSize] = map(int, file[0].split())
    endPointDone: bool = False
    videos: List[Video] = []
    caches: List[Cache] = []
    endPoints: List[Endpoint] = []
    cacheLatencies: List[CacheLatency] = []
    requests: List[Requests] = []
    
    for i in range(cacheCount):
        caches.append(Cache(i, cacheSize))
    
    pos = 1
    while pos < len(file):
        if pos == 1:
            videoSizes = map(int, file[pos].split())
            for i, size in enumerate(videoSizes):
                videos.append(Video(i, size))
            pos += 1
            continue
        elif endPointDone == False:
            while(len(endPoints) < endpointCount):
                [endPointLatency, endPointCacheCount] = map(int, file[pos].split())
                newEndpoint = Endpoint(len(endPoints), endPointLatency)
                pos += 1
                for i in range(endPointCacheCount):
                    [currentCacheId, cacheLatency] = map(int, file[pos].split())
                    currentCache = next(x for x in caches if x.Id == currentCacheId);
                    newEndpoint.Caches.append(currentCache)
                    cacheLatencies.append(CacheLatency(len(cacheLatencies), cacheLatency, currentCache, newEndpoint))
                    pos += 1
                    #print(pos)
                endPoints.append(newEndpoint)
            endPointDone == True
        for i in range(requestCount):
            [videoId, endPointId, videoRequests] = map(int, file[pos].split())
            selectedVideo = next(x for x in videos if x.Id == videoId)
            selectedEndpoint = next(x for x in endPoints if x.Id == endPointId)
            requests.append(Requests(videoRequests, selectedVideo, selectedEndpoint))
            pos += 1
            
        pos += 1
    
    requests.sort(key=lambda x: x.Count, reverse=True)
    
    return videos, caches, endPoints, cacheLatencies, requests
                

def filterPossibleCache(x):
    return x.canAdd          

    


for fileName in fileNames:
    with open('./input/'+fileName, "r") as f:
        file = f.read().split("\n")
        videos, caches, endPoints, cacheLatencies, requests = resolveFile(file)
        
        for currentRequest in requests:
            requestVideo: Video = currentRequest.Video
            requestEndpoint: Endpoint = currentRequest.Endpoint
            requestVideo: Video = currentRequest.Video
            requestEndpointCaches: List[Cache] = requestEndpoint.Caches
            
            possibleCaches = [x.Id for x in requestEndpointCaches if x.canAdd(requestVideo.Id)]
            possibleCacheLatencies = [x for x in cacheLatencies if x.Endpoint.Id == requestEndpoint.Id and x.Cache.Id in possibleCaches]
            
            if len(possibleCacheLatencies) > 0:
                selectedLatency = min(possibleCacheLatencies, key=lambda x: x.Latency)
                selectedLatency.Cache.addVideo(requestVideo)
                next(x for x in caches if x.Id == selectedLatency.Cache.Id).addVideo(requestVideo)
                next(x for x in requestEndpointCaches if x.Id == selectedLatency.Cache.Id).addVideo(requestVideo)
        
        
        usedCaches = [x for x in caches if len(x.Videos) > 0]
        usedCaches.sort(key=lambda x: x.Id)
        print(len(usedCaches))
        
        with open('./output/'+fileName.replace('in', 'out'), "w") as f:
            f.write(str(len(usedCaches))+'\n')
            for usedCache in usedCaches:
                f.write(str(usedCache.Id)+' '+ ' '.join([str(x.Id) for x in usedCache.Videos])+'\n')
            f.close()
            #f.write(str(len(allLikes))+ ' ' + ' '.join(allLikes))
            
