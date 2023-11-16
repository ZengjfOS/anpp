import os
import sys
import shutil
import json

from anpp.CmdWindow import CmdWindow

def acmdsets():
    exePath = os.path.abspath(__file__)
    folder = os.path.dirname(exePath)
    currentFolder = os.getcwd()
    templateFolder = os.path.join(folder, 'template')

    if not os.path.exists(os.path.expanduser('~') + "/.anpp"):
        os.mkdir(os.path.expanduser('~') + "/.anpp")
        shutil.copyfile(templateFolder + "/acmdsets/ACmdSets.json", os.path.expanduser('~') + "/.anpp/ACmdSets.json")

    if len(sys.argv) == 2:
        if sys.argv[1] == "new":
            shutil.copyfile(templateFolder + "/acmdsets/ACmdSets.json", os.path.expanduser('~') + "/.anpp/ACmdSets.json")
        elif sys.argv[1] == "config":
            shutil.copyfile(currentFolder + "/ACmdSets.json", os.path.expanduser('~') + "/.anpp/ACmdSets.json")
    else:
        configFile = open(os.path.expanduser('~') + "/.anpp/ACmdSets.json")
        config = json.load(configFile)
        cmdWindow = CmdWindow(config)
        

def main():
    exePath = os.path.abspath(__file__)
    folder = os.path.dirname(exePath)
    currentFolder = os.getcwd()
    templateFolder = os.path.join(folder, 'template')

    if len(sys.argv) == 2:
        if sys.argv[1] == "new":
            shutil.copytree(templateFolder + "/anpp", currentFolder, dirs_exist_ok=True)
    else:
        print("USAGE:")
        print("   anpp new")
        print("")
