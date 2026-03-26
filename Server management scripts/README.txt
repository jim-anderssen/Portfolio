These are some python scripts I wrote for managing files on a shared server.  

The server contained tens of thousands of files, with a lot of junk and old files that wasn’t needed.

There were a lot of constraints on just deleting the files so some efficient way of sorting all the files was needed. I implemented these as command-line applications for ease of use.

Methods I used:
- Scan through server for and sort files by age (e.g find all files older than X years)
- Find all duplicate files by using hash key algorithms
- Find all paths that are nested over X amount of times
- Create a directory tree graph of any chosen directory
- Scan for all images and compress any img that’s over 400 KB. 

I mostly output the file paths to a text file, and then wrote a script to delete all files left in text file after manually checking what should be saved an not by looking at the filenames.