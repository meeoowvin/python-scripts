; Wait for the file upload dialog to appear
WinWaitActive("File Upload")

; Type the file path in the "File Name" field
ControlSetText("Open", "", "Edit1", $CmdLine[1])

; Click the "Open" button
ControlClick("Open", "", "Button1")