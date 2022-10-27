## Code for testing function implementations
import unittest
import networkx as nx
from parsing import *

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

        self.assertEquals(len(g.nodes), 4)
        self.assertEquals(g.nodes["GO:1"]["name"], "mitochondrion inheritance")
        self.assertEquals(g.number_of_edges(), 3) # Check for 3 edges

    def test_go_annotations(self):
        '''
        Test case for smaller annotations parsing function.
        '''
        ret = read_go_annotations_test("goa_test.txt")

unittest.main()