#!/usr/bin/python3
'''This module has one class, Scan,
    which scans and switches special characters'''

import re
import hashlib


class Scan:

    def switch_emphasis(self, _str: str) -> str:
        '''
        switch dunder & <em> .
        '''
        return re.sub(r"\_\_([\<\>\/\*\w\s]+)\_\_",
                      r"<em>\1</em>", _str)

    def switch_c(self, _str: str) -> str:
        '''delete c's'''
        return re.sub(r"\(\([\w\s]+\)\)",
                      lambda x: self._delete_paren(
                          self._delete_c(x.group())), _str)

    def switch_bold(self, _str: str) -> str:
        '''
        switch double asterisk & <bold> .
        '''
        return re.sub(r"\*\*([\<\>\/\*\w\s]+)\*\*",
                      r"<b>\1</b>", _str)

    def switch_md5(self, _str: str) -> str:
        '''
        switch double bracket & md5 encryption.
        '''
        return re.sub(r"\[\[([\/\w\s]+)\]\]",
                      lambda f: self._encrypt_md5(f.group()), _str)

    def _delete_c(self, _str: str) -> str:
        '''
        deletes all c's from a string.
        '''
        return "".join(c for c in _str if c not in {"c", "C"})

    def _encrypt_md5(self, _str: str) -> str:
        '''
        Encrypts a string& md5.
        '''
        return hashlib.md5(self._delete_bracket(_str).encode()).hexdigest()

    def _delete_paren(self, _str: str) -> str:
        '''
        deletes all parentheses from a string.
        '''
        return "".join(c for c in _str if c not in {"(", ")"})

    def _delete_bracket(self, _str: str) -> str:
        '''
        deletes all brackets from a string.
        '''
        return "".join(c for c in _str if c not in {"[", "]"})

