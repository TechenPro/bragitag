import music_tag as music
import os
import re
import json

class bragitagEngine:
    metadata = {}
    def loadFolder(folder):
        track = {}
        art = {}
        tracks = [track,art]
        
        
        for i,filePath in enumerate(os.listdir(folder),start = 1):
            ext = re.fullmatch(".+\.(aac|aiff|dsf|flac|m4a|mp3|ogg|opus|wav|wv)", filePath.lower())
            if os.path.isdir(filePath):
                bragitagEngine.loadFolder(os.path.join(folder,filePath))
            elif ext:
                meta = music.load_file(os.path.join(folder,filePath))
                track[str(i)] = {"tracktitle": meta["tracktitle"].value,
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
                
                bragitagEngine.metadata[str(i)] = meta
            
        return json.dumps(tracks)

    
    
    def editFile(fileInfo):
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