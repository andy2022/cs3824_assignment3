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

def create_annotations(graph, annotations):
    '''
    Function for creating annotations between every node and every one of its ancestors
    with evidence codes associated with that pair. Annotations stored in similar structure
    as human_annotations object.
    graph: Directed Graph
    annotations: human_annotations object
    '''

    human_annotations_transferred = {} # Initialize record of annotations
    # Iterate through every node
    for term in graph.nodes():

        # If term does not exist in human_annotations, skip this iteration
        if term not in annotations: continue

        # Get list of genes and evidence codes for this node from human_annotations
        genes = annotations[term]["obj_id"]
        evs = annotations[term]["evidence_code"]

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

def specific_GO_terms(go_dag, human_annotations_transferred):
    '''
    Function for generating groups of GO terms. The process is described as:
    For each of 3 aspects in go_dag, find root term. Then, use transferred to count
    number of genes annotated to that term, which generates n_bp, n_mf, n_cc.
    For each aspect, use go_dag and transferred to find all GO terms that annotate
    n/100 and n/10 (2 thresholds) genes, which will be a subset S.
    Find most specific terms in S - include only descendent terms in S.
    go_dag: Main DiGraph
    '''

    # Helper function to get root term for each aspect
    bp_root = get_root(go_dag, "bp")
    mf_root = get_root(go_dag, "mf")
    cc_root = get_root(go_dag, "cc")

    # Count number of annotations (evidence codes) for each root term
    n_bp = len(human_annotations_transferred[bp_root]["evidence_code"])
    n_mf = len(human_annotations_transferred[mf_root]["evidence_code"])
    n_cc = len(human_annotations_transferred[cc_root]["evidence_code"])

    # Initialize sets
    bp_1 = []; bp_10 = []
    mf_1 = []; mf_10 = []
    cc_1 = []; cc_10 = []

    # For 1% threshold - find GO terms
    for node in go_dag.nodes():

        if go_dag.nodes[node]["namespace"] == "biological_process" and node in human_annotations_transferred:
            # If number of annotations in transferred >= n/100
            if len(human_annotations_transferred[node]["evidence_code"]) >= n_bp/100:
                bp_1.append(node)
            # If number of annotations in transferred >= n/10
            if len(human_annotations_transferred[node]["evidence_code"]) >= n_bp/10:
                bp_10.append(node)
        if go_dag.nodes[node]["namespace"] == "molecular_function" and node in human_annotations_transferred:
            if len(human_annotations_transferred[node]["evidence_code"]) >= n_mf/100:
                mf_1.append(node)
            if len(human_annotations_transferred[node]["evidence_code"]) >= n_mf/10:
                mf_10.append(node)
        if go_dag.nodes[node]["namespace"] == "cellular_component" and node in human_annotations_transferred:
            if len(human_annotations_transferred[node]["evidence_code"]) >= n_cc/100:
                cc_1.append(node)
            if len(human_annotations_transferred[node]["evidence_code"]) >= n_cc/10:
                cc_10.append(node)

    bp_1_specific = []; bp_10_specific = []
    mf_1_specific = []; mf_10_specific = []
    cc_1_specific = []; cc_10_specific = []

    # Get subset consisting of descendent nodes
    for each in bp_1:
        # If this node is a descendent, add to subset
        if len(nx.descendants(go_dag, each)) == 0:
            bp_1_specific.append(each)
    for each in bp_10:
        if len(nx.descendants(go_dag, each)) == 0:
            bp_10_specific.append(each)
    for each in mf_1:
        if len(nx.descendants(go_dag, each)) == 0:
            mf_1_specific.append(each)
    for each in mf_10:
        if len(nx.descendants(go_dag, each)) == 0:
            mf_10_specific.append(each)
    for each in cc_1:
        if len(nx.descendants(go_dag, each)) == 0:
            cc_1_specific.append(each)
    for each in cc_10:
        if len(nx.descendants(go_dag, each)) == 0:
            cc_10_specific.append(each)




def get_root(g, aspect):
    '''
    Helper function for finding root term for a given aspect. Since the root term
    has no ancestors, the function iterates through all nodes until one is found with
    no ancestors.
    g: DiGraph
    aspect: one of 3 options - bp, mf, cc
    '''
    root_name = "" # Initialize root name

    aspect_name = ""
    if aspect == "bp": aspect_name = "biological_process"
    elif aspect == "mf": aspect_name = "molecular_function"
    elif aspect == "cc": aspect_name = "cellular_component"
    else: raise Exception("Unknown aspect")

    for node in g.nodes():

        # If node matches aspect being evaluated
        if g.nodes[node]["namespace"] == aspect_name:

            # Generate ancestors
            ancestors = ancestors_set(g, node)
            # If ancestors subgraph empty, root found
            if ancestors.number_of_nodes() == 0:
                root_name = node
                break

    return root_name # Return name of root node for this aspect



