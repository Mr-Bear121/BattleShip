| *** Settings ***
| Documentation	| Testing ${Program_File} connection method
| Library	| Process


| *** Variables ***
| ${Socket_Address} | https://nqppg18xe6.execute-api.us-east-2.amazonaws.com/Alpha/rampresource
| ${Jar_Path} | ../../../dist/AWS_Client.jar
| ${Test_Case} | RobotTesting.JavBot.TestClient
| ${location} | -classpath AWS_Client.jar RobotTesting.JavBot.TestClient

| *** Keywords ***
| Test Connection      | [Documentation] | Attempt to get a response code from "getResponseCode" after running " HttpURLConnection"
|			| [Arguments]	 | ${Jar} | ${Test} | ${Address}
|                       | Log | File:${Jar}
|                       | Log | Program:${Test}
|                       | Log | Address:${Address}
|                       | Log | Full path:${Jar} ${Test}
|			| Run Process	 | Java | -classpath | ${Jar} | ${Test} | ${Address} | alias=Connect
|			| ${Result}	 | Get Process Result | Connect
|                       | Log | NetWork Code:${Result.stdout}
|                       | RETURN | ${Result}
