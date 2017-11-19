XComment
========


Table of Contents
-----------------

* `XComment`_

  * `Table of Contents`
  * `Installation`_
  * `Usage`_
     * `Processing files`_
     * `Processing directories`_
     * `Archives`_
        * `Logging`_
     * `Get supported language list`_
     * `To see full CLI specification, run`_
  * `Development`_
     * `Getting Up-and-Running Locally`_
        * `Setting Things Up on Ubuntu`_
     * `Deployment`_
        * `Pip registry`_
           * `Install dependencies`_
           * `Set pypi credentials`_
           * `Create distribution`_
           * `Upload`_
  * `Tips`_

Installation
------------

.. code-block:: shell

    $ pip install XComment

Usage
-----

Use the project's CLI to interact with the script.


Processing files
++++++++++++++++

Say, you are working with the file `./tests/sources/HTML/index.html`.

Precondition: virtualenv is activated (of course).

To remove comments (output code without comments to output file) invoke

```shell
$ comments_remover ./tests/sources/HTML/input.html HTML ./
```
This will take `./tests/sources/HTML/input.html`, designated as `HTML` file, and put the copy of the former (with HTML-specific comments removed, obviously) to `./` named `rc.input.html`. The latter is the name of the original file prefixed with `rc.` by default.

To highlight comments (outputs comments only to output file) invoke

.. code-block:: shell

    $ comments_remover ./tests/sources/HTML/input.html HTML -p ./


Processing directories
++++++++++++++++++++++

If on start been specified directory path, script will be processing directory recursively with all subdirs for sources by specified language.


Archives
++++++++

For processing archived sources use option -a

Examples:

.. code-block:: shell

    $ # remove comments
    $ comments_remover ./tmp/test.zip -a Python

    $ # highlight comments
    $ comments_remover ./tmp/test.zip -a -p Python

Logging
+++++++

-l option enable logging (in stdout by default)

-f < path > specify path to log file

Example:

.. code-block:: shell

    $ comments_remover ./tmp/test.py -l -f ./remove.log Python

Get supported language list
+++++++++++++++++++++++++++

For get list supported languages use -i option.
Result list will returned in json format


.. code-block:: shell

    $ comments_remover -i

    ["PHP", "Python", "CSS", "HTML", "JavaScript", "ActionScript", "Ruby",
    "Assembly", "AppleScript", "Bash", "CSharp", "VB", "XML", "SQL", "C"]


To see full CLI specification, run
++++++++++++++++++++++++++++++++++


.. code-block:: shell

    $ comments_remover


Development
-----------


Getting Up-and-Running Locally
++++++++++++++++++++++++++++++

Tested with the following configuration:

* Ubuntu 16.04 / 17
* Python 3.6.

*Note: the below occurences of `./` refer to the project root unless explicitly stated otherwise*.


Setting Things Up on Ubuntu
~~~~~~~~~~~~~~~~~~~~~~~~~~~

#. Enter the shell.

#. Install `pyenv` via [pyenv-installer](https://github.com/pyenv/pyenv-installer):

    .. code-block:: shell

        $ curl -L https://raw.githubusercontent.com/pyenv/pyenv-installer/master/bin/pyenv-installer | bash

    .. image:: ./docs/images/pyenv-installer.png

#. Follow the instructions on how to initialize `pyenv` on shell startup, for instance:

    .. code-block:: shell

        $ echo 'export PATH="/root/.pyenv/bin:$PATH"' >> ~/.bash_profile
        $ echo 'eval "$(pyenv init -)"' >> ~/.bash_profile
        $ echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bash_profile

    .. image:: ./docs/images/initialize-pyenv-with-shell.png

#. Install Python 3.6.x via `pyenv`, say Python 3.6.2 (latest micro release versions are preferred):

    .. code-block:: shell
    
        $ pyenv install 3.6.2

    .. image:: ./docs/images/pyenv-install-3-6-2.png

#. Create a virtualenv for the project:

    .. code-block:: shell

        $ pyenv virtualenv 3.6.2 comments_remover

    .. image:: ./docs/images/pyenv-virtualenv-3.6.2-comments_remover.pngA

#. Switch to whatever directory you wish the project to reside in, say `~`:

    .. code-block:: shell

        $ cd ~

    .. image:: ./docs/images/cd-~.pngA

#. Clone the project from GitHub:
    * either via SSH (the preferred way):

    .. code-block:: shell

        $ git clone git@github.com:Singapore-Tech-Entrepreneurs/comments_remover.git

    .. image:: ./docs/images/git-clone-gitatgithub-com-singapore-tech-entrepreneurs-comments-remover-git.png

    * or via HTTPS:

    .. code-block:: shell

        $ git clone https://github.com/Singapore-Tech-Entrepreneurs/comments_remover.git

    .. image:: ./docs/images/git-clone-https-github-com-singapore-tech-entrepreneurs-comments-remover-git.png

#. Switch to the project directory:

    .. code-block:: shell

        $ cd comments_remover

    .. image:: ./docs/images/cd-comments_remover.png

#. Activate the virtualenv:

    .. code-block:: shell

        $ pyenv activate comments_remover

    .. image:: ./docs/images/pyenv-activate-comments_remover.png

#. Install project dependencies:

    .. code-block:: shell

        $ pip install -U -r ./requirements.txt

    .. image:: ./docs/images/pip-install-u-r-requirements-txt.png

#. Install dependencies for testing:

    .. code-block:: shell

        $ pip install -U -r ./requirements-test.txt

    .. image:: ./docs/images/pip-install-u-r-requirements-test-txt.png

#. (optional) Install [IPython](https://ipython.org/) interactive shell to speed up development:

    .. code-block:: shell

        $ pip install ipython==6.1.0

    .. image:: ./docs/images/pip-install-ipython-6-1-0.png
    
To run tests, simply

.. code-block:: shell

    $ pytest ./

.. image:: ./docs/images/pytest.png

To also see coverage report,

.. code-block:: shell

    pytest --cov ./

.. image:: ./docs/images/pytest-cov.png

You should be good to go now.

Deployment
++++++++++

Pip registry
~~~~~~~~~~~~

Install dependencies
********************

.. code-block:: shell

    $ python install -r requirements-deploy.txt

Set pypi credentials
********************

.. code-block:: shell

    $ export TWINE_USERNAME=<pypi username>
    $ export TWINE_PASSWORD=<pypi password>

Create distribution
*******************

.. code-block:: shell

    $ python setup.py sdist bdist_wheel


Upload
******

.. code-block:: shell

    $ twine upload dist/XComment-x.y.z.tar.gz

Tips
----

If you're not using [PyCharm](https://www.jetbrains.com/pycharm/) yet, make sure to at least consider this as an option. 
Also check out [JetBrains Toolbox](https://www.jetbrains.com/toolbox/), a single tool to rule them all (the JetBrains products). 
To stay up-to-date, follow [PyCharm Blog](https://blog.jetbrains.com/pycharm/). 
