# AUTOGENERATED! DO NOT EDIT! File to edit: ../01_case.ipynb.

# %% auto 0
__all__ = ['acronyms', 'px_labeler', 'replace_parentheses', 'snake2words', 'replace_acronyms', 'if_instance',
           'snake2words_replace_acronyms', 'snake2words_replace_acronyms_if_str', 'PxLabeler']

# %% ../01_case.ipynb 3
import re
import pandas as pd
from plotly import express
from fastcore.all import *
from .core import *
from functools import partial

# %% ../01_case.ipynb 5
def replace_parentheses(s):
    '''Replaces `__x__` by ` (x)` in string s.'''
    out = s.replace('__','_(', 1).replace('__',')', 1)
    if out == s: return out
    return replace_parentheses(out)

# %% ../01_case.ipynb 8
_par_re = re.compile(r'((?<=\()[A-Z])')

# %% ../01_case.ipynb 9
def snake2words(s):
    '''Return properly capitalized version of snake_case string `s`'''
    return re.sub(_par_re, lambda x: x.group(0).lower(), ' '.join(replace_parentheses(s).title().split('_')))

# %% ../01_case.ipynb 11
acronyms = ['MAE', 'RMSE', 'R2']

# %% ../01_case.ipynb 12
def replace_acronyms(s):
    '''Replaces acronyms in s by its capitalized version.'''
    if is_listy(s): return [replace_acronyms(o) for o in s]
    for o in acronyms:
        s = re.sub(rf'\b({o.lower()}|{o.capitalize()}|{o.title()})\b', o, s)
    return s

# %% ../01_case.ipynb 19
def if_instance(fun, t, x): return fun(x) if isinstance(x, t) else x

# %% ../01_case.ipynb 20
def snake2words_replace_acronyms(x): return  replace_acronyms(snake2words(x))

# %% ../01_case.ipynb 21
def snake2words_replace_acronyms_if_str(x): return if_instance(snake2words_replace_acronyms, str, x)

# %% ../01_case.ipynb 22
@patch
def rename2words(self:pd.DataFrame, rename_index_name=True, rename_column_name=True): 
    '''Renames columns in snake_case to Words.'''
    out = self.renamec(snake2words_replace_acronyms_if_str)
    if rename_column_name:
        out.columns.name = snake2words_replace_acronyms_if_str(out.columns.name)
    if rename_index_name:
        out.index.name = snake2words_replace_acronyms_if_str(out.index.name)
    return out

# %% ../01_case.ipynb 25
class PxLabeler:
    '''Behaves like a dictionary from snake_case --> Snake Case.'''
    def __init__(self): self.default_dict = {}
    def __setitem__(self, key, value):
        if isinstance(value, str): self.default_dict[key] = self[value]
        else: self.default_dict[key] = value
    def __getitem__(self, item): 
        if item in self.default_dict: return self.default_dict[item]
        if isinstance(item, str): return replace_acronyms(snake2words(item))
        return item
    def __str__(self): return 'snake_case2Words'
    def copy(self): return self
    def get(self, item, default=None):
        if isinstance(item, str): return self[item]
        else: return default
    __repr__ = __str__
px_labeler = PxLabeler()
