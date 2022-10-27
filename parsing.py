## Functions for parsing data files

def read_go_structure(go_dag, fname):
    '''
    Function for reading GO file in OBO format. For each term, the function creates nodes and adds
    them to an existing networkx DiGraph. All "is_a" and "part_of" relationships are recorded in
    lists, which are processed after all nodes have been added.
    go_dag: Networkx DiGraph
    fname: Input OBO file name
    '''
    isa_sources = [] # Empty list for "is_a" relationship sources
    isa_targets = [] # Empty list for "is_a" relationship targets
    partof_sources = [] # Empty list for "part_of" relationship sources
    partof_targets = [] # Empty list for "part_of" relationship targets

    with open(fname, "r") as f:

        # Skip first section of text - 28 lines + 1 blank
        for i in range(29):
            f.readline()

        # Main loop for reading each term - start by ensuring this is a new term block
        while f.readline() == "[Term]\n":

            # Pick up ID, name, and namespace line arrays
            id = f.readline().split()[1] # Save 2nd element
            name_line = f.readline().split()
            namespace_line = f.readline().split()

            # For name and name_space, if array length > 2, combine multiple words into single string
            name = ""
            if len(name_line) > 2:
                for i in range(1, len(name_line)-1):
                    name = name + name_line[i] + " " # Add space
                name = name + name_line[-1] # Add last word (no space at end)
            else:
                name = name_line[1] # Otherwise, save 2nd element
            namespace = ""
            if len(namespace_line) > 2:
                for i in range(1, len(namespace_line)-1):
                    namespace = namespace + namespace_line[i] + " " # Add space
                namespace = namespace + namespace_line[-1] # Add last word (no space at end)
            else:
                namespace = namespace_line[1] # Otherwise, save 2nd element

            # Add node to graph based on collected data
            go_dag.add_node(id, name=name, namespace=namespace)

            # Read until end of block, check for "is_a" and "part_of" relationships
            line = f.readline().split()
            while line != []:
                if line[0] == "is_a:":
                    # "is_a" relationship - add this node to sources, found node to targets
                    isa_sources.append(id)
                    isa_targets.append(line[1])
                    #go_dag.add_edge(id, line[1], relationship="is_a")
                elif line[1] == "part_of":
                    # "part_of" relationship - add this node to sources, found node to targets
                    partof_sources.append(id)
                    partof_targets.append(line[2])
                    #go_dag.add_edge(id, line[2], relationship="part_of")

                line = f.readline().split()

        # End while loop

    f.close() # Close file

    # Using collected "is_a" and "part_of" lists, generate edges
    for i in range(len(isa_sources)):
        go_dag.add_edge(isa_sources[i], isa_targets[i], relationship="is_a")
    for i in range(len(partof_sources)):
        go_dag.add_edge(partof_sources[i], partof_targets[i], relationship="part_of")