import os
import sys
import shutil

def main():
    exePath = os.path.abspath(__file__)
    folder = os.path.dirname(exePath)
    currentFolder = os.getcwd()
    templateFolder = os.path.join(folder, 'template')

    if len(sys.argv) == 2:
        if sys.argv[1] == "new":
            shutil.copytree(templateFolder, currentFolder, dirs_exist_ok=True)
    else:
        print("USAGE:")
        print("   anpp new")
        print("")
