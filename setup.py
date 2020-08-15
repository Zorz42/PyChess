from setuptools import setup


setup(
    name='PyChess',
    description='Chess game and AI using PyGame',

    packages=['pychess'],
    entry_points={'console_scripts': ['pychess=pychess.__main__:main']},

    install_requires=[
        'pygame>=2.0.0<3.0.0'
    ],
)
