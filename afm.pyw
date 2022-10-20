import time
import os
import shutil
import DownloadManager as DM

files = []

# the automatic-file-mover

os.chdir(DM.FileHandler.DownloadPath)

while True: # check for new downloads
    os.chdir(DM.FileHandler.DownloadPath)
    time.sleep(0.1)
    for file in os.listdir(DM.FileHandler.DownloadPath): # loup through all new files in the downloads folder and check if they are an unfinished chrome download
        FN, FE = os.path.splitext(file)
        if FE != ".crdownload":
            files.append(file)

    for file in files: # move all files that are not unfinished chrome downloads
        shutil.move(os.path.abspath(file), DM.FileHandler.MDPath + "/DwNew")
    files.clear()

    for file in os.listdir(DM.FileHandler.MDPath + "/DwNew"): # check if files in the "DwNew" directory aren't actually new anymore
        os.chdir(DM.FileHandler.MDPath + "/DwNew")
        MinutesSinceDownload = (time.time() - os.path.getmtime(os.path.abspath(file))) / 60
        if MinutesSinceDownload >= 5:
            DM.FileHandler.move_file(file)