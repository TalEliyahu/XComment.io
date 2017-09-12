# Name of your Project goes here

One Paragraph of project description goes here

## Getting Started

These instructions will get you knowledge of how to use sonar scanner on your local machine and add this project to sonarcloud, all examples are given for linux machine.

### Prerequisites

Operating system on which our project files are and proper version of sonar scanner and available there by your user.
GitHub account which you will able to link with sonarcloud.

### Installing

Go to
https://sonarcloud.io/sessions/new
![SonarCloud login](https://user-images.githubusercontent.com/26525441/30277114-6a8bc878-9739-11e7-9ff1-2d1f2424638d.JPG)

and authorize with your GitHub account.
![SonarCloud page after login](https://user-images.githubusercontent.com/26525441/30277115-6a8bec18-9739-11e7-8cdb-5a02a4b75397.JPG)

Prepare your organization - "My Account > Organizations".
![SonarCloud login](https://user-images.githubusercontent.com/26525441/30279315-6e85c4fa-973f-11e7-84fa-b224a866edc5.JPG)

Generate an authentication token - "My Account > Security".
![SonarCloud login](https://user-images.githubusercontent.com/26525441/30279316-6e9377d0-973f-11e7-986d-19d5f18bc925.JPG)

Download sonar scanner for your operating system (where project files are located) from
https://docs.sonarqube.org/display/SCAN/Analyzing+with+SonarQube+Scanner
```
wget https://sonarsource.bintray.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-3.0.3.778-linux.zip
```
![SonarCloud login](https://user-images.githubusercontent.com/26525441/30279317-6e945560-973f-11e7-9480-cc70dfb606d2.JPG)

Unzip it in some directory where your user has permissions to use it.
```
ls
unzip sonar-scanner-cli-3.0.3.778-linux.zip
```
![SonarCloud login](https://user-images.githubusercontent.com/26525441/30279319-6e968af6-973f-11e7-9d39-6771c1725808.JPG)

Create "sonar-project.properties" file in your project's root and fill it as follows:
```
cd myproject
vi sonar-project.properties
```
![SonarCloud login](https://user-images.githubusercontent.com/26525441/30279321-6e9d8e0a-973f-11e7-9689-8d646d75867a.JPG)
```
sonar.projectKey=your_project_key_that_must_be_unique
sonar.sources=.
sonar.host.url=https://sonarcloud.io
sonar.organization=your_organization_key
sonar.login=authenticated_token
```
![SonarCloud login](https://user-images.githubusercontent.com/26525441/30279318-6e957698-973f-11e7-8f73-cc35cad60068.JPG)

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
![SonarCloud login](https://user-images.githubusercontent.com/26525441/30279322-6eae47fe-973f-11e7-8d8e-3c36aa151f8b.JPG)

Easiest way is to use absolute path to it from your project's root (where sonar-project.properties file that we created earlier is located). Add "-X" or "--debug" at the end if you need more detailed (DEBUG) output.
```
ls
cd myproject
/home/user/sonar-scanner-3.0.3.778-linux/bin/sonar-scanner -X
```
![SonarCloud login](https://user-images.githubusercontent.com/26525441/30279324-6eb49d02-973f-11e7-820f-8c47992ba9fb.JPG)


![SonarCloud login](https://user-images.githubusercontent.com/26525441/30279323-6eb33c5a-973f-11e7-8041-8fde0216dc35.JPG)

You can find more information about scanner on it's documentation page:
https://docs.sonarqube.org/display/SCAN/Analyzing+with+SonarQube+Scanner

Now you can go to https://sonarcloud.io/ and find analysis result of your project at "Project" tab or via link that was given inside output of your scan.
![SonarCloud login](https://user-images.githubusercontent.com/26525441/30282315-814b5548-9747-11e7-9cc3-6b4498fa9cdb.JPG)
