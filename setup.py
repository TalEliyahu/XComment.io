import os
from setuptools import find_packages, setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="XComment",
    version="0.0.1",
    author="Singapore-Tech-Entrepreneurs",
    author_email="tal@ste.sg",
    description="A script to remove comments from code.",
    keywords="code comments removal xcomment",
    url="http://packages.python.org/XComment",
    packages=find_packages(),
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
    ],
    scripts=[
        'comments_remover'
    ],
    install_requires=[
        'Django==1.11.7',
        'pyunpack==0.1.2',
        'gunicorn==19.7.1',
        'whitenoise==3.3.1'
    ]
)
