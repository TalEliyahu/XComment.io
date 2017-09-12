This plugin removes comments from source files for a number of programming languages. Required Python 3 on Jenkins server.
A new build step is added: 'Invoke Comments Remover' which accepts files to process as input and creates uncommented
version of them. 

User can specify Python path in global settings for the plugin (otherwise the one on the system PATH is used).

Before build:
Put ZIP archive of Comments Remover (in Python) in src/main/resources. The plugin will look for the archive
and attempt to run 'comment_remover.py' in it. Also expects to have requirement.txt at top level of the archive.

Debug:
mvnDebug hpi:run
You can attach Java Debugger to a local Java process of Jenkins.

Prepare plugin for distribution:
mvn package
The *.hpi file will be created in target/ directory.
To install manually on local Jenkins, copy it to $JENKINS_HOME/plugins directory.

