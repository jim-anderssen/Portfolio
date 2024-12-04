import os

### Check so it actually works

def process_duplicates(file_path):
    
    with open(file_path, 'r') as f:
        lines = f.readlines()

    hash_to_files = {}
    current_hash = None

    # Parse the file to map hashes to their corresponding file paths
    for line in lines:
        line = line.strip()
        if line.startswith("Hash: "):
            current_hash = line.split(" ")[1]
            hash_to_files[current_hash] = []
        elif current_hash:
            hash_to_files[current_hash].append(line)


    for hash_value,  files in hash_to_files.items():
        if len(files) > 1:
            files_to_keep = files[0]
            print(f"Keeping file: {files_to_keep}")
            files_to_delete = files[1:]

            for file_path in files_to_delete:
                try:
                    #os.remove(file_path)
                    print(f"Deleting file: {file_path}")
                except Exception as e:
                    print(f"Failed to delete {file_path}: {e}")

                 
    
if __name__ == "__main__":
    duplicates_file = "Z:/python_test_duplicates.txt"
    process_duplicates(duplicates_file)


