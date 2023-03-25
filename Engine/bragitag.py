import music_tag as music
import os
import re
import json


class bragitagEngine:
    
    def __init__(self):
        self.metadata = {}
        self.track = {}
        self.art = {}
        self.data = [self.track,self.art]
        
    def loadMetaData(self, filePath):
        meta = music.load_file(os.path.join(filePath))
        self.track[str(i)] = {"parentdir": os.path.relpath(os.path.join(filePath,os.pardir)),
                              "path": filePath,
                              "tracktitle": meta["tracktitle"].value,
                              "artist": meta["artist"].value,
                              "album": meta["album"].value,
                              "albumartist": meta["albumartist"].value,
                              "composer": meta["composer"].value,
                              "tracknumber": meta["tracknumber"].value,
                              "totaltracks": meta["totaltracks"].value,
                              "discnumber": meta["discnumber"].value,
                              "totaldiscs": meta["totaldiscs"].value,
                              "genre": meta["genre"].value,
                              "year": meta["genre"].value,
                              "isrc": meta["isrc"].value,
                              "comment": meta["comment"].value,
                              "compilation": meta["compilation"].value,
                              "#bitrate": meta["#bitrate"].value,
                              "#codec": meta["#codec"].value,
                              "#length": meta["#length"].value,
                              "#channels": meta["#channels"].value,
                              "#bitspersample": meta["#bitspersample"].value,
                              "#samplerate": meta["#samplerate"].value}
        
        self.metadata[str(i)] = meta
    
    def editFile(self,fileInfo):
        fileInfo = json.loads(fileInfo)
        meta = bragitagEngine.metadata
        for Id in fileInfo["ids"]:
            meta[Id]            

    
def main():
    tracks = bragitagEngine.loadFolder("C:/Users/19bst/Downloads/RADIOHEAD - KID A MNESIA (2021)  FLAC [PMEDIA] ⭐️")
    bragitagEngine.editFile(tracks)
    #print(tracks[0]["15"]["tracktitle"])
    #print(tracks)

if __name__ == "__main__":
    main()