from bragiengine.bragitag import BragitagEngine
import argparse
import sys


class BragiTagCLI():
    """Command Line Interface for running the BragiTag Engine
    Author: Ari Lacanienta
    Date: 03/25/2023"""

    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("-f",     metavar='f',  type=str, help="Path to the audio file")
        self.parser.add_argument("--tracktitle",   type=str, required=False, help="Alter Track Title")
        self.parser.add_argument("--artist",       type=str, required=False, help="Alter Artist")
        self.parser.add_argument("--album",        type=str, required=False, help="Alter Album")
        self.parser.add_argument("--albumartist",  type=str, required=False, help="Alter Album Artist")
        self.parser.add_argument("--artwork",      type=str, required=False, help="Alter Image")
        self.parser.add_argument("--composer",     type=str, required=False, help="Alter Composer")
        self.parser.add_argument("--tracknumber",  type=str, required=False, help="Alter Track Number")
        self.parser.add_argument("--totaltracks",  type=str, required=False, help="Alter Total Tracks")
        self.parser.add_argument("--discnumber",   type=str, required=False, help="Alter Disc Number")
        self.parser.add_argument("--totaldiscs",   type=str, required=False, help="Alter Total Discs")
        self.parser.add_argument("--genre",        type=str, required=False, help="Alter Genre")
        self.parser.add_argument("--year",         type=str, required=False, help="Alter Year")
        self.parser.add_argument("--isrc",         type=str, required=False, help="Alter isrc")
        self.parser.add_argument("--comment",      type=str, required=False, help="Alter Comment")
        self.parser.add_argument("--compilation",  type=str, required=False, help="Alter Compilation")

    def run(self):
        """Parses commands and edits music file metadata accordingly"""

        args = self.parser.parse_args()

        if len(sys.argv) > 3:

            tag_name = str()
            changes = dict()

            for i, argument in enumerate(sys.argv[3:]):
                if i % 2 == 0:
                    tag_name = argument[2:]
                else:
                    changes[tag_name] = argument

                

        engine = BragitagEngine(None)

        tracks = dict()
        engine.load_meta_data(args.f, tracks)

        print(engine.metadata[1])
        engine.edit_file_metadata({ "ids": [1], "changes": changes})

if __name__ == "__main__":
    exec = BragiTagCLI()
    exec.run()
