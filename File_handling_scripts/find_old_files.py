

import os
from datetime import datetime, timedelta
import argparse



# Function to find files older than a given date
def find_files_older_than(root_folder, age, all):
    cutoff_date = datetime.now() - timedelta(days=age*365)
    if not all:
        # Interval between x years and x+1 years from today's date
        cutoff_interval = datetime.now()-timedelta(days=(age)*365), datetime.now()-timedelta(days=(age+1)*365)
    
    older_files = []
    total_found = 0
    total_not_found = 0
    
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            try:
                file_path = os.path.join(root, file)
                file_modified_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                if all:
                    if file_modified_time < cutoff_date:
                        older_files.append(file_path)
                else:
                    if file_modified_time < cutoff_interval[0] and file_modified_time > cutoff_interval[1]:
                        older_files.append(file_path)
                total_found += 1
            except Exception as e:
                total_not_found += 1
                print('File could not be found: ',root, file)
    return older_files,total_found,total_not_found

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Finds all files with a chosen age (5,10,15 years etc)")
    parser.add_argument('input',help="Input directory to search files")
    parser.add_argument('output',help='Text file to output all files found')
    parser.add_argument('age',help='Specific age x to find (older than x years, but not older than x+1 years)',type=int)
    parser.add_argument('--all',help='Finds all files older than given age x',action="store_true")
    args = parser.parse_args()
    
    #root_directory = "J:/MILJOHÄLSOVÅRD/hälsoinspektionen -terveysvalvonta/Hälsoskydd"
    #output_file = "Z:/hälsoskydd_lastmodified_older_5years.txt"

    # Find all files older than x years
    older_files,total_found,total_not_found = find_files_older_than(args.input, args.age,args.all)

    # Save full paths to a text file
    with open(args.output, 'w', encoding='utf-8') as f:
        if args.all:
            f.write(f"All files older than {datetime.now()-timedelta(days=(args.age)*365)}"+'\n')
        else:
            f.write(f"Files within the interval of {datetime.now()-timedelta(days=(args.age)*365)} and {datetime.now()-timedelta(days=(args.age+1)*365)}:"+'\n')
        for file_path in older_files:
            f.write(file_path + '\n')

    
        f.write(f"Found: {total_found}, Not_found: {total_not_found}"+'\n')
        f.write(f"Saved paths of {len(older_files)} older files")