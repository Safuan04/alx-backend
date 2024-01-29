#!/usr/bin/env python3
"""Defining a function index_range"""
from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """returns a tuple of size two containing a start index
    and an end index corresponding to the range of indexes"""
    start_index = (page - 1) * page_size
    end_index = page * page_size
    return (start_index, end_index)
