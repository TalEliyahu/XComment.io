# comments_remover

Tested with the following configuration:

* Ubuntu 17;
* Python 3.6.

*Note: the below occurences of *`./`* refer to the project root unless explicitly stated otherwise*.



## Table of Contents

* [Getting Up-and-Running Locally](#getting-up-and-running-locally)
    * [Developing on Ubuntu](#developing-on-ubuntu)
    * [Usage](#usage)
* [Tips](#tips)

## Getting Up-and-Running Locally<a name="getting-up-and-running-locally"></a>


### Developing on Ubuntu<a name="developing-on-ubuntu"></a>

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


### Usage<a name="usage"></a>

Use the project's CLI to interact with the script.

Say, you want the `./tests/sources/HTML/index.html` file's comments removed. Given the project virtualenv is activated, from `./` invoke
```shell
$ python comments_remover.py ./tests/sources/HTML/input.html HTML ./
``` 

This will take `./tests/sources/HTML/input.html`, designated as `HTML` file, and put the copy of the former (with HTML-specific comments removed, obviously) to `./` named `rc.input.html`. The latter is the name of the original file prefixed with `rc.` by default. 

To see full CLI specification, run 
```shell
$ python comments_remover.py
```



## Tips<a name="tips"></a>

If you're not using [PyCharm](https://www.jetbrains.com/pycharm/) yet, make sure to at least consider this as an option. 
Also check out [JetBrains Toolbox](https://www.jetbrains.com/toolbox/), a single tool to rule them all (the JetBrains products). 
To stay up-to-date, follow [PyCharm Blog](https://blog.jetbrains.com/pycharm/). 
