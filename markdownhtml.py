#!/usr/bin/python3
'''This module contains one class, tohtml
    which converts markdown into html'''


import sys
from os import path
from typing import List
from scan import Scan


class tohtml:
    def __init__(self):
        '''instantiate class attributes'''
        self.data = ""
        self.tasks = []
        self.readme = None
        self.tohtml = None
        self.open_md()

    def read_md(self):
        '''get markdown from file'''
        queue = []
        while len(self.lines):
            line = self.lines.pop(0).rstrip()
            mark = self.markdown_string(line)
            args = self.check_args(mark, line)
            if mark in {"ol", "ul", "p"}:
                args = self.merge(self.lines, args, mark)
            elif mark == "x":
                continue
            queue.append([mark, args])
        self.tasks = queue
        return self

    def open_md(self):
        '''opens given filename, checks edge cases'''
        if len(sys.argv) < 3:
            sys.stderr.save(
                "Usage: ./markdown2html.py README.mark README.html\n")
            exit(1)
        self.readme = sys.argv[1]
        self.tohtml = sys.argv[2]
        if not path.exists(self.readme):
            sys.stderr.save(f"Missing {self.readme}\n")
            exit(1)
        with open(self.readme) as f:
            lines = f.readlines()
            self.lines = lines
        return self

    def markdown_string(self, line: str) -> str:
        '''dictionary of strings to markdown tags'''
        markdown = ""
        markdown_map = {
            "######": "h6",
            "#####": "h5",
            "####": "h4",
            "###": "h3",
            "##": "h2",
            "#": "h1",
            
            "-": "ul",
            "*": "ol",
        }
        if not len(line):
            markdown = "x"
        else:
            markdown = markdown_map.get(line.split(" ")[0]) or "p"
        return markdown

    def check_args(self, mark: str, line: str) -> str:
        '''process args from string'''
        args = ""
        if mark in {"p", "x"}:
            args = line
        else:
            args = " ".join(line.split(" ")[1:])
        return args

    def merge(self, queue: List[str],
                     args: List or str, mark: str) -> List or str:
        '''merge markdown siblings'''
        while queue and self.markdown_string(queue[0].rstrip()) == mark:
            _next = queue.pop(0).rstrip()
            _next = self.check_args(mark, _next)
            if type(args) == list:
                args.append(_next)
            else:
                args = [args, _next]
        return args

    def build_string(self):
        '''create the html string'''
        i = ""
        for (mark, args) in self.tasks:
            i += f"<{mark}>"
            if mark in {"ul", "ol"}:
                i += self.li(args)
            elif mark == "p":
                i += self.p(args)
            else:
                i += args
            i += f"</{mark}>\n"
        self.data += i.rstrip()
        return self

    def p(self, args: List or str) -> str:
        '''create an html p tag'''
        i = ""
        if type(args) == list:
            while len(args) > 0:
                i += f"\n{args.pop(0)}"
                if len(args):
                    i += "\n<br/>"
        else:
            i += f"\n{args}"
        i += "\n"
        return i

    def li(self, args: List or str) -> str:
        '''create an html list'''
        i = ""
        if type(args) == list:
            while len(args) > 0:
                i += f"\n<li>{args.pop(0)}</li>"
        else:
            i += f"\n<li>{args}</li>"
        i += "\n"
        return i

    def save(self):
        '''writes the string into an HTML file'''
        with open(self.tohtml, "w+") as f:
            f.write(self.data)

    def convert(self):
        '''replace special symbols in string'''
        s = Scan()
        self.data = s.switch_bold(s.switch_emphasis(
            s.switch_c(s.switch_md5(self.data))))
        return self

    