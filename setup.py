from setuptools import setup


try:
    from Cython.Build import cythonize
except ImportError:
    def cythonize(*args, **kwargs):
        return []


extensions = cythonize([
    'pychess/util.py',
    'pychess/pieces.py',
    'pychess/algorithm.py',
    'pychess/variables.py',
])

for extension in extensions:
    extension.optional = True


setup(
    name='PyChess',
    description='Chess game and AI using PyGame',

    packages=['pychess'],
    ext_modules=extensions,

    entry_points={'console_scripts': ['pychess=pychess.__main__:main']},

    setup_requires=[
        'cython>=3.0.0a,<4.0.0',
    ],
    install_requires=[
        'pygame>=2.0.0<3.0.0',
        'numpy>=1.0.0<2.0.0',
        'pyttsx3>=2.0.0<3.0.0'
    ],
)
