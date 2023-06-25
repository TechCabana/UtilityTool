import os

def get_filepaths(directory):
    """
    This function will generate the file names in a directory 
    tree by walking the tree either top-down or bottom-up. For each 
    directory in the tree rooted at directory top (including top itself), 
    it yields a 3-tuple (dirpath, dirnames, filenames).
    """
    file_paths = []  # List which will store all of the full filepaths.

    # Walk the tree.
    for root, directories, files in os.walk(directory):
        for filename in files:
            # Join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)  # Add it to the list.
         

    return file_paths  # Self-explanatory.

# Run the above function and store its results in a variable. All values get stored in variable full_file_path   
full_file_paths = get_filepaths("/Users/ankhitsharma/Downloads/")


def get_filenames(directory):
    """
    This function will generate the file names in a directory 
    tree by walking the tree either top-down or bottom-up. For each 
    directory in the tree rooted at directory top (including top itself), 
    it yields a 3-tuple (dirpath, dirnames, filenames).
    """
    file_names = []  # List which will store all of the full filepaths.

    # Walk the tree.
    for root, directories, files in os.walk(directory):
        for filename in files:
            # Join the two strings in order to form the full filepath.
            file = os.path.basename(filename)
            file_names.append(file)  # Add it to the list.
         
        
    return file_names  # Self-explanatory.

# Run the above function and store its results in a variable. All values get stored in variable full_file_path   
full_file_names = get_filenames("/Users/ankhitsharma/Downloads/250Prachi")


#Write to CSV
with open('/Users/ankhitsharma/Desktop/test.csv', 'w') as f:
    for row in full_file_names:
        print(row)
        f.write("%s\n" % str(row))
