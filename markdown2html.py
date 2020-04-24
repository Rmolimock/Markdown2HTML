#!/usr/bin/python3

'''
Convert markdown code into HTML
'''

from markdownhtml import tohtml

if __name__ == '__main__':

    tohtml = tohtml()
    tohtml.read_md().build_string().convert().save()
    exit(0)