#!/usr/bin/env python3
"""
Script to move unused files to the old directory
Safely moves all files listed in UNUSED_FILES_V10.9.txt to the old/ directory
"""

import os
import shutil
from pathlib import Path

def read_unused_files():
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

def move_file_safely(file_path, old_dir):
    """Safely move a file to the old directory, creating subdirectories as needed"""
    try:
        # Create the full path in the old directory
        old_path = os.path.join(old_dir, file_path)
        
        # Create the directory structure if it doesn't exist
        old_dir_path = os.path.dirname(old_path)
        if old_dir_path and not os.path.exists(old_dir_path):
            os.makedirs(old_dir_path, exist_ok=True)
        
        # Check if source file exists
        if os.path.exists(file_path):
            # Move the file
            shutil.move(file_path, old_path)
            return True, None
        else:
            return False, f"Source file not found: {file_path}"
            
    except Exception as e:
        return False, str(e)

def main():
    """Main function"""
    print("🗂️ Moving unused files to old/ directory...")
    
    # Read unused files
    unused_files = read_unused_files()
    print(f"📋 Found {len(unused_files)} unused files to move")
    
    # Create old directory if it doesn't exist
    old_dir = "old"
    if not os.path.exists(old_dir):
        os.makedirs(old_dir)
        print(f"✅ Created {old_dir}/ directory")
    
    # Track results
    moved_count = 0
    failed_count = 0
    failed_files = []
    
    # Move each file
    for i, file_path in enumerate(unused_files, 1):
        print(f"📦 [{i:3d}/{len(unused_files)}] Moving: {file_path}")
        
        success, error = move_file_safely(file_path, old_dir)
        
        if success:
            moved_count += 1
            print(f"   ✅ Moved successfully")
        else:
            failed_count += 1
            failed_files.append((file_path, error))
            print(f"   ❌ Failed: {error}")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 MOVEMENT SUMMARY")
    print("=" * 60)
    print(f"Total files to move: {len(unused_files)}")
    print(f"Successfully moved: {moved_count}")
    print(f"Failed to move: {failed_count}")
    
    if failed_files:
        print(f"\n❌ FAILED FILES:")
        for file_path, error in failed_files:
            print(f"   - {file_path}: {error}")
    
    # Create a summary file
    with open('old/movement_summary.txt', 'w') as f:
        f.write("UNUSED FILES MOVEMENT SUMMARY\n")
        f.write("=" * 40 + "\n\n")
        f.write(f"Total files to move: {len(unused_files)}\n")
        f.write(f"Successfully moved: {moved_count}\n")
        f.write(f"Failed to move: {failed_count}\n\n")
        
        if failed_files:
            f.write("FAILED FILES:\n")
            f.write("-" * 20 + "\n")
            for file_path, error in failed_files:
                f.write(f"- {file_path}: {error}\n")
    
    print(f"\n✅ Movement summary saved to old/movement_summary.txt")
    print(f"🎉 Cleanup completed! {moved_count} files moved to old/ directory")

if __name__ == "__main__":
    main()
