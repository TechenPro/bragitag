from bragitag import BragitagEngine as be
import os

def main():

    engine = be(".config")
    root_folder = "C:/Users/19bst/Downloads/RADIOHEAD - KID A MNESIA (2021)  FLAC [PMEDIA] ⭐️"

    # editJson = '{"ids":[6,7,8],"changes":{"tracktitle":"HELLO WORLD", "comment":"THIS IS A COMMENT"}}'
    for filename in os.listdir(root_folder):
        engine.loadMetaData(os.path.join(root_folder, filename))
    # #engine.editFileJson(editJson)
    # engine.editFileName(4,"4 3")
    # engine.editFileTags(4, "album", "New Artist")
    string = "%album% - %tracktitle% - /%hello"
    str1 = engine.stringCustomize(3,string)
    print(str1)
if __name__ == "__main__":
    main()

