from bragitag import BragitagEngine
import os

engine = BragitagEngine("bragiengine/.config")

filename = '01. Everything In Its Right Place.flac'
nopicture = 'Hymns_004_TruthEternal_eng.mp3'

editJson = '{"ids":[6,7,8],"changes":{"tracktitle":"HELLO WORLD", "comment":"THIS IS A COMMENT",}}'
for filename in os.listdir(engine.root_dir):
    engine.loadMetaData(os.path.join(engine.root_dir, filename))
# engine.editFile(editJson)
# with open("image.txt", "w") as artwork:
#     artwork.write(str(engine.metadata[6]["artwork"].first.data))


#print(engine.data)


# BragitagEngine.editFile(tracks)

#print(tracks[0]["15"]["tracktitle"])
# print(tracks)

