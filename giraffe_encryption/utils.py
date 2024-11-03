"""Shared functions for encrypting and decrypting the Giraffe"""
from typing import List

def _count_white(substring: str, output: List[int]) -> List[int]:
    stripped = substring.lstrip()
    if stripped == substring:
        output.append(0)
    else:
        output.append(substring.find(stripped))
    
    if stripped == "":
        return output
    else:
        return _count_chars(stripped, output)

def _count_chars(substring: str, output: List[int]) -> List[int]:
    ind = substring.find(" ")
    if ind == -1:
        output.append(len(substring))
        return output
    else:
        output.append(ind)
        return _count_white(substring[ind:], output)
    
def describe_whitespace(line: str) -> List[int]:
    output = []
    return _count_white(line, output)  

def string_sub(string, pos:int, char:str) -> str:
    return string[: pos] + char + string[pos + 1:-1] + " \n"