import os
import shutil
import ctypes
import sys
import shelve

if os.path.dirname(__file__) != "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup": # check if file is in the startup folder
    if ctypes.windll.shell32.IsUserAnAdmin() == 0: # check if the file has admin
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1) > 32, exit() # request admin if not
    else: # copy the file to its new location if it has admin
        s = shelve.open("DownloadManager")
        a = s["FilePath"]
        s.close()
        s = shelve.open("C:\ProgramData\Microsoft\Windows\Start Menu\Programs/pyDM")
        s["FilePath"] = a
        s.close()
        shutil.copy2(str(__file__), "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp")

r = shelve.open("C:\ProgramData\Microsoft\Windows\Start Menu\Programs/pyDM") # store the directory of the amf for future startups
afmdir = r["FilePath"]
r.close()
afmPath = afmdir + "/afm.bat"
os.system("python" + str(afmPath))