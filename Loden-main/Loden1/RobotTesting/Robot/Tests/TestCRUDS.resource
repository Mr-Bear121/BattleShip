*** Settings ***
| Documentation | this robot file is working in  tandem with "MessageOperations.java" to test this application.
| Library | Process

*** Variables ***
| ${Socket_Address} | https://nqppg18xe6.execute-api.us-east-2.amazonaws.com/Alpha/rampresource
| ${cTest_Case} | RobotTesting.JavBot.TestClient


*** Keywords ***
| Test CRUDS | [Documentation] | Tests "MessageOperations.java"`s "Create" statement.
|			| [Arguments]	 | ${Jar} | ${Test} | ${CRUDS_OP}
|                       | Log | File:${Jar}
|                       | Log | Program:${Test}
|                       | Log | Full path:${Jar} ${Test}
|			| Run Process	 | Java | -classpath | ${Jar} | ${Test} | ${CRUDS_OP} | alias=Connect
|			| ${Result}	 | Get Process Result | Connect
|                       | Log | NetWork Code:${Result.stdout}
|                       | RETURN | ${Result}
