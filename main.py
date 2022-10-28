## Main code for running program
from parsing import *
from annotation import *
import networkx as nx

g = nx.DiGraph()
read_go_structure(g, "go.obo.txt")
human_interactions = read_go_annotations("goa_human.gaf")

human_interactions_transferred = create_annotations(g, human_interactions)
print("S")