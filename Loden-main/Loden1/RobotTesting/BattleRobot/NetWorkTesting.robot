*** Settings ***
| Documentation | this robot file is working in  tandem with "Client.py" to test this application.
| Library | Process
| Library | Dialogs
| Library | String
| Resource| ../../Client/Client.py

*** Variables ***
| @{options} | ConnectionTest | Test 1 Client | Test 2 Clients
| ${test_Message} | command:end_turn:cell:{Cell},end:game over

*** Keywords ***
| Select Test Dialog | [Documentation] | Determines what action the user wishes to take via dialog box
|            | ${selection} | Get Selection From User | Network Testing | @{options}
|            | RETURN FROM KEYWORD | ${selection}

| Run Selected Operation | [Documentation] | Select a Test based on selected dialog option
| 	     | [Arguments] | ${option}
| 	     | ${expectedResponse} | testing
| 	     | IF | '${option}' == 'ConnectionTest'
| 	     | ${result} | connectClient | ${test_Message}
| 	     | Should Be Equal | ${result.stdout} | ${expectedResponse} 
|	     | ELSE IF | '${option}' == 'Test 1 Client'
|	     |
|	     | ELSE IF| '${option}' == 'Test 2 Client'
|	     |
| 	     | END



*** Test Cases ***
| Get User Input | [Documentation] | Gather Input From user
|                | ${Selection} | Select Test Dialog
|                | Log | Value of ${Selection}
|                | Run Selected Operation | ${selection}