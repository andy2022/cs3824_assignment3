## Functions related to annotation computations
import networkx as nx

def ancestors_set(graph, term):
    '''
    Function for computing set of ancestors for a GO term (node in graph). Returns
    new DiGraph consisting only of ancestor nodes
    graph: Directed Graph
    term: Node to find ancestors for
    '''
    ancestors = nx.ancestors(graph, term)

    # Use subgraph to generate graph of ancestors
    a_graph = graph.subgraph(ancestors)

    # Return ancestors graph
    return a_graph

def create_annotations(graph, interactions):
    '''
    Function for creating annotations between every node and every one of its ancestors
    with evidence codes associated with that pair. Annotations stored in similar structure
    as human_interactions object.
    graph: Directed Graph
    interactions: human_interactions object
    '''

    human_annotations_transferred = {} # Initialize record of annotations
    # Iterate through every node
    for term in graph.nodes():

        # If term does not exist in human_interactions, skip this iteration
        if term not in interactions: continue

        # Get list of genes and evidence codes for this node from human_interactions
        genes = interactions[term]["obj_id"]
        evs = interactions[term]["evidence_code"]

        ancestors = ancestors_set(graph, term) # Get ancestors graph

        # Iterate through each ancestor
        for a in ancestors.nodes():

            # If ancestor does not exist as key, make new structure
            if a not in human_annotations_transferred:
                # Add gene and evidence code lists of current term as first entries
                human_annotations_transferred[a] = {
                    "obj_id":genes, "evidence_code":evs}
            # Else, if current ancestor exists, extend w/ node lists
            else:
                human_annotations_transferred[a]["obj_id"].extend(genes)
                human_annotations_transferred[a]["evidence_code"].extend(evs)

    return human_annotations_transferred # Return new dict