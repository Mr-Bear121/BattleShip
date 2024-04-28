*** Settings ***
| Documentation | this robot file is working in  tandem with "TestClient.java" to test this application.
| Library | Process
| Library | Dialogs
| Library | String
| Resource | ./ClientConnectionTest.resource
| Resource | ./Tests/TestCRUDS.resource

*** Variables ***
| @{options} | ConnectionTest | CreateTest | ReadTest | UpdateTest | DeleteTest | SearchTest
| ${Create_Test_Case} | test


*** Keywords ***
| Select Test Dialog | [Documentation] | Determines what action the user wishes to take via dialog box
|            | ${selection} | Get Selection From User | Network Testing | @{options}
|            | RETURN FROM KEYWORD | ${selection}

| Run Selected Operation | [Documentation] | Select a Test based on selected dialog option
| 	     | [Arguments] | ${Option}
| 	     | ${Option} | Convert To Lower Case | ${Option}
| 	     | ${Condition} | Set Variable | 200 


| 	     | Log To Console | TestCase:${Option}


| 	     | IF | '${Option}' == 'connectiontest'

| 	     | ${Result} | Test Connection | ${Jar_Path} | ${Test_Case} | ${Socket_Address}

|            | Should Be Equal As Integers | ${Result.stdout} | 200 | Connection was not established correctly

| 	     | ELSE IF | '${Option}' == 'createtest' 


| 	     | ${Result} | Test CRUDS | ${Jar_Path} | ${cTest_Case} | create

|            | Should Be Equal | ${Result.stdout} | ${Condition}

| 	     | ELSE IF | '${Option}' == 'readtest' 
| 	     |
| 	     |
| 	     | ${Result} | Test CRUDS | ${Jar_Path} | ${cTest_Case} | read
| 	     |
|            | Should Be Equal As Integers | ${Result.stdout} | 200 | Connection was not established correctly
|            |
| 	     | ELSE IF | '${Option}' == 'updatetest'
| 	     |
| 	     |
| 	     | ${Result} | Test CRUDS | ${Jar_Path} | ${cTest_Case} | update
| 	     |
|            | Should Be Equal As Integers | ${Result.stdout} | 200
|            |
| 	     | ELSE IF | '${Option}' == 'deletetest' 
| 	     |
| 	     |
| 	     | ${Result} | Test CRUDS | ${Jar_Path} | ${cTest_Case} | delete
| 	     |
|            | Should Be Equal As Integers | ${Result.stdout} | 200
|            |
| 	     | Else If | '${Option}' == 'searchtest'
| 	     |
| 	     |
| 	     | ${Result} | Test CRUDS | ${Jar_Path} | ${cTest_Case} | search
| 	     |
|            | Should Be Equal As Integers | ${Result.stdout} | 200
|            |
| 	     |
| 	     | END



*** Test Cases ***
| Get User Input | [Documentation] | Gather Input From user
|                | ${Selection} | Select Test Dialog
|                | Log | Value of ${Selection}
|                | Run Selected Operation | ${selection}