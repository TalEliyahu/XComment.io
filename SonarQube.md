# SonarQube Installation and GitHub Integration

One Paragraph of project description goes here

## Getting Started

These instructions will get you knowledge of how to use sonar scanner on your local machine and add this project to sonarcloud, all examples are given for linux machine.

### Prerequisites

Operating system on which our project files are and proper version of sonar scanner and available there by your user.
GitHub account which you will able to link with sonarcloud.

### Installing

Go to
https://sonarcloud.io/sessions/new
![SonarCloud login](https://user-images.githubusercontent.com/26525441/30324723-9b113576-97f4-11e7-9947-871d4adae23b.JPG)

and authorize with your GitHub account.
![SonarCloud page after login](https://user-images.githubusercontent.com/26525441/30324721-9b0a0710-97f4-11e7-802d-09d919bbb0a6.JPG)

Prepare your organization - "My Account > Organizations".
![SonarCloud login](https://user-images.githubusercontent.com/26525441/30324720-9b092a48-97f4-11e7-8470-9f26e8b901a4.JPG)

Generate an authentication token - "My Account > Security".
![SonarCloud login](https://user-images.githubusercontent.com/26525441/30324724-9b27f3a6-97f4-11e7-8142-221c6ae46eeb.JPG)

Download sonar scanner for your operating system (where project files are located) from
https://docs.sonarqube.org/display/SCAN/Analyzing+with+SonarQube+Scanner
```
wget https://sonarsource.bintray.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-3.0.3.778-linux.zip
```
![SonarCloud login](https://user-images.githubusercontent.com/26525441/30324726-9b297a5a-97f4-11e7-9eed-afe56e4b421d.JPG)

Unzip it in some directory where your user has permissions to use it.
```
ls
unzip sonar-scanner-cli-3.0.3.778-linux.zip
```
![SonarCloud login](https://user-images.githubusercontent.com/26525441/30324725-9b297a64-97f4-11e7-93ae-1922b82237b7.JPG)

Create "sonar-project.properties" file in your project's root and fill it as follows:
```
cd myproject
vi sonar-project.properties
```
![SonarCloud login](https://user-images.githubusercontent.com/26525441/30324728-9b2d040e-97f4-11e7-8d65-3a5c8b3941e2.JPG)
```
sonar.projectKey=your_project_key_that_must_be_unique
sonar.sources=.
sonar.host.url=https://sonarcloud.io
sonar.organization=your_organization_key
sonar.login=authenticated_token
```
![SonarCloud login](https://user-images.githubusercontent.com/26525441/30324727-9b2b10d6-97f4-11e7-81eb-8c8226c6ca20.JPG)

where:
  - "sonar.projectKey" is friendly name to recognize your project.
  - "sonar.organization" is name of your organization, you can find it at - "My Account > Organizations" and it looks like "<your_github_username>-github"
  - "sonar.login" is autherntication token generated at "My Account > Security" from the step above.

## Running scans

Now you can run scans from your OS, for that you need to specify the path to sonar-scanner executable.
It located in "bin" directory, which is in root of sonar scanner's unzipped folder.
```
ls
cd sonar-scanner-3.0.3.778-linux/
ls
pwd
```
![SonarCloud login](https://user-images.githubusercontent.com/26525441/30324729-9b318312-97f4-11e7-9c89-eff443cc1f50.JPG)

Easiest way is to use absolute path to it from your project's root (where sonar-project.properties file that we created earlier is located). Add "-X" or "--debug" at the end if you need more detailed (DEBUG) output.
```
ls
cd myproject
/home/user/sonar-scanner-3.0.3.778-linux/bin/sonar-scanner -X
```
![SonarCloud login](https://user-images.githubusercontent.com/26525441/30324718-9b0776ee-97f4-11e7-9019-75354f2430e8.JPG)


![SonarCloud login](https://user-images.githubusercontent.com/26525441/30324719-9b08aea6-97f4-11e7-90e9-b5e51883ae90.JPG)

You can find more information about scanner on it's documentation page:
https://docs.sonarqube.org/display/SCAN/Analyzing+with+SonarQube+Scanner

Now you can go to https://sonarcloud.io/ and find analysis result of your project at "Project" tab or via link that was given inside output of your scan.
![SonarCloud login](https://user-images.githubusercontent.com/26525441/30324722-9b0c0150-97f4-11e7-91ea-38b7f510b86c.JPG)
