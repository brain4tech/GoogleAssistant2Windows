#Region ;**** Directives created by AutoIt3Wrapper_GUI ****
#AutoIt3Wrapper_Icon=..\..\media\GA2W-logo.ico
#AutoIt3Wrapper_Res_Description=Console (2020-10-20)
#AutoIt3Wrapper_Res_Fileversion=0.1.0.0
#AutoIt3Wrapper_AU3Check_Stop_OnWarning=y
#EndRegion ;**** Directives created by AutoIt3Wrapper_GUI ****
; compiler information for AutoIt

; opt and just singleton -------------------------------------------------------
Opt( 'GUIOnEventMode', 1 )   ; Enable OnEvent function notification for the Gui, instead of using GUIGetMsg() (in a while loop).
Opt( 'MustDeclareVars', 1 )  ; Variables must be pre-declared.
Opt( 'TrayMenuMode', 1 + 2 ) ; Remove default tray menu for custom tray menu.
Opt( 'TrayOnEventMode', 1 )  ; Enable OnEvent function notification for the tray menu.

Global $aInst = ProcessList( 'GA2W Console.exe' )
If $aInst[0][0] > 1 Then Exit



; includes ---------------------------------------------------------------------
#include-once
#include <GUIConstantsEx.au3>
#include <GuiEdit.au3>
#include <File.au3>
#include <String.au3>
#include <WindowsConstants.au3>



; declaration ------------------------------------------------------------------
Global $sPathCommunication    = _PathFull( '..\data\communication\' )
Global $sFilePathConsole      = $sPathCommunication & 'console.txt'
Global $sFilePathConsoleReady = $sPathCommunication & 'console-ready.txt'
Global $sFilePathEvm          = $sPathCommunication & 'evm.txt'
Global $sFilePathEvmReady     = $sPathCommunication & 'evm-ready.txt'
Global $sFilePathMain         = $sPathCommunication & 'main.txt'
Global $sFilePathMainReady    = $sPathCommunication & 'main-ready.txt'
Global $sFilePathTerminate	  = $sPathCommunication & 'terminate.txt'
Global $sFilePathInterpreter  = $sPathCommunication & 'interpreter-ready.txt'

Global $hGui, $cEventLog, $cUserInput



; processing -------------------------------------------------------------------
;_cleanupOldData()
_createCustomTrayMenu()
_createGui()
_setGuiEvents()
_readFileLoop()

Func _cleanupOldData()
    FileDelete( $sFilePathConsole )
    FileDelete( $sFilePathConsoleReady )
    FileDelete( $sFilePathEvm )
    FileDelete( $sFilePathEvmReady )
    FileDelete( $sFilePathMain )
    FileDelete( $sFilePathMainReady )
	FileDelete ( $sFilePathTerminate )
EndFunc

Func _createCustomTrayMenu()
    Local $cTrayItem = TrayCreateItem( 'Restore console' )
    TrayItemSetOnEvent( $cTrayItem, '_restoreConsole' )

    Local Const $iHideTrayIcon = 2
    TraySetState( $iHideTrayIcon )
EndFunc

Func _createGui()
    Local $iGuiWidth     = 800
    Local $iGuiHeight    = 300
    Local $iGuiXPosition = Default
    Local $iGuiYPosition = Default

    $hGui       = GUICreate( 'GoogleAssistant2Windows Console', $iGuiWidth, $iGuiHeight, $iGuiXPosition, $iGuiYPosition, BitOR( $WS_SYSMENU, $WS_MINIMIZEBOX ) )
    $cEventLog  = GUICtrlCreateEdit( '', 10, 10, $iGuiWidth - 25, $iGuiHeight -70, BitOR( $ES_READONLY, $ES_WANTRETURN, $ES_AUTOVSCROLL, $WS_VSCROLL ) )
    $cUserInput = GUICtrlCreateInput( '', 10, $iGuiHeight - 55, $iGuiWidth - 25, 20, $ES_WANTRETURN )

    GUICtrlSetBkColor( $cEventLog, 0xFFFFFF )
    ;GUICtrlSetFont( $cEventLog, 9, Default, Default, 'Consolas' )
    ;GUICtrlSetFont( $cUserInput, 9)
    GUICtrlSetState( $cUserInput, $GUI_FOCUS )

    GUISetState( @SW_SHOW, $hGui )
EndFunc

Func _setGuiEvents()
    GUISetOnEvent( $GUI_EVENT_MINIMIZE, '_minimizeConsole', $hGui )
    GUISetOnEvent( $GUI_EVENT_CLOSE, '_closeConsole', $hGui )
    GUICtrlSetOnEvent( $cUserInput, '_processUserInput' )
EndFunc

Func _readFileLoop()
    While 1
        If FileExists( $sFilePathConsoleReady ) Then
            Local $aFileContentList = FileReadToArray( $sFilePathConsoleReady )
            ;_ArrayDisplay( $aFileContentList )
            Local $sMessage         = $aFileContentList[0]
            Local $iMode            = $aFileContentList[1]
            Local $sTime            = $aFileContentList[2]

            _addConsoleLogEntry( $sMessage, $iMode, $sTime )
            FileDelete( $sFilePathConsoleReady )
        EndIf

		If FileExists( $sFilePathInterpreter ) Then
            Local $aFileContentList = FileReadToArray( $sFilePathInterpreter )
            ;_ArrayDisplay( $aFileContentList )
			Local $iFileReadCount = UBound ($aFileContentList) -1

			If $iFileReadCount == 0 Then
				_addConsoleLogEntry( $aFileContentList[0], 2, 0 )
			Else
				For $i = 0 To $iFileReadCount Step 1
					_addConsoleLogEntry( $aFileContentList[$i], 3, 0 )
				Next
			EndIf


            FileDelete( $sFilePathInterpreter )
        EndIf

        Sleep( 150 )
    WEnd
EndFunc

Func _minimizeConsole()
    GUISetState( @SW_MINIMIZE, $hGui )
EndFunc

Func _closeConsole()
    _addConsoleLogEntry( 'Hide the console.', 1 )
    _writeEventReadyFile( 'User pressed close button. Hiding the console.' )
    _showTrayIconHideGui()
EndFunc

Func _processUserInput()
    Local $sUserInput = StringLower( GUICtrlRead( $cUserInput ) )

    If $sUserInput == '' Then
        Return
    EndIf

    GUICtrlSetData( $cUserInput, '' )

    _writeEventReadyFile( 'Console message: <' & $sUserInput & '>' )
    _executeCommand( $sUserInput )
EndFunc

Func _hideTrayIconShowGui()
    Local Const $iHideTrayIcon = 2
    TraySetState( $iHideTrayIcon )

    GUISetState( @SW_SHOW, $hGui )
EndFunc

Func _showTrayIconHideGui()
    Local Const $iShowTrayIcon = 1
    TraySetState( $iShowTrayIcon )

    GUISetState( @SW_HIDE, $hGui )
EndFunc

Func _restoreConsole()
    _addConsoleLogEntry( 'Console restored.', 1 )
    _writeEventReadyFile( 'User used tray icon to restore the console. Restoring console.' )
    _hideTrayIconShowGui()
EndFunc

Func _addConsoleLogEntry( $sMessage, $iMode = 0, $sTime = 0 )
    If $sTime == 0 Then
        $sTime = @HOUR & ':' & @MIN & ':' & @SEC
    EndIf

    Switch $iMode
        Case 1
            $sMessage = _StringRepeat( '-', 100 ) & @CRLF & '[' & $sTime & '] ' & $sMessage
        Case 2
            $sMessage = '> ' & $sMessage
        Case 3
            $sMessage = '  ' & $sMessage
		Case 4
			$sMessage = '' & $sMessage
    EndSwitch

    _GUICtrlEdit_AppendText( $cEventLog, $sMessage & @CRLF )
EndFunc

Func _executeCommand( $sUserInput )
    _addConsoleLogEntry( '<' & $sUserInput & '>', 1 )

    Local $aCommandTable = _
        [ _
            ['help',   '_helpInformation'], _
            ['--help', '_helpInformation'], _
            ['-h',     '_helpInformation'], _
            ['-?',     '_helpInformation'], _
            ['?',      '_helpInformation'], _
            ['clear',  '_clearConsole'], _
            ['cls',    '_clearConsole'], _
            ['hide',   '_hideConsole'], _
            ['quit',   '_terminateConsole'], _
            ['stop',   '_terminateConsole'], _
            ['send',   '_writeMainReadyFile'], _
			['m',	   '_writeMainReadyFile'], _
			['i',	   '_writeMainReadyFile'], _
			['online', '_writeMainReadyFile'], _
			['on', '_writeMainReadyFile'], _
			['om', '_writeMainReadyFile'] _
        ]

    Local $aUserInputList    = StringSplit( $sUserInput, ' ' )
    Local $sUserCommand      = $aUserInputList[1]
    Local $iCommandListCount = UBound( $aCommandTable ) - 1

    For $i = 0 To $iCommandListCount Step 1
        Local $sCommand = $aCommandTable[$i][0]

        If $sCommand == $sUserCommand Then

			If $sCommand == 'send' Then
				_writeMainReadyFile( $aUserInputList )
                Return
			ElseIf $sCommand == 'm' OR $sCommand == 'i' Then
				_writeMainReadyFile( $aUserInputList )
                Return
			ElseIf $sCommand == 'online' OR $sCommand == 'on' OR $sCommand == 'om' Then
				_writeMainReadyFile( $aUserInputList )
                Return
			Else
				Local $sFunctionName = $aCommandTable[$i][1]
                Call( $sFunctionName )
                Return
			EndIf

		EndIf
    Next

    _addConsoleLogEntry( 'Unknown command. Type <help> for more information.', 2 )
    _writeEventReadyFile( 'User typed <' & $sUserCommand & '> which is an unknown command. Ignoring it.' )
EndFunc

Func _helpInformation()
    Local $sHelpInformation = _
        '> The following general commands are documented:' & @CRLF & _
        '  |-- clear, cls		: Clears the console output.' & @CRLF & _
        '  |-- help, --help, -h, -?, ?	: Shows this help information.' & @CRLF & _
        '  |-- hide			: Hides the console and creates a tray icon.' & @CRLF & _
        '  |			  You can restore the console by right-clicking on the tray icon.' & @CRLF & _
        '  |-- m, --i			: Manually enter a command and send it to the interpreter.' & @CRLF & _
        '  |			  ["m" --> manually, "i" --> interpreter' & @CRLF & _
		'  |--online, --on, --om		: Toggle onlinemode [-true (default) or -false]' & @CRLF & _
        '  |			  Whether the program should be able to receive telegram-messages' & @CRLF & _
        '  |-- quit, stop		: Shutdown the application.'

    _addConsoleLogEntry( $sHelpInformation , 4)
    _writeEventReadyFile( 'User typed <help>. Showing help text.' )
EndFunc

Func _clearConsole()
    GUICtrlSetData( $cEventLog, '' )
    _writeEventReadyFile( 'User typed <clear>. Clearing console.' )
EndFunc

Func _hideConsole()
    _addConsoleLogEntry( 'Hide the console.', 2 )
    _writeEventReadyFile( 'User typed <hide>. Hiding the console.' )
    _showTrayIconHideGui()
EndFunc

Func _terminateConsole()
    _writeEventReadyFile( 'User typed <quit>. Program is terminating.', 2 )
	_addConsoleLogEntry( 'Shutting down background processes ...', 2 )

	FileOpen($sFilePathTerminate, 1)

	_addConsoleLogEntry( 'Terminating console ...', 2 )
	_addConsoleLogEntry( 'Bye!', 2 )

	Sleep(1000 )

    Exit
EndFunc

Func _writeMainReadyFile( $aCommandStringList )
    Local $sCommand = $aCommandStringList[1]

    _ArrayDelete( $aCommandStringList, 0 )
    _ArrayDelete( $aCommandStringList, 0 )

    Local $sMessage         = _ArrayToString( $aCommandStringList, ' ' )
    Local $sCompleteMessage = $sCommand & @CRLF & $sMessage

    _writeFile( $sFilePathMain, $sCompleteMessage )
    _transformToReadyFile( $sFilePathMain, $sFilePathMainReady )
EndFunc

Func _writeEventReadyFile( $sMessage, $iLevel = 1, $sTime = 0 )
    Local $sCompleteMessage = $sMessage & @CRLF & $iLevel & @CRLF & $sTime

    _writeFile( $sFilePathEvm, $sCompleteMessage )
    _transformToReadyFile( $sFilePathEvm, $sFilePathEvmReady )

    Sleep( 150 )
EndFunc

Func _writeFile( $sFile, $sText )
    Local Const $iWriteModeCreateDirectoryUtf8 = 2 + 8 + 256
    Local $hFile = FileOpen( $sFile, $iWriteModeCreateDirectoryUtf8 )
    FileWrite( $hFile, $sText )
    FileClose( $hFile )
EndFunc

Func _transformToReadyFile( $sFromFile, $sToFile )
    Local Const $iOverwriteCreateDirectory = 1 + 8
    FileMove( $sFromFile, $sToFile, $iOverwriteCreateDirectory )
    FileDelete( $sFromFile )
EndFunc
