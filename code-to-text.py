#!/usr/bin/env python3

'''
This script combines the contents of all files in the current directory and its subdirectories into a single file called "combined_files.txt".
It also creates a file called "file_paths.txt" that contains the relative paths of each file included in the combined file.
'''

import os

def main():
    base_dir = os.getcwd()
    combined_file_name = "combined_files.txt"
    file_paths_file_name = "file_paths.txt"
    skip_dirs = ["google-api-php-client--PHP8.0"]
    skip_files = ["code-to-text.py"]
    
    combined_file_path = os.path.join(base_dir, combined_file_name)
    file_paths_file_path = os.path.join(base_dir, file_paths_file_name)
    
    # Open both output files
    with open(combined_file_path, "w", encoding="utf-8") as combined_file, \
         open(file_paths_file_path, "w", encoding="utf-8") as paths_file:
        
        directory_paths = set()
        file_paths = []
        
        # Walk through all directories and files starting at base_dir
        for root, dirs, files in os.walk(base_dir):
            # Remove directories that should be skipped and hidden directories (those starting with a period)
            dirs[:] = [d for d in dirs if d not in skip_dirs and not d.startswith('.')]
            
            rel_root = os.path.relpath(root, base_dir)
            directory_paths.add(rel_root)
            
            for file in files:
                # Skip the output files, hidden files (files starting with a period), and files in skip_files so we don't process them
                if file in [combined_file_name, file_paths_file_name] or file.startswith('.') or file in skip_files:
                    continue
                
                # Determine the relative path of the file
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, base_dir)
                
                file_paths.append(relative_path)
                
                # Write the header and then file content into combined_files.txt
                combined_file.write(f"[{relative_path}]\n")
                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        combined_file.write(f.read())
                except Exception as e:
                    # If the file can't be read (e.g. binary file or access issue), note the error
                    combined_file.write(f"Error reading file: {e}")
                combined_file.write("\n\n")  # Add spacing between files
        
        # Write directories and files to file_paths.txt in two sections
        paths_file.write("Directories:\n")
        for d in sorted(directory_paths):
            paths_file.write(d + "\n")

        paths_file.write("\nFiles:\n")
        for f in sorted(file_paths):
            paths_file.write(f + "\n")

if __name__ == '__main__':
    main()