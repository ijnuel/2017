from tkinter import S
from typing import List, Tuple, Dict

class Video:
    def __init__(self, Id: int, Size: int):
        self.Id = Id
        self.Size = Size
        
class Cache:
    def __init__(self, Id: int, SizeAvailable: int):
        self.Id = Id
        self.SizeAvailable = SizeAvailable
        self.Videos : List[Video] = []
    
    def addVideo(self, video: Video):
        if video in self.Videos:
            return
        self.Videos.append(video)
        self.SizeAvailable = self.SizeAvailable - video.Size
    
    def canAdd(self, videoSize: int):
        return videoSize <= self.SizeAvailable

class Endpoint:
    def __init__(self, Id: int, CloudLatency: int):
        self.Id = Id
        self.CloudLatency = CloudLatency
        self.Caches : List[Cache] = []
            
class Requests:
    def __init__(self, Count: int, Video: Video, Endpoint: Endpoint):
        self.Count = Count
        self.Video = Video
        self.Endpoint = Endpoint

class CacheLatency:
    def __init__(self, Id: int, Latency: int, Cache: Cache, Endpoint: Endpoint):
        self.Id = Id
        self.Latency = Latency
        self.Cache = Cache
        self.Endpoint = Endpoint