import sys

from . import hello


def main():
    name = sys.argv[1] if len(sys.argv) > 1 else 'world'
    hello(name)


if __name__ == '__main__':
    main()
