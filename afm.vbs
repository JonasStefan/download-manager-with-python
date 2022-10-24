Set oShell = CreateObject ("Wscript.Shell") 
Dim strArgs
strArgs = "cmd /c afm.pyw"
oShell.Run strArgs, 0, false