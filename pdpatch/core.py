# AUTOGENERATED! DO NOT EDIT! File to edit: 00_core.ipynb (unless otherwise specified).

__all__ = ['dummydf', 'l', 'minmax', 'Walker', 'Less']

# Cell
from functools import partial
from itertools import chain
import math

from fastcore.all import *
import pandas as pd
import ipywidgets as widgets
from IPython.display import display

# Cell
def dummydf(): return pd.DataFrame({'col_1': range(100, 105), 'col_2': ['a','b','c','d','e']})

# Cell
@patch
def repetitions(self:pd.DataFrame, col): return self.groupby(col).size()

# Cell
add_docs(pd.DataFrame,
         repetitions='Counts the number of repetitions for each element.',
         ffill=pd.core.generic.NDFrame.ffill.__doc__,
         bfill=pd.core.generic.NDFrame.bfill.__doc__,
         clip=pd.core.generic.NDFrame.clip.__doc__,
         interpolate=pd.core.generic.NDFrame.interpolate.__doc__,
         where=pd.core.generic.NDFrame.where.__doc__,
         mask=pd.core.generic.NDFrame.mask.__doc__)

# Cell
@patch
def repetition_counts(self:pd.DataFrame, col): return self.repetitions(col).value_counts()

# Cell
add_docs(pd.DataFrame,repetition_counts='Counts the number of groups with the same number of repetitions.')

# Cell
@patch
def single_events(self:pd.DataFrame, col): return self.set_index(col).loc[self.repetitions(col)==1].reset_index()

# Cell
add_docs(pd.DataFrame, single_events='Returns rows that appear only once.')

# Cell
@patch
@delegates(pd.crosstab)
def crosstab(self:pd.DataFrame, index, column, **kwargs): return pd.crosstab(self[index], self[column], **kwargs)

# Cell
add_docs(pd.DataFrame, crosstab=pd.crosstab.__doc__)

# Cell
@patch
def len(self:pd.DataFrame): return len(self)

# Cell
add_docs(pd.DataFrame, len=len.__doc__)

# Cell
@patch
def len(self:pd.Series): return len(self)

# Cell
@patch(as_prop=True)
def l(self:pd.Index): return L(self, use_list=True)

# Cell
@patch(as_prop=True)
def minmax(self:pd.Series): return (self.min(), self.max())

# Cell
@patch
def page(self:pd.DataFrame, page, page_size=5): return self.head(page*page_size).tail(page_size)

# Cell
add_docs(pd.DataFrame, page='Shows rows from page*page_size to (page+1)*page_size')

# Cell
@patch
def page(self:pd.Series, page, page_size=5): return self.head(page*page_size).tail(page_size)

# Cell
add_docs(pd.Series,
         page='Shows rows from page*page_size to (page+1)*page_size',
         ffill=pd.core.generic.NDFrame.ffill.__doc__,
         bfill=pd.core.generic.NDFrame.bfill.__doc__,
         clip=pd.core.generic.NDFrame.clip.__doc__,
         interpolate=pd.core.generic.NDFrame.interpolate.__doc__,
         where=pd.core.generic.NDFrame.where.__doc__,
         mask=pd.core.generic.NDFrame.mask.__doc__,
         len=len.__doc__)

# Cell
@patch
def renamec(self:pd.DataFrame, d, *args):
    if args:
        if isinstance(d, dict): d = chain(*d.items())
        d = dict(chunked(listify(d) + listify(args), 2))
    return self.rename(columns=d)

# Cell
add_docs(pd.DataFrame, renamec='Renames column names.')

# Cell
@patch
def notin(self:pd.Series, values): return ~self.isin(values)

# Cell
add_docs(pd.Series, notin='Whether elements in Series are not contained in `values`.')

# Cell
@patch
def mapk(self:pd.Series, fun, **kwargs): return self.map(partial(fun, **kwargs))

# Cell
add_docs(pd.Series, mapk='Like map but passes kwargs to function.')

# Cell
@patch
def title(self:pd.DataFrame, title):
    '''Displays DataFrame with a title.'''
    out = widgets.Output()
    with out: display(self)
    layout = widgets.Layout(align_items='center')
    return widgets.VBox([widgets.Label(title, layout=layout), out])

# Cell
class Walker:
    def __init__(self, val=0, min_val=None, max_val=None): store_attr()
    def _next(self, *args, val=1, **kwargs):
        self.val += val
        if self.max_val: self.val = min(self.max_val, self.val)
    def _prev(self, *args, val=1, **kwargs):
        self.val -= val
        if self.min_val: self.val = max(self.min_val, self.val)
    def _head(self):
        self.val = 0
        if self.min_val: self.val = max(self.min_val, self.val)

# Cell
class Less:
    def __init__(self, df, page_size=5, page=1, where=None):
        store_attr()
        if not where is None:
            page = math.floor(L(range_of(df))[where][0]/page_size+1)

        self.out = widgets.Output(wait=True)
        self.out_df = widgets.Output(wait=True)
        self.out_df.append_display_data(self.df.page(page, page_size=self.page_size))

        self.n_pages = len(df)//self.page_size+1
        self.page = Walker(val=page, min_val=1, max_val=self.n_pages)

        self.next = widgets.Button(description='next')
        self.next.on_click(self.page._next)
        self.next.on_click(self.refresh)

        self.prev = widgets.Button(description='prev')
        self.prev.on_click(self.page._prev)
        self.prev.on_click(self.refresh)

        layout = widgets.Layout(width='100%', display='flex', align_items='center')
        self.out_label = widgets.Output(wait=True)
        with self.out_label: display(widgets.Label(f"page {self.page.val} of {self.n_pages}"))
        self.box = widgets.VBox([widgets.HBox([self.prev, self.next, self.out_label]), self.out_df])
        with self.out:
            display(self.box)

    def refresh(self, event):
        self.out_df.clear_output()
        with self.out_df: display(self.df.page(self.page.val, page_size=self.page_size))
        self.out_label.clear_output()
        with self.out_label: display(widgets.Label(f"page {self.page.val} of {self.n_pages}"))

# Cell
@patch
def less(self:pd.DataFrame, page_size=5, page=1, where=None):
    return Less(self, page_size=page_size, page=page, where=where).out

# Cell
@patch
def to_percent(self:pd.DataFrame, exclude=[]):
    cols = self.dtypes[self.dtypes=='float'].index
    cols = [c for c in cols if c not in exclude]
    return self.style.format({c: '{:.1%}'.format for c in cols})

# Cell
add_docs(pd.DataFrame,
         less='Displays one page of the DataFrame and buttons to move forward and backward.',
         to_percent='Formats float columns to percentage.')

# Cell
@patch
def less(self:pd.Series, page_size=5, where=None): return Less(self, page_size=page_size, where=where).out

# Cell
add_docs(pd.Series,
         less='Displays one page of the Series and buttons to move forward and backward.',
         )

# Cell
@patch
def c2back(self:pd.DataFrame, cols2back):
    if not is_listy(cols2back): cols2back = [cols2back]
    cols = [c for c in self.columns if c not in cols2back]+cols2back
    return self[cols]

# Cell
@patch
def c2front(self:pd.DataFrame, cols2front):
    if not is_listy(cols2front): cols2front = [cols2front]
    cols = cols2front + [c for c in self.columns if c not in cols2front]
    return self[cols]

# Cell
add_docs(pd.DataFrame,
         c2back="Move columns to back",
         c2front="Move columns to front")

# Cell
@patch
def reorderc(self:pd.DataFrame, to_front=[], to_back=[]):
    '''Reorder DataFrame columns.'''
    return self.c2front(to_front).c2back(to_back)