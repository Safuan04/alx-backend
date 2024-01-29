#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
import math
from typing import List, Dict


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """Returns a dictionay of dataset information based on
        a specified index and page_size"""
        assert index <= len(self.indexed_dataset())

        index_dict = {}
        data_list = []
        indexes = []
        add_index = 0

        for key in self.indexed_dataset().keys():
            if index <= key < index + page_size:
                indexes.append(key)

        if len(indexes) < page_size:
            add_index = index + page_size
            while len(indexes) < page_size:
                indexes.append(add_index)
                add_index += 1

        for indexx in indexes:
            data_list.append(self.indexed_dataset()[indexx])

        index_dict['index'] = index
        index_dict['data'] = data_list
        index_dict['page_size'] = page_size
        index_dict['next_index'] = indexes[-1] + 1

        return index_dict
