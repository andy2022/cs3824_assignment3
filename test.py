## Code for testing function implementations
import unittest
import networkx as nx
from parsing import *
from annotation import *

class tests(unittest.TestCase):

    def setUp(self):
        pass

    def test_go_structure(self):
        '''
        Test case for parsing GO OBO file and creating corresponding graph. Reads
        smaller version of OBO file.
        '''
        g = nx.DiGraph()
        read_go_structure(g, "go.obo_test.txt")

        self.assertEqual(len(g.nodes), 5) # Should only add 5 nodes
        self.assertEqual(g.nodes["GO:1"]["name"], "mitochondrion inheritance")
        self.assertEqual(g.number_of_edges(), 4) # Check for 4 edges

    def test_go_annotations(self):
        '''
        Test case for annotations parsing function.
        '''
        #ret = read_go_annotations("goa_human.gaf")
        ret = read_go_annotations("goa_test.txt")

        self.assertEqual(len(ret), 6)

    def test_get_ancestors(self):
        '''
        Test case for getting ancestors for a node.
        '''
        g = nx.DiGraph()
        read_go_structure(g, "go.obo_test.txt")
        ancestors = ancestors_set(g, "GO:2")
        self.assertEqual(ancestors.number_of_nodes(), 3)
        self.assertEqual(ancestors.number_of_edges(), 2)

        # Ancestors of node with no parents
        ancestors = ancestors_set(g, "GO:1")
        self.assertEqual(ancestors.number_of_nodes(), 0)
        self.assertEqual(ancestors.number_of_edges(), 0)

unittest.main()