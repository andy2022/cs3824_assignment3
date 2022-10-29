## Main code for running program
from parsing import *
from annotation import *
import networkx as nx

g = nx.DiGraph()
read_go_structure(g, "go.obo.txt")
human_annotations = read_go_annotations("goa_human.gaf")

human_annotations_transferred = create_annotations(g, human_annotations)
specific_GO_terms(g, human_annotations_transferred)