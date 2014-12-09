from into.convert import convert, list_to_numpy, iterator_to_numpy_chunks
from into.chunks import chunks
from datashape import discover
from toolz import first
from collections import Iterator
import datashape
import numpy as np
import pandas as pd

def test_basic():
    assert convert(tuple, [1, 2, 3]) == (1, 2, 3)


def test_array_to_set():
    assert convert(set, np.array([1, 2, 3])) == set([1, 2, 3])


def eq(a, b):
    c = a == b
    if isinstance(c, (np.ndarray, pd.Series)):
        c = c.all()
    return c


def test_set_to_Series():
    assert eq(convert(pd.Series, set([1, 2, 3])),
              pd.Series([1, 2, 3]))


def test_Series_to_set():
    assert convert(set, pd.Series([1, 2, 3])) == set([1, 2, 3])


def test_dataframe_and_series():
    s = pd.Series([1, 2, 3], name='foo')
    df = convert(pd.DataFrame, s)
    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ['foo']

    s2 = convert(pd.Series, df)
    assert isinstance(s2, pd.Series)

    assert s2.name == 'foo'


def test_iterator_and_numpy_chunks():
    c = iterator_to_numpy_chunks([1, 2, 3], chunksize=2)
    assert isinstance(c, chunks(np.ndarray))
    assert isinstance(first(c), np.ndarray)

    L = convert(list, c)
    assert L == [1, 2, 3]


def test_list_to_numpy():
    ds = datashape.dshape('3 * int32')
    x = list_to_numpy([1, 2, 3], dshape=ds)
    assert (x == [1, 2, 3]).all()
    assert isinstance(x, np.ndarray)


    ds = datashape.dshape('3 * ?int32')
    x = list_to_numpy([1, None, 3], dshape=ds)
    assert np.isnan(x[1])