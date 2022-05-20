""" Python script to validate data

Run as:

    python3 scripts/validata_data.py data
"""

import os
import sys
import hashlib
import glob


def file_hash(filename):
    """ Get byte contents of file `filename`, return SHA1 hash

    Parameters
    ----------
    filename : str
        Name of file to read

    Returns
    -------
    hash : str
        SHA1 hexadecimal hash string for contents of `filename`.
    """
    with open(filename, 'rb') as fobj:
        file_bytes = fobj.read()
    return hashlib.sha1(file_bytes).hexdigest()


def validate_data(data_directory):
    """ Read ``hash_list.txt`` file in ``data_directory``, check hashes
    
    An example file ``data_hashes.txt`` is found in the baseline version
    of the repository template for your reference.

    Parameters
    ----------
    data_directory : str
        Directory containing data and ``hash_list.txt`` file.

    Returns
    -------
    None

    Raises
    ------
    ValueError:
        If hash value for any file is different from hash value recorded in
        ``hash_list.txt`` file.
    """
    # Read lines from ``hash_list.txt`` file.
    hash_fname = glob.glob(os.path.join(data_directory, "group-0?", "hash_list.txt"), recursive=True)
    for hash_file in hash_fname:  
        with open(hash_file, 'rt') as f:
            hash_list = f.read().split()

        # Split into SHA1 hash and filename
        hashes = hash_list[0::2]
        fnames = hash_list[1::2]
        
        for i in range(len(fnames)):
            # Calculate actual hash for given filename.
            filename = os.path.join(data_directory, fnames[i])
            actual_hash = file_hash(filename)

            # If hash for filename is not the same as the one in the file, raise
            # ValueError
            if actual_hash != hashes[i]:
                raise ValueError(f'hash value for {fnames[i]} does not match hash value recorded in {hash_file}.')


def main():
    # This function (main) called when this file run as a script.
    #
    # Get the data directory from the command line arguments
    if len(sys.argv) < 2:
        raise RuntimeError("Please give data directory on "
                           "command line")
    data_directory = sys.argv[1]
    # Call function to validate data in data directory
    validate_data(data_directory)


if __name__ == '__main__':
    # Python is running this file as a script, not importing it.
    main()
