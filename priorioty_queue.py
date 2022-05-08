#!/usr/bin/env python3
#
# Simple priority queue. 
# Assume an incoming stream of dictionaries containing two keys; command to be executed and priority. 
# Priority is an integer value [0, 10], where work items of the same priority are processed in the order they are received. 
#
# © 2022 Nicolas Houle <nickhoule@gmail.com>
#

import unittest


class PriorityQueue:

    def __init__(self) -> None:
        self.data = list()

    def empty(self) -> bool:
        return not len(self.data)

    def put(self, item: dict) -> None:
        self.data.append(item)

    def get(self) -> str:
        # sort by priority, keep the same order if priority is same
        sorted_list = sorted(self.data, key=lambda x: x["priority"])

        # take out first element of the list
        item = sorted_list.pop(0)

        # store list without the element taken
        self.data = sorted_list

        return item["command"]

    def add_items(self, items: list):
        # append items to stored items
        for item in items:
            self.put(item)

    def execute_all(self, **kwargs: dict[str, int]):

        while not self.empty():
            command = self.get()
            yield eval(command, kwargs)
        

class Testing(unittest.TestCase):
    _items = [
        dict(priority=5, command="x * y"),
        dict(priority=7, command="foo"),
        dict(priority=3, command="4 * x"),
        dict(priority=1, command="4 * y"),
        dict(priority=7, command="bar"),
        dict(priority=9, command="y * 5"),
        dict(priority=3, command="4 * 5"),
    ]


    def setUp(self) -> None:
        self.priority_queue = PriorityQueue()
        self.items = self._items.copy()
        self.mapping = dict(foo="foo", bar="bar", x=2, y=3)

    def test_order_is_good(self) -> None:
        """ Test PriorityQueue with various priority dicts """
        self.priority_queue.add_items(self._items)
        expected = [12, 8, 20, 6, "foo", "bar", 15]
        result = list(self.priority_queue.execute_all(**self.mapping))
        self.assertEqual(result, expected)

    def test_order_is_bad(self) -> None:
        """ Test PriorityQueue with various priority dicts and expected to fail """
        self.items.reverse()
        self.priority_queue.add_items(self.items)
        expected = [12, 8, 20, 6,  "foo", "bar", 15]
        result = list(self.priority_queue.execute_all(**self.mapping))
        self.assertNotEqual(result, expected)

    def test_priority_all_same(self) -> None:
        """ Test PriorityQueue with all same priority value """
        for item in self.items:
            item["priority"] = 5
        self.priority_queue.add_items(self._items)
        expected = [6, "foo", 8, 12, "bar", 15, 20]
        result = list(self.priority_queue.execute_all(**self.mapping))
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
