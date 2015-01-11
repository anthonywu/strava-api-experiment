import functools
import json
import pygments
import pygments.lexer as lexer

def prettify_dict(d):
  return json.dumps(d)

def print_dict(d):
  print(prettify_dict(d))
