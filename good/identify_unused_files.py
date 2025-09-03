#!/usr/bin/env python3
"""
Script to identify unused files in V10.9
Compares all Python files against the V10.9 refactored list
"""

import os
import re

def normalize_path(path):
    """Normalize path by removing ./ prefix"""
    if path.startswith('./'):
        return path[2:]
    return path

def read_v10_9_files():
    """Read the V10.9 refactored files list"""
    v10_9_files = set()
    
    # Read the extracted V10.9 files list
    with open('v10_9_files_list.txt', 'r') as f:
        for line in f:
            file_path = line.strip()
            if file_path.endswith('.py'):
                v10_9_files.add(normalize_path(file_path))
    
    return v10_9_files

def read_all_python_files():
    """Read all Python files in the project"""
    all_files = set()
    
    with open('all_python_files.txt', 'r') as f:
        for line in f:
            file_path = line.strip()
            if file_path.endswith('.py'):
                all_files.add(normalize_path(file_path))
    
    return all_files

def categorize_unused_files(unused_files):
    """Categorize unused files by type"""
    categories = {
        'old_monolithic_files': [],
        'old_launch_scripts': [],
        'old_test_files': [],
        'old_demo_files': [],
        'old_integration_files': [],
        'old_utility_files': [],
        'old_analysis_files': [],
        'old_ai_module_files': [],
        'old_portfolio_files': [],
        'old_chart_files': [],
        'old_data_files': [],
        'old_config_files': [],
        'old_message_files': [],
        'old_workflow_files': [],
        'miscellaneous': []
    }
    
    for file_path in unused_files:
        if 'modular_panel_ui' in file_path and 'refactored' not in file_path:
            categories['old_monolithic_files'].append(file_path)
        elif 'launch_' in file_path and 'refactored' not in file_path:
            categories['old_launch_scripts'].append(file_path)
        elif 'test_' in file_path and 'refactored' not in file_path:
            categories['old_test_files'].append(file_path)
        elif 'demo_' in file_path and 'refactored' not in file_path:
            categories['old_demo_files'].append(file_path)
        elif 'integration' in file_path and 'refactored' not in file_path:
            categories['old_integration_files'].append(file_path)
        elif 'utils' in file_path or 'utility' in file_path:
            categories['old_utility_files'].append(file_path)
        elif 'analyzer' in file_path or 'analysis' in file_path:
            categories['old_analysis_files'].append(file_path)
        elif 'ai_module' in file_path:
            categories['old_ai_module_files'].append(file_path)
        elif 'portfolio' in file_path and 'refactored' not in file_path:
            categories['old_portfolio_files'].append(file_path)
        elif 'chart' in file_path and 'refactored' not in file_path:
            categories['old_chart_files'].append(file_path)
        elif 'data' in file_path and 'refactored' not in file_path:
            categories['old_data_files'].append(file_path)
        elif 'config' in file_path:
            categories['old_config_files'].append(file_path)
        elif 'message' in file_path:
            categories['old_message_files'].append(file_path)
        elif 'workflow' in file_path:
            categories['old_workflow_files'].append(file_path)
        else:
            categories['miscellaneous'].append(file_path)
    
    return categories

def main():
    """Main function"""
    print("🔍 Identifying unused files in V10.9...")
    
    # Read V10.9 refactored files
    v10_9_files = read_v10_9_files()
    print(f"✅ Found {len(v10_9_files)} files in V10.9 refactored list")
    
    # Read all Python files
    all_files = read_all_python_files()
    print(f"✅ Found {len(all_files)} total Python files")
    
    # Find unused files
    unused_files = all_files - v10_9_files
    print(f"⚠️ Found {len(unused_files)} unused files")
    
    # Categorize unused files
    categories = categorize_unused_files(unused_files)
    
    # Write results to file
    with open('UNUSED_FILES_V10.9.txt', 'w') as f:
        f.write("=" * 80 + "\n")
        f.write("                    UNUSED FILES IN V10.9 SCRIPT\n")
        f.write("=" * 80 + "\n\n")
        
        f.write("SUMMARY:\n")
        f.write(f"- Total Python files: {len(all_files)}\n")
        f.write(f"- V10.9 refactored files: {len(v10_9_files)}\n")
        f.write(f"- Unused files: {len(unused_files)}\n")
        f.write(f"- Unused percentage: {(len(unused_files)/len(all_files)*100):.1f}%\n\n")
        
        f.write("=" * 80 + "\n")
        f.write("                                CATEGORIES\n")
        f.write("=" * 80 + "\n\n")
        
        for category, files in categories.items():
            if files:
                f.write(f"\n{category.upper().replace('_', ' ')} ({len(files)} files):\n")
                f.write("-" * 60 + "\n")
                for i, file_path in enumerate(sorted(files), 1):
                    f.write(f"{i:3d}. {file_path}\n")
        
        f.write("\n" + "=" * 80 + "\n")
        f.write("                                ALL UNUSED FILES\n")
        f.write("=" * 80 + "\n\n")
        
        for i, file_path in enumerate(sorted(unused_files), 1):
            f.write(f"{i:3d}. {file_path}\n")
    
    print(f"✅ Results written to UNUSED_FILES_V10.9.txt")
    print(f"📊 Summary: {len(unused_files)} unused files out of {len(all_files)} total files")

if __name__ == "__main__":
    main()
