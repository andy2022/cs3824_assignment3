## Functions for parsing data files

def read_go_structure():
    '''
    Function for reading GO file in OBO format.
    '''

    with open("go.obo.txt", "r") as f:

        # Skip first section of text - 28 lines + 1 blank
        for i in range(29):
            f.readline()

        # Main loop for reading each term
        while True:
            assert(f.readline() == "[Term]\n")

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

            # Record


        pass
    pass