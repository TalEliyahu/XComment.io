# Comments Remover Jenkins plugin

This plugin removes comments from source files for a number of programming languages. Required Python 3 on Jenkins server.
A new build step is added: 'Invoke Comments Remover' which accepts files to process as input and creates uncommented
version of them. 

User can specify Python path in global settings for the plugin (otherwise the one on the system PATH is used).

### Before build
Put ZIP archive of Comments Remover (in Python) in `src/main/resources`.
The plugin expects to find `comment_remover.py`  and `requirement.txt` in the archive.

### Debug
`mvnDebug hpi:run`

You can attach Java Debugger to a local Java process of Jenkins.

### Prepare plugin for distribution
`mvn package`

The *.hpi file will be created in target/ directory.
To install manually on local Jenkins, copy it to $JENKINS_HOME/plugins directory.


# Global settings

Go to Manage Jenkins -> Configure System to access them

![settings](images/1.png "Settings")

![settings](images/2.png "Settings")

![settings](images/3.png "Settings")

There is help section to provide examples:

![settings](images/4.png "Settings")


# Usage

The plugin can be used wherever build steps can be defined, e.g. Freestyle project

![job](images/5.png "Job")

Adding build step:

![build](images/6.png "Build")

![build step](images/7.png "Build step")

This part also has "help" section:

![build step help](images/8.png "Build step help")

##### Example of build output and result:

![build output](images/9.png "Build output")

![build result](images/10.png "Build result")

![build result](images/11.png "Build result")