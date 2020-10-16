#cs ----------------------------------------------------------------------------

 AutoIt Version: 3.3.14.5
 Author:         Brain4Tech

 Script Function:
	Console for GA2W, as GUIs in Python are complete rubbish.


#ce ----------------------------------------------------------------------------

; Script Start - Add your code below here

;Start with including some Scripts for the GUI
	#include <EditConstants.au3>
	#include <GUIConstantsEx.au3>
	#include <WindowsConstants.au3>
	#include <ColorConstants.au3>
	#include <GuiEdit.au3>
	#include <Misc.au3>
	#include <Array.au3>

;Set some optionflags
	Opt ("GUIOnEventMode", 1) ;Check actions within a GUI with OnEvent, not with While and Switch
	Opt ("TrayMenuMode", 3) ;Remove the classic tray menu
	Opt ("TrayOnEventMode", 3) ;Check actions within the trayicon with OnEvent, not with While and Switch


_CreateConsoleTrayMenu ()

;Create the GUI and Traymenu
_CreateConsoleGUI ()

FileChangeDir ("..\..\")
$filedir = @WorkingDir & "\data\communication\console-ready.txt"

;Delete Files
FileDelete (@WorkingDir & "\data\communication\console.txt")
FileDelete (@WorkingDir & "\data\communication\console-ready.txt")
FileDelete (@WorkingDir & "\data\communication\evm.txt")
FileDelete (@WorkingDir & "\data\communication\evm-ready.txt")
FileDelete (@WorkingDir & "\data\communication\main.txt")
FileDelete (@WorkingDir & "\data\communication\main-ready.txt")


Func _CreateConsoleGUI () ;Create the console GUI

	Global $hMain = GUICreate("GoogleAssistant2Windows Console", 800, 300, 200, 120, BitOR ($WS_SYSMENU, $WS_MINIMIZEBOX))
	 GUISetOnEvent ($GUI_EVENT_CLOSE, "_HideConsoleGUI")
	 GUISetOnEvent ($GUI_EVENT_MINIMIZE, "_MinimizeConsole")
	 GUISetBkColor ($COLOR_WHITE)

	Global $iEdit = GUICtrlCreateEdit("", 8, 8, 777, 230, BitOR($ES_READONLY, $ES_WANTRETURN, $ES_AUTOVSCROLL, $WS_VSCROLL))
	 GUICtrlSetBkColor (-1, $COLOR_WHITE)

	Global $iInput = GUICtrlCreateInput("", 8, 245, 777, 20, $ES_WANTRETURN)
	 GUICtrlSetOnEvent (-1, "_SendInput")
	 GUICtrlSetState (-1, $GUI_FOCUS)

	GUISetState(@SW_SHOW, $hMain)

EndFunc

Func _SendInput ()
	$input = GUICtrlRead ($iInput)
	GUICtrlSetData ($iInput, "")

	If $input = "" Then
		Return
	Else
		_SendEMMessage ("CONSOLE MESSAGE: <" & $input & ">")
		_ProcessCmd($input)
	EndIf

EndFunc

Func _HideConsoleGUI ()
	TraySetState (1)
	GUISetState (@SW_HIDE)
	_SendEMMessage ("User pressed closebutton of UI. Hiding the console.")
	_ConsoleLog ("Hid the console.", 1)
EndFunc

Func _HideConsole ()
	TraySetState (1)
	GUISetState (@SW_HIDE)
	_SendEMMessage ("User issued command <hide>. Hiding the console.")
	_ConsoleLog ("Hid the console.", 2)
EndFunc

Func _MinimizeConsole () ;Minimize GUI
	GUISetState(@SW_MINIMIZE, $hMain)
EndFunc

Func _RestoreConsole () ;Restore GUI
	TraySetState (2)
	GUISetState (@SW_SHOW)
	_SendEMMessage ("User used trayicon to restore the console. Restoring console.")
	_ConsoleLog ("Console restored", 1)
EndFunc

Func _ConsoleLog ($message, $mprefix=0, $time = 0)
	If $time = 0 Then
		$time = @HOUR & ":" & @MIN & ":" & @SEC
	EndIf

	If $mprefix = 1 Then
		$sprefix = "[" & $time & "] "
	ElseIf $mprefix = 2 Then
		$sprefix = ">   "
	ElseIf $mprefix = 3 Then
		$sprefix = "     "
	Else
		$sprefix = ""
	EndIf

	_GUICtrlEdit_AppendText ($iEdit, $sprefix & $message & @CRLF)

EndFunc

Func _ConsoleLogArray ($array)
	For $i = 0 To UBound ($array) -1
		_ConsoleLog ($array[$i])
	Next

EndFunc

Func _ProcessCmd ($command)

	_ConsoleLog ("<" & $command & ">", 1)

	$command_split  =  StringSplit ($command, " ")
	$cmd = $command_split[1]

	Local $commandList = [["hide", "_HideConsole"], ["stop", "_Terminate"], ["quit", "_Terminate"], ["clear", "_ClearConsole"], ["cls", "_ClearConsole"], ["help", "_LogHelp"], ["?", "_LogHelp"], ["send", "_SendTMessage"]]

	$function = ""

	For $i = 0 To UBound($commandList)-1
		If $commandList[$i][0] = $cmd Then

			$function = $commandList [$i][1]
		EndIf
	Next

	If $function <> "" Then
		If $cmd = "send" Then
			_SendTMessage ($command_split)
		Else
			Call ($function)
		EndIf

	Else
		_ConsoleLog ("Unknown command. Type <help> for more information.", 2)
		_SendEMMessage ("User issued command <" & $cmd & ">, which is an unknown command. Ignoring it.")
	EndIf


EndFunc

Func _Terminate ()
	_ConsoleLog ("Shutting down console", 2)
	_SendEMMessage ("User issued command <quit>. Shutting down console.", 2)
	Sleep(1000)
	Exit
EndFunc

Func _ClearConsole ()
	GUICtrlSetData ($iEdit, "")
	_SendEMMessage ("User issued command <clear>. Clearing Console.")
EndFunc

Func _LogHelp ()

	Local $helptext = [">   The following general commands are documented:", _
        "  quit	Shuts down the application", _
        "  hide	Hides the console and creates a trayicon." & @CRLF & "	You can restore the console by right-clicking on this trayicon.", _
        "  clear	Clears the console output"]

	_ConsoleLogArray ($helptext)
	_SendEMMessage ("User issued command <help>. Showing help text.")
EndFunc

Func _SendTMessage ($strMessage)
	$path = @WorkingDir & "\data\communication"

	$completeMessage = ""

	For $i = 2 To UBound ($strMessage) -1
		$completeMessage = $completeMessage & " " & $strMessage[$i]
	Next

	ConsoleWrite($completeMessage & @CRLF)

	FileOpen ($path & "\main.txt")
	FileWrite ($path & "\main.txt", "send" & @CRLF)
	FileWrite ($path & "\main.txt", $completeMessage)
	FileClose ($path & "\main.txt")

	FileMove ($path & "\main.txt", $path  & "\main-ready.txt")
	FileDelete ($path & "\main.txt")

EndFunc

Func _SendEMMessage ($completeMessage, $intLevel=1, $strTime=0)
	$path = @WorkingDir & "\data\communication"


	FileOpen ($path & "\evm.txt")
	FileWrite ($path & "\evm.txt", $completeMessage & @CRLF)
	FileWrite ($path & "\evm.txt", $intLevel & @CRLF)
	FileWrite ($path & "\evm.txt", $strTime)
	FileClose ($path & "\evm.txt")

	FileMove ($path & "\evm.txt", $path & "\evm-ready.txt")
	FileDelete ($path & "\evm.txt")

	Sleep (100)

EndFunc

Func _CreateConsoleTrayMenu () ;Create a custom trayicon-menu

	TrayCreateItem ("Restore Console")
	TrayItemSetOnEvent (-1, "_RestoreConsole")
	TraySetState (2)

EndFunc

While 1
	Sleep (100)

	If FileExists ($filedir) Then
		$aFile = FileReadToArray($filedir)
		;_ArrayDisplay ($aFile)
		_ConsoleLog ($aFile[0], $aFile[1], $aFile[2])
		FileDelete ($filedir)
	EndIf
WEnd
