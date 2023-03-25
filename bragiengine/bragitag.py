import music_tag as music
import os
import re
import bragiengine.pathutils as pathutils



class BragitagEngine:
    """BragitagEngine
    Description: Class for modifying audio file metadata and interfacing with the webapp
    Authors: Ari Lacanienta, Benjamin Stone, Turin Briggs
    Date: 03/25/2023"""

    def __init__(self, config):
        """initialize and configure engine"""
        self.metadata = {}
        self.artworks = {}
        if not config:
            self.root_dir = "/library"
        else:
            self.parse_config(config)

    def parse_config(self, config_file):
        """initialize variables from the config file"""
        with open(config_file, encoding="utf-8") as config:
            configuration = dict((key, value) for key, value in
                                 (setting.split(": ") for setting in config.read().split("\n")))

            self.root_dir = configuration["ROOT_DIR"]

            if not self.root_dir:
                self.root_dir = "/library"

    def get_dir_tree(self):
        """get all subdirectories of root"""
        return pathutils.get_child_dirs(self.root_dir)

    def change_active_dir(self, dir_path):
        """switches to new active directory, making contained music metadata files available for editing"""
        tracks = dict()
        if not os.path.isdir(dir_path):
            return
        self.metadata.clear()
        self.artworks.clear()
        for path in pathutils.get_child_audio_files(self.root_dir):
            self.load_meta_data(path, tracks)
        return tracks

    def load_meta_data(self, filepath, tracks):
        """Extracts relevant metadata from provided file and provides it to tracks and self.artworks.
        Each track gets a unique ID.
        Also stores track file in self.metadata (indexed using the same ID)"""
        meta = music.load_file(filepath)

        art_key, art_data = self.parse_artwork(meta["artwork"].first)

        keys = tracks.keys()
        track_id = len(keys) + 1
        tracks[track_id] = {"parentdir": os.path.abspath(os.path.join(filepath, os.pardir)),
                            "path": os.path.basename(filepath).split('/')[-1],
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
                            "year": meta["year"].value,
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
            self.artworks[art_key] = art_data
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

    def edit_file_metadata(self, file_info):
        """identically modifies the metadata of all tracks
        where fileInfo is a dict containing an array of ids to change
        and a dict of metadata fields to change, and their new value
        """
        for track_id in file_info["ids"]:
            for field in file_info["changes"]:
                self.metadata[track_id][field] = file_info["changes"][field]
            self.metadata[track_id].save()

        

    def edit_filename(self, track_id, new_name):
        """changes a track's filename"""
        ext = os.path.splitext(self.metadata[track_id].filename)
        parent_path = os.path.abspath(os.path.join(self.metadata[track_id].filename, os.pardir))
        os.rename(self.metadata[track_id].filename, os.path.join(parent_path, new_name) + ext[1])
        self.metadata[track_id] = music.load_file(os.path.join(parent_path, new_name) + ext[1])


    def resolve_metadata_macros(self, track_id, string):
        """if `string` contains metadata fields surrounded by '%', replace it with the provided track's metadata values
        EX: `The artist is: %artist%` -> `The artists is: The Beatles"""
        resolved_str = ""
        string_arr = string.split('%')
        for word in string_arr:
            if word in self.metadata[track_id]._TAG_MAP.keys():
                resolved_str += str(self.metadata[track_id][word])
            
            elif word == "":
                continue

             #escape char   
            elif word[-1] == '\\':
                resolved_str += "{:s}%".format(word[:len(word)-1])
                
            else:
                resolved_str += word

        return resolved_str
