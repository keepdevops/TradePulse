#!/usr/bin/env python3
"""
Script to verify cleanup by comparing UNUSED_FILES_V10.9.txt with old directory
"""

import os
import re

def read_unused_files_list():
    """Read the list of unused files from UNUSED_FILES_V10.9.txt"""
    unused_files = []
    
    with open('UNUSED_FILES_V10.9.txt', 'r') as f:
        content = f.read()
    
    # Find the "ALL UNUSED FILES" section
    start_marker = "ALL UNUSED FILES"
    if start_marker in content:
        # Extract the section after the marker
        start_idx = content.find(start_marker)
        section = content[start_idx:]
        
        # Parse file paths (lines starting with numbers)
        lines = section.split('\n')
        for line in lines:
            line = line.strip()
            if line and line[0].isdigit() and '.py' in line:
                # Extract the file path (remove the number and dot)
                parts = line.split('. ', 1)
                if len(parts) > 1:
                    file_path = parts[1].strip()
                    if file_path.endswith('.py'):
                        unused_files.append(file_path)
    
    return unused_files

def get_files_in_old_directory():
    """Get all Python files in the old directory"""
    old_files = []
    
    for root, dirs, files in os.walk('old'):
        for file in files:
            if file.endswith('.py'):
                # Get relative path from old directory
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, 'old')
                old_files.append(relative_path)
    
    return old_files

def compare_lists():
    """Compare the two lists and report differences"""
    print("🔍 Verifying cleanup...")
    
    # Read the unused files list
    unused_files = read_unused_files_list()
    print(f"📋 Files listed in UNUSED_FILES_V10.9.txt: {len(unused_files)}")
    
    # Get files actually in old directory
    old_files = get_files_in_old_directory()
    print(f"📁 Files actually in old/ directory: {len(old_files)}")
    
    # Convert to sets for comparison
    unused_set = set(unused_files)
    old_set = set(old_files)
    
    # Find differences
    in_list_not_in_old = unused_set - old_set
    in_old_not_in_list = old_set - unused_set
    
    print(f"\n📊 COMPARISON RESULTS:")
    print(f"=" * 50)
    
    if not in_list_not_in_old and not in_old_not_in_list:
        print("✅ PERFECT MATCH! All files accounted for.")
    else:
        if in_list_not_in_old:
            print(f"❌ Files in list but NOT in old/ directory ({len(in_list_not_in_old)}):")
            for file_path in sorted(in_list_not_in_old):
                print(f"   - {file_path}")
        
        if in_old_not_in_list:
            print(f"⚠️ Files in old/ directory but NOT in list ({len(in_old_not_in_list)}):")
            for file_path in sorted(in_old_not_in_list):
                print(f"   - {file_path}")
    
    # Show some examples from each list
    print(f"\n📋 SAMPLE FROM UNUSED_FILES_V10.9.txt (first 10):")
    for i, file_path in enumerate(sorted(unused_files)[:10], 1):
        print(f"   {i:2d}. {file_path}")
    
    print(f"\n📁 SAMPLE FROM old/ DIRECTORY (first 10):")
    for i, file_path in enumerate(sorted(old_files)[:10], 1):
        print(f"   {i:2d}. {file_path}")
    
    return len(in_list_not_in_old) == 0 and len(in_old_not_in_list) == 0

def main():
    """Main function"""
    success = compare_lists()
    
    if success:
        print(f"\n🎉 VERIFICATION SUCCESSFUL!")
        print(f"All files from UNUSED_FILES_V10.9.txt are present in old/ directory.")
    else:
        print(f"\n⚠️ VERIFICATION FAILED!")
        print(f"There are discrepancies between the list and the old/ directory.")

if __name__ == "__main__":
    main()
