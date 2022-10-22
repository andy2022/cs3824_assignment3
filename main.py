## Main code for running program
from parsing import read_go_structure
import networkx as nx

g = nx.DiGraph()
read_go_structure(g)