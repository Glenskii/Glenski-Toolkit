Set fileSystem = CreateObject("Scripting.FileSystemObject")
Set shell = CreateObject("WScript.Shell")

scriptsDirectory = fileSystem.GetParentFolderName(WScript.ScriptFullName)
skillDirectory = fileSystem.GetParentFolderName(scriptsDirectory)
pythonWindowless = skillDirectory & "\.venv\Scripts\pythonw.exe"
serviceScript = skillDirectory & "\guardian_service.py"

If Not fileSystem.FileExists(pythonWindowless) Then
    WScript.Quit 1
End If

shell.CurrentDirectory = skillDirectory
shell.Run """" & pythonWindowless & """ """" & serviceScript & """ --once", 0, False
