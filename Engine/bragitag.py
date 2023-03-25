import music_tag as music
import os
import re
import json


class BragitagEngine:
    
    def __init__(self, config):
        self.metadata = {}
        self.track = {}
        self.art = {}
        self.data = [self.track, self.art]
        self.root_dir = ''
        self.parse_config(config)
    
    def parse_config(self, config_file):

        with open(config_file, encoding="utf-8") as config:
            configuration = dict((key, value) for key, value in 
                (setting.split(": ") for setting in config.read().split("\n")))
            
            self.root_dir = configuration["ROOT_DIR"]

            if not self.root_dir:
                self.root_dir = "/Library"
        
    def loadMetaData(self, filePath):
        meta = music.load_file(os.path.join(filePath))

        art_key, art_data = self.parse_artwork(meta["artwork"].first)

        keys = self.track.keys()
        track_id = len(keys) +1
        self.track[track_id] = {"parentdir": os.path.relpath(os.path.join(filePath,os.pardir)),
                                "path": filePath,
                                "tracktitle": meta["tracktitle"].value,
                                "artist": meta["artist"].value,
                                "album": meta["album"].value,
                                "albumartist": meta["albumartist"].value,
                                "artwork": art_key,
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
        if art_data:
            self.art[art_key] = art_data
        
        self.metadata[track_id] = meta
    
    def parse_artwork(self, art):
        if art:
            md5 = re.fullmatch(".*([a-z0-9]{32})", str(art)).group(1)
            art_data = {"type": art.mime,
                        "width": art.width,
                        "height": art.height,
                        "data": art.data,
                        }
        else :
            md5 = None
            art_data = None

        return (md5, art_data)

    def editFileJson(self,fileInfo):
        fileInfo = json.loads(fileInfo)
        for Id in fileInfo["ids"]:
            for key in fileInfo["changes"]:
                self.editFileTags(Id,key,fileInfo["changes"][key])

    def editFileTags(self,Id,key,value):
        self.metadata[Id][key] = value
        for meta in self.metadata.values():
            meta.save()
            
    def editFileName(self,Id,newName):
        os.rename(self.track[Id]["path"],newName)



def main():

    engine = BragitagEngine(".config")
    root_folder = "C:/Users/19bst/Downloads/RADIOHEAD - KID A MNESIA (2021)  FLAC [PMEDIA] ⭐️"

    editJson = '{"ids":[6,7,8],"changes":{"tracktitle":"HELLO WORLD", "comment":"THIS IS A COMMENT"}}'
    for filename in os.listdir(root_folder):
        engine.loadMetaData(os.path.join(root_folder, filename))
    engine.editFileJson(editJson)
    print(engine.metadata[6]["comment"])
    engine.editFileName(4,"HELLO!.flac")

if __name__ == "__main__":
    main()



        