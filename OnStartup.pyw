import os
import shutil
import ctypes
import sys
import shelve

if os.path.dirname(__file__) != "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup":
    if ctypes.windll.shell32.IsUserAnAdmin() == 0:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1) > 32, exit()
    else:
        s = shelve.open("DownloadManager")
        a = s["FilePath"]
        s.close()
        s = shelve.open("C:\ProgramData\Microsoft\Windows\Start Menu\Programs/pyDM")
        s["FilePath"] = a
        s.close()
        shutil.copy2(str(__file__), "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp")
else:
    r = shelve.open("C:\ProgramData\Microsoft\Windows\Start Menu\Programs/pyDM")
    afmdir = r["FilePath"]
    r.close()
    afmPath = afmdir + "/afm.vbs"
    os.system("d:")
    os.chdir(afmdir)
    os.system("afm.bat")