import music_tag as music
import os
import re
import json
import pathutils

class BragitagEngine:

    def __init__(self, config):
        self.metadata = {}
        self.track = {}
        self.art = {}
        self.data = [self.track, self.art]
        self.parse_config(config)

    def parse_config(self, config_file):
        """initialize variables from the config file"""
        with open(config_file, encoding="utf-8") as config:
            configuration = dict((key, value) for key, value in
                                 (setting.split(": ") for setting in config.read().split("\n")))

            self.root_dir = configuration["ROOT_DIR"]

            if not self.root_dir:
                self.root_dir = "/library"

    def load_dir_tree(self):
        return pathutils.get_child_dirs(self.root_dir)

    def loadMetaData(self, filePath):
        """Extracts relevant metadata from provided file and returns it in self.data
        Each track gets a unique ID.
        Also stores track file in self.metadata (indexed using the same ID)"""
        meta = music.load_file(os.path.join(filePath))

        art_key, art_data = self.parse_artwork(meta["artwork"].first)

        keys = self.track.keys()
        track_id = len(keys) + 1
        self.track[track_id] = {"parentdir": os.path.relpath(os.path.join(filePath, os.pardir)),
                                "path": os.path.basename(filePath).split('/')[-1],
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
        """gets album artwork data and returns md5 hash as a key. """
        if art:
            md5 = re.fullmatch(".*([a-z0-9]{32})", str(art)).group(1)
            art_data = {"type": art.mime,
                        "width": art.width,
                        "height": art.height,
                        "data": art.data,
                        }
        else:
            md5 = None
            art_data = None

        return md5, art_data

    def editFileJson(self, fileInfo):
        fileInfo = json.loads(fileInfo)
        for Id in fileInfo["ids"]:
            for key in fileInfo["changes"]:
                self.editFileTags(Id, key, fileInfo["changes"][key])
            self.metadata[Id].save()

    def editFileTags(self, Id, key, value):
        self.metadata[Id][key] = value

    def editFileName(self, Id, newName):
        ext = os.path.splitext(self.track[Id]["path"])
        os.rename(os.path.join(self.track[Id]["parentdir"], self.track[Id]["path"]), os.path.join(
            self.track[Id]["parentdir"], newName) + ext[1])
        self.track[Id]["path"] = newName+ext[1]
        
    def stringCustomize(self, Id, string):
        customStr = ""
        stringArr = string.split('%')
        for word in stringArr:
            if word in self.track[Id].keys():
                customStr += self.track[Id][word]
                
            #elif word[len(word) -1] == '/':
             #   customStr += "{:s}%".format(word[:len(word)-1])
                
            else:
                customStr += word
        return customStr


