#!/usr/bin/env python

from fitparse import FitFile
import IPython

def main():
    import sys
    f = FitFile(sys.argv[1])
    for msg in f.get_messages('record'):
        print(msg.get_values().keys())
        IPython.embed()


if __name__ == '__main__':
    main()
