import os
import argparse

def delete_files(text_file):
    deleted_paths = set()
    total = 0

    with open(text_file, 'r', encoding='utf-8') as f:
        paths = f.read().splitlines()
    i = 0
    for path in paths:
        if os.path.exists(path):
            try:
                size = os.path.getsize(path)
                os.remove(path)
                total += size
                deleted_paths.add(path)
            except Exception as e:
                print(f"Failed to read path")
        else:
            i += 1
            print("Path does not exist: ", path)
    print(f"Total size removed: {round(total/(1000*1000*1000),3)} GB, not removed: {i}")

    remaining_paths = [path for path in paths if path not in deleted_paths]
    return remaining_paths

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Delete all files with locations given from text file")
    parser.add_argument('input', help="Input text file from where to delete files")
    args = parser.parse_args()
    #input_file = "Z:/egen_version_av_borttagningsfiler/hälsoskydd_5år.txt"
    remaining_paths = delete_files(args.input)
    
    with open(args.input, 'w', encoding='utf-8') as f:
        f.write('Paths remaining after deleting files: ' +'\n')
        f.write('\n'.join(remaining_paths))
        f.write(f"Length of remaining paths: {len(remaining_paths)}")
        