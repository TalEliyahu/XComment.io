# XComment


## Table of Contents

* [XComment](#xcomment)
  * [Table of Contents](#table-of-contents)
  * [Installation<a name="user-content-installation"></a>](#installation)
  * [Usage<a name="user-content-usage"></a>](#usage)
     * [Processing files](#processing-files)
     * [Processing directories](#processing-directories)
     * [Archives](#archives)
        * [Logging](#logging)
     * [Get supported language list](#get-supported-language-list)
     * [To see full CLI specification, run](#to-see-full-cli-specification-run)
  * [Development<a name="user-content-development"></a>](#development)
     * [Getting Up-and-Running Locally<a name="user-content-getting-up-and-running-locally"></a>](#getting-up-and-running-locally)
        * [Setting Things Up on Ubuntu<a name="user-content-setting-things-up-on-ubuntu"></a>](#setting-things-up-on-ubuntu)
     * [Deployment](#deployment)
        * [Pip registry](#pip-registry)
           * [Install dependencies](#install-dependencies)
           * [Set pypi credentials](#set-pypi-credentials)
           * [Create distribution](#create-distribution)
           * [Upload](#upload)
  * [Tips<a name="user-content-tips"></a>](#tips)

## Installation<a name="installation">

```shell
$ pip install XComment
```

## Usage<a name="usage"></a>

Use the project's CLI to interact with the script.

### Processing files

Say, you are working with the file `./tests/sources/HTML/index.html`.

Precondition: virtualenv is activated (of course).

To remove comments (output code without comments to output file) invoke

```shell
$ comments_remover ./tests/sources/HTML/input.html HTML ./
```
This will take `./tests/sources/HTML/input.html`, designated as `HTML` file, and put the copy of the former (with HTML-specific comments removed, obviously) to `./` named `rc.input.html`. The latter is the name of the original file prefixed with `rc.` by default.

To highlight comments (outputs comments only to output file) invoke

```shell
$ comments_remover ./tests/sources/HTML/input.html HTML -p ./
```


### Processing directories

If on start been specified directory path, script will be processing directory recursively with all subdirs for sources by specified language.


### Archives

For processing archived sources use option -a

Examples:

```shell
$ # remove comments
$ comments_remover ./tmp/test.zip -a Python

$ # highlight comments
$ comments_remover ./tmp/test.zip -a -p Python
```

#### Logging

-l option enable logging (in stdout by default)

-f < path > specify path to log file

Example:

```shell
$ comments_remover ./tmp/test.py -l -f ./remove.log Python
```

### Get supported language list

For get list supported languages use -i option.
Result list will returned in json format


```shell
$ comments_remover -i

["PHP", "Python", "CSS", "HTML", "JavaScript", "ActionScript", "Ruby",
"Assembly", "AppleScript", "Bash", "CSharp", "VB", "XML", "SQL", "C"]

```

### To see full CLI specification, run


```shell
$ comments_remover
```


## Development<a name="development"></a>


### Getting Up-and-Running Locally<a name="getting-up-and-running-locally"></a>

Tested with the following configuration:

* Ubuntu 16.04 / 17
* Python 3.6.

*Note: the below occurences of `./` refer to the project root unless explicitly stated otherwise*.


#### Setting Things Up on Ubuntu<a name="setting-things-up-on-ubuntu"></a>

1. Enter the shell.
1. Install `pyenv` via [pyenv-installer](https://github.com/pyenv/pyenv-installer):
    ```shell
    $ curl -L https://raw.githubusercontent.com/pyenv/pyenv-installer/master/bin/pyenv-installer | bash
    ```
    ![Installing `pyenv` via [pyenv-installer](https://github.com/pyenv/pyenv-installer)](./docs/images/pyenv-installer.png)
1. Follow the instructions on how to initialize `pyenv` on shell startup, for instance:
    ```shell
    $ echo 'export PATH="/root/.pyenv/bin:$PATH"' >> ~/.bash_profile
    $ echo 'eval "$(pyenv init -)"' >> ~/.bash_profile
    $ echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bash_profile
    ```
    ![Initializing `pyenv` on shell startup](./docs/images/initialize-pyenv-with-shell.png)
1. Install Python 3.6.x via `pyenv`, say Python 3.6.2 (latest micro release versions are preferred):
    ```shell
    $ pyenv install 3.6.2
    ```
    ![Installing Python 3.6.2 via `pyenv`](./docs/images/pyenv-install-3-6-2.png)
1. Create a virtualenv for the project:
    ```shell
    $ pyenv virtualenv 3.6.2 comments_remover
    ```
    ![Creating a virtualenv for the project](./docs/images/pyenv-virtualenv-3.6.2-comments_remover.png)
1. Switch to whatever directory you wish the project to reside in, say `~`:
    ```shell
    $ cd ~
    ```
    ![Switching to `~`](./docs/images/cd-~.png)
1. Clone the project from GitHub:
    * either via SSH (the preferred way):
    ```shell
    $ git clone git@github.com:Singapore-Tech-Entrepreneurs/comments_remover.git
    ```
    ![Cloning the project from GitHub via SSH](./docs/images/git-clone-gitatgithub-com-singapore-tech-entrepreneurs-comments-remover-git.png)
    * or via HTTPS:
    ```shell
    $ git clone https://github.com/Singapore-Tech-Entrepreneurs/comments_remover.git
    ```
    ![Cloning the project from GitHub via SHTTPSSH](./docs/images/git-clone-https-github-com-singapore-tech-entrepreneurs-comments-remover-git.png)
1. Switch to the project directory:
    ```shell
    $ cd comments_remover
    ```
    ![Switching to the project directory](./docs/images/cd-comments_remover.png)
1. Activate the virtualenv:
    ```shell
    $ pyenv activate comments_remover
    ```
    ![Activating the virtualenv](./docs/images/pyenv-activate-comments_remover.png)
1. Install project dependencies:
    ```shell
    pip install -U -r ./requirements.txt
    ```
    ![Installing project dependencies](./docs/images/pip-install-u-r-requirements-txt.png)
1. Install dependencies for testing:
    ```shell
    pip install -U -r ./requirements-test.txt
    ```
    ![Installing dependencies for testing](./docs/images/pip-install-u-r-requirements-test-txt.png)
1. (optional) Install [IPython](https://ipython.org/) interactive shell to speed up development:
    ```shell
    pip install ipython==6.1.0
    ```
    ![Installing [IPython](https://ipython.org/) interactive shell to speed up development](./docs/images/pip-install-ipython-6-1-0.png)
    
To run tests, simply

```shell
pytest ./
```
![Running tests](./docs/images/pytest.png)

To also see coverage report,

```shell
pytest --cov ./
```
![Running tests with coverage report](./docs/images/pytest-cov.png)

You should be good to go now.

### Deployment

#### Pip registry

##### Install dependencies
```shell
$ python install -r requirements-deploy.txt
```

##### Set pypi credentials
```shell
$ export TWINE_USERNAME=<pypi username>
$ export TWINE_PASSWORD=<pypi password>
```

##### Create distribution
```shell
$ python setup.py sdist bdist_wheel
```

##### Upload
```shell
$ twine upload dist/XComment-x.y.z.tar.gz
```



## Tips<a name="tips"></a>

If you're not using [PyCharm](https://www.jetbrains.com/pycharm/) yet, make sure to at least consider this as an option. 
Also check out [JetBrains Toolbox](https://www.jetbrains.com/toolbox/), a single tool to rule them all (the JetBrains products). 
To stay up-to-date, follow [PyCharm Blog](https://blog.jetbrains.com/pycharm/). 
