import unittest

from xbot.commands.commands import ls
from xbot.commands.util_functions import list_by_item_state, request_data


class TestListNodes(unittest.TestCase):
    def test_list_all_nodes_not_empty(self):
        """Test that the list of nodes is not empty."""
        base_url = f"http://localhost:3000/nodes"
        response = request_data(base_url)
        node_list = response.json()
        self.assertTrue(len(node_list) > 0)

    def test_list_all_nodes_not_none(self):
        """ Test that list of nodes is not None. """
        base_url = f"http://localhost:3000/nodes"
        response = request_data(base_url)
        node_list = response.json()
        self.assertIsNotNone(node_list)

    def test_list_all_nodes_is_list(self):
        """ Test that list of nodes is a list. """
        base_url = f"http://localhost:3000/nodes"
        response = request_data(base_url)
        node_list = response.json()
        self.assertIsInstance(node_list, list)

    def test_list_all_nodes_is_dict(self):
        """ Test that list of nodes is a dict. """
        base_url = f"http://localhost:3000/nodes"
        response = request_data(base_url)
        node_list = response.json()
        self.assertIsInstance(node_list[0], dict)

    def test_list_all_nodes_has_name(self):
        """ Test that list of nodes has a name. """
        base_url = f"http://localhost:3000/nodes"
        response = request_data(base_url)
        node_list = response.json()
        self.assertTrue("name" in node_list[0])

    def test_list_all_nodes_has_id(self):
        """ Test that list of nodes has an id. """
        base_url = f"http://localhost:3000/nodes"
        response = request_data(base_url)
        node_list = response.json()
        self.assertTrue("id" in node_list[0])

    def test_list_all_nodes_has_state(self):
        """ Test that list of nodes has a state. """
        base_url = f"http://localhost:3000/nodes"
        response = request_data(base_url)
        node_list = response.json()
        self.assertTrue("node_state" in node_list[0])

    def test_list_all_nodes_has_type(self):
        """ Test that list of nodes has a type. """
        base_url = f"http://localhost:3000/nodes"
        response = request_data(base_url)
        node_list = response.json()
        self.assertTrue("node_type" in node_list[0])

    def test_list_all_nodes_has_date_created(self):
        """ Test that list of nodes has an ip. """
        base_url = f"http://localhost:3000/nodes"
        response = request_data(base_url)
        node_list = response.json()
        self.assertTrue("date_created" in node_list[0])

    def test_total_nodes_is_an_integer(self):
        """Test that the value returned by the total command is an integer."""
        base_url = f"http://localhost:3000/nodes/total"
        response = request_data(base_url)
        total_nodes = response.json()
        self.assertIsInstance(len(total_nodes), int)


if __name__ == "__main__":
    unittest.main()
