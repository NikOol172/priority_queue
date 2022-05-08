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
        """ Check if PriorityQueue is empty. """
        return not len(self.data)

    def put(self, item: dict) -> None:
        """ Append one item to stored items. """
        self.validate_item(item)

        # if there is not a priority, put lower priority in there.
        if not "priority" in item:
            item["priority"] = 10
        self.data.append(item)

    def get(self) -> str:
        """ Get first item by priority. """
        # sort by priority, keep the same order if priority is same.
        sorted_list = sorted(self.data, key=lambda x: x["priority"])

        # take out first element of the list.
        item = sorted_list.pop(0)

        # store list without the element taken.
        self.data = sorted_list

        return item["command"]

    def add_items(self, items: list) -> None:
        """ append items to stored items. """
        for item in items:
            self.put(item)

    def execute_all(self, **kwargs: dict[str, int]) -> str or int:
        """ Execute all commands in the PriorityQueue. """
        while not self.empty():
            command = self.get()
            yield eval(command, kwargs)

    @staticmethod
    def validate_item(item: dict) -> bool:
        """ Validate item """
        assert isinstance(item, dict), "item is not a dict."
        
        assert "command" in item, "Item dict does not have a command." 

        

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
        self.priority_queue.add_items(self.items)
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
        self.priority_queue.add_items(self.items)
        expected = [6, "foo", 8, 12, "bar", 15, 20]
        result = list(self.priority_queue.execute_all(**self.mapping))
        self.assertEqual(result, expected)

    def test_item_is_not_a_dict(self) -> None:
        self.items.append('test')
        with self.assertRaises(AssertionError):
            self.priority_queue.add_items(self.items)

    def test_item_do_no_have_a_command(self) -> None:
        self.items.append(dict())
        with self.assertRaises(AssertionError):
            self.priority_queue.add_items(self.items)

if __name__ == '__main__':
    # items = [
    #     dict(),
    #     dict(priority=5, command="x * y"),
    #     dict(priority=7, command="foo"),
    #     dict(priority=3, command="4 * x"),
    #     dict(priority=1, command="4 * y"),
    #     dict(priority=7, command="bar"),
    #     dict(priority=9, command="y * 5"),
    #     dict(priority=3, command="4 * 5"),
    # ]
    # mapping = dict(foo="foo", bar="bar", x=2, y=3)
    # priority_queue = PriorityQueue()
    # priority_queue.add_items(items)
    # list(priority_queue.execute_all(**mapping))


    unittest.main()
