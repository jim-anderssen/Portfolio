import os
import hashlib
from collections import defaultdict
import time
import logging
import re

# Setup logging for debugging
logging.basicConfig(filename='debug.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')

# Function to compute the hash of a file
def get_file_hash(file_path, hash_algorithm='md5'):
    hash_func = hashlib.new(hash_algorithm)
    try:
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hash_func.update(chunk)
        return hash_func.hexdigest()
    except OSError as e:
        #logging.error(f"OSError while hashing file {file_path}: {e}")
        return None
    except Exception as e:
        #logging.error(f"Unexpected error while hashing file {file_path}: {e}")
        return None

if __name__ == "__main__":
    s = time.time()
    search_directory = 'J:/MILJOHÄLSOVÅRD/hälsoinspektionen -terveysvalvonta/Logon och hemsida'
    output_file = 'Z:/logon_duplicates.txt'
    temp_file_pattern = re.compile(r'^~\$.*$')
    

    # Dictionary to group files by their size
    size_dict = defaultdict(list)

    totals = 0

    # Step 1: Group files by size
    for root, dirs, files in os.walk(search_directory):
        for name in files:
            file_path = os.path.join(root, name)
            totals += 1
            if temp_file_pattern.match(name):
                logging.debug(f"Skipping temporary file: {file_path}")
                continue
            try:
                file_size = os.path.getsize(file_path)
                size_dict[file_size].append(file_path)    
            except Exception as e:
                continue
             

    # Dictionary to group files by their hash
    hash_dict = defaultdict(list)
    
    
    # Step 2: Compute hashes for files with the same size and group them by hash
    total_file_size = 0
    to_be_subtracted = 0
    for size, file_list in size_dict.items():
        total_file_size += size*(len(file_list)-1)
        if len(file_list) > 1:  # Only consider sizes with more than one file
            for file_path in file_list:
                try:    
                    file_hash = get_file_hash(file_path)
                    hash_dict[file_hash].append(file_path)
                except OSError:
                    continue
    

    # Step 3: Find duplicates and write them to the output file
    amount_different_files = 0
    total_files = 0
    amount_duplicates = 0
    with open(output_file, 'w', encoding='utf-8') as f:
        for file_hash, file_list in hash_dict.items():
            if len(file_list) > 1:  # Only consider hashes with more than one file
                f.write(f"Hash: {file_hash}\n")
                for file_path in file_list:
                    f.write(file_path + '\n')
                    amount_duplicates += 1
                f.write("\n")
                amount_different_files += 1
            total_files += 1
        f.write(f"Total files: {totals}, Amount of different files: {amount_different_files}, Amount of duplicates: {amount_duplicates-amount_different_files}, Total file size to be saved: {round(total_file_size/(1024*1024),2)} MB")
    e = time.time()
    print(f"Total time: {round((e-s)/60,2)} min")
