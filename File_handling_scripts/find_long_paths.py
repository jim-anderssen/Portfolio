import os
import sys
import argparse

def find_long_path(root_directory, txt_file):
    long_paths = []
    total = 0
    for root,dirs,files in os.walk(root_directory):
        rel_path = os.path.relpath(root, root_directory)
        nesting_level = len(rel_path.split(os.sep))
        if nesting_level > 4:
            long_paths.append(root)
            # if the dir is nested more than 4 times from the root:
                # path = os.join(root, dir) 
                # long_paths.append(path)
            total += 1

    print('Writing paths to text file')
    with open(txt_file, 'w') as f:
        for file in long_paths:
            f.write(file + '\n')
        f.write(f"'Total amount of directories nested over 4 times: {total}'")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find long directory paths in a chosen directory")
    parser.add_argument('input', help='input directory')
    parser.add_argument('output', help='output file')
    args = parser.parse_args()
    
    print(f"Input directory: {args.input}")
    print(f"Text file: {args.output}")

    #input_directory = "J:/MILJOHÄLSOVÅRD/hälsoinspektionen -terveysvalvonta/Gemensamma"
    #txt_file = "Z:/Gemensamma_long_paths.txt"
    #find_long_path(input_directory, txt_file)
    find_long_path(args.input, args.output)