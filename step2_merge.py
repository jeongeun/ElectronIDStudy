import numpy as np
import sys

def generate_filenames(prefix, count):
    """
    Generates a list of filenames based on a prefix and a count.

    Parameters:
    - prefix (str): The prefix for each filename.
    - count (int): The number of files to generate.

    Returns:
    - list: A list of generated filenames.
    """
    return [f"./npy/{prefix}_{i}_new.npy" for i in range(count + 1)]
## Load each .npy file
#file_names = ['DY50_0_new.npy', 'DY50_1_new.npy', 'DY50_2_new.npy', 'DY50_3_new.npy', 'DY50_4_new.npy']    

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: script.py <prefix> <count>")
        sys.exit(1)

    prefix = sys.argv[1]
    count = int(sys.argv[2])

    file_names = generate_filenames(prefix, count)
    print(file_names)
    merged_dict = {}
    
    for file_name in file_names:
        loaded_dict = np.load(file_name, allow_pickle=True)[()]
        for key in loaded_dict:
            if key in merged_dict:
                # Ensure both arrays are standard numpy arrs before concatenation
                merged_dict[key] = np.concatenate([merged_dict[key], loaded_dict[key]])
            else:
                merged_dict[key] = loaded_dict[key]
    
    # Save the merged array to a new .npy file (optional)
    np.save(f'Comb_' + prefix +'_new.npy', merged_dict)
