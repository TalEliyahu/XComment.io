# comments_remover



## Getting Up-and-Running Locally


### Prerequisites

Tested with the following configuration:

* Ubuntu 17.04;
* PyCharm 2017.2;
* Python 3.6.x.

*Note: the below occurences of *`./`* refer to the project root unless explicitly stated otherwise*. 


### Setting Things Up on Ubuntu

1. Create a Python 3.6 virtualenv.
    1. Install:
        1. [virtualenv](https://virtualenv.pypa.io/en/stable/);
        1. (optionally) [pyenv](https://github.com/pyenv/pyenv);
        1. (optionally) [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/stable/);
        1. (optionally) [pyenv-virtualenvwrapper](https://github.com/pyenv/pyenv-virtualenvwrapper).
1. Enter the created virtualenv.
1. Install dependencies:
    ```shell
    pip install -r ./requirements.txt
    ```
    
You should be good to go now.

If you're not using PyCharm yet, make sure to at least consider this as an option.

* For full-fledged Django support, opt out for [PyCharm Professional](https://www.jetbrains.com/pycharm/).
* Also check out [JetBrains Toolbox](https://www.jetbrains.com/toolbox/), a single tool to rule them all (the JetBrains products).
* To stay up-to-date, follow [PyCharm Blog](https://blog.jetbrains.com/pycharm/). 

We also suggest you to try out [IPython](https://ipython.org/) interactive shell to speed up development.


### Running Tests

Simply
```shell
pytest ./
```

To also see coverage report,
```shell
pytest --cov ./
```
