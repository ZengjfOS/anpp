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

    DEFAULT_CONFIG_PATH = templateFolder + "/acmdsets/ACmdSets.json"
    HOME_CONFIG_PATH = os.path.expanduser('~') + "/.anpp/ACmdSets.json"
    CURRENT_DIR_CONFIG_PATH = currentFolder + "/ACmdSets.json"

    if not os.path.exists(os.path.expanduser('~') + "/.anpp"):
        os.mkdir(os.path.expanduser('~') + "/.anpp")
        shutil.copyfile(DEFAULT_CONFIG_PATH, HOME_CONFIG_PATH)

    if len(sys.argv) == 2:
        if sys.argv[1] == "new":
            shutil.copyfile(DEFAULT_CONFIG_PATH, HOME_CONFIG_PATH)
        elif sys.argv[1] == "config":
            shutil.copyfile(CURRENT_DIR_CONFIG_PATH, HOME_CONFIG_PATH)
    else:
        configFilePath = HOME_CONFIG_PATH
        if os.path.exists(CURRENT_DIR_CONFIG_PATH):
            configFilePath = CURRENT_DIR_CONFIG_PATH

        configFile = open(configFilePath)
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
