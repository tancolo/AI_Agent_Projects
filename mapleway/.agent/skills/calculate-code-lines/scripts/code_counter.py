import os
import re

# Configuration for file extensions and their comment styles
# Format: 'extension': {'single': 'prefix', 'multi_start': 'start', 'multi_end': 'end'}
LANGUAGE_CONFIG = {
    '.py': {'single': '#', 'multi_start': ['"""', "'''"], 'multi_end': ['"""', "'''"]},
    '.rb': {'single': '#', 'multi_start': ['=begin'], 'multi_end': ['=end']},
    '.java': {'single': '//', 'multi_start': ['/*'], 'multi_end': ['*/']},
    '.c': {'single': '//', 'multi_start': ['/*'], 'multi_end': ['*/']},
    '.cpp': {'single': '//', 'multi_start': ['/*'], 'multi_end': ['*/']},
    '.h': {'single': '//', 'multi_start': ['/*'], 'multi_end': ['*/']},
    '.js': {'single': '//', 'multi_start': ['/*'], 'multi_end': ['*/']},
    '.ts': {'single': '//', 'multi_start': ['/*'], 'multi_end': ['*/']},
    '.kt': {'single': '//', 'multi_start': ['/*'], 'multi_end': ['*/']},
    '.go': {'single': '//', 'multi_start': ['/*'], 'multi_end': ['*/']},
}

IGNORED_DIRS = {'.git', '.idea', '__pycache__', 'venv', 'node_modules', 'dist', 'build', 'artifacts', '.gemini'}

def count_lines(file_path, config):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return 0

    code_lines = 0
    in_block_comment = False
    block_comment_end_token = None

    single = config.get('single')
    multi_starts = config.get('multi_start', [])
    multi_ends = config.get('multi_end', [])
    
    # Normalize Multi-line configs to lists if they are strings (not strictly needed with current config but good for robustness)
    if isinstance(multi_starts, str): multi_starts = [multi_starts]
    if isinstance(multi_ends, str): multi_ends = [multi_ends]

    for line in lines:
        line = line.strip()
        
        if not line:
            continue

        if in_block_comment:
            # Check if block comment ends
            # For Python/Ruby, checking if the line contains the end token
             # Simple logic: if line contains end token, assumption: code might follow or it ends the block
            if block_comment_end_token:
                 if block_comment_end_token in line:
                    in_block_comment = False
                    # Technically, there could be code after the block comment on the same line. 
                    # For simplicity and typical usage, we'll assume it's negligible or check strictness.
                    # If we want to be strict: remove the comment part and check if anything remains.
                    # Let's simple check:
                    if not line.endswith(block_comment_end_token) and len(line.split(block_comment_end_token)[-1].strip()) > 0:
                        code_lines += 1
            else:
                # Should not happen if logic is correct
                in_block_comment = False
            continue

        # Check for start of block comment
        block_started = False
        for i, start_token in enumerate(multi_starts):
            if line.startswith(start_token):
                in_block_comment = True
                block_comment_end_token = multi_ends[i]
                
                # Check if it also ends on the same line (e.g. /* comment */)
                if block_comment_end_token in line[len(start_token):]:
                     in_block_comment = False
                     # Again, check if there is code around it? 
                     # Case: /* comment */ int a = 1; -> starts with /*, so filtered.
                     # Case: int a = 1; /* comment */ -> handled by single line check or inline logic?
                     # Current logic "startswith" assumes comment takes up the start of the line.
                
                block_started = True
                break
        
        if block_started:
            continue

        # Check for single line comment
        if single and line.startswith(single):
            continue

        code_lines += 1

    return code_lines

def analyze_directory(directory):
    stats = {lang: 0 for lang in LANGUAGE_CONFIG}
    stats['Total'] = 0
    
    # Map extension to display name
    ext_map = {
        '.py': 'Python',
        '.rb': 'Ruby',
        '.java': 'Java',
        '.c': 'C',
        '.cpp': 'C++',
        '.h': 'C/C++ Header',
        '.js': 'JavaScript',
        '.ts': 'TypeScript',
        '.kt': 'Kotlin',
        '.go': 'Go'
    }

    display_stats = {}

    for root, dirs, files in os.walk(directory):
        # Ignore hidden directories and common ignore patterns
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS and not d.startswith('.')]
        
        for file in files:
            ext = os.path.splitext(file)[1]
            if ext in LANGUAGE_CONFIG:
                file_path = os.path.join(root, file)
                lines = count_lines(file_path, LANGUAGE_CONFIG[ext])
                stats[ext] += lines
                
    
    # Calculate Total
    total_lines = sum(stats[ext] for ext in LANGUAGE_CONFIG)
    
    # Build Display Dictionary
    for ext, name in ext_map.items():
        if ext in stats and stats[ext] > 0:
             display_stats[name] = stats[ext]
             
    return display_stats, total_lines

def print_table(stats, total):
    # Sort stats by line count descending
    sorted_stats = sorted(stats.items(), key=lambda item: item[1], reverse=True)
    
    headers = [k for k, v in sorted_stats] + ["Total code lines"]
    
    # Build calculation string
    calc_str = " + ".join([f"{v:,}" for k, v in sorted_stats]) + f" = {total:,}"
    
    # Markdown Table Construction
    # | Lang1 | Lang2 | ... | Total code lines |
    # | :--- | :--- | ... | ---: |
    # | val1 | val2 | ... | calc_string |
    
    header_row = "| " + " | ".join(headers) + " |"
    separator_row = "| " + " | ".join([":---:" if i < len(headers)-1 else "---:" for i in range(len(headers))]) + " |"
    
    values = [f"{v:,}" for k, v in sorted_stats]
    value_row = "| " + " | ".join(values) + f" | {calc_str} |"
    
    print("\nCode Line Analysis Report:\n")
    print(header_row)
    print(separator_row)
    print(value_row)
    print("\n")

if __name__ == "__main__":
    current_dir = os.getcwd()
    # Go up one level if we are inside skills_scripts to scan the project root, 
    # OR scan current if run from root. 
    # Assumption: script is in ./skills_scripts and we want to scan the project root (parent)
    # But usually a scraper project structure might be:
    # root/
    #   skills_scripts/
    #   code/
    # So we probably want to scan the parent directory of this script's location if it's inside a subdir,
    # or just current working directory if the user calls it from root.
    
    # Let's default to scanning the current working directory, 
    # but the user might run it from root.
    target_dir = current_dir
    
    print(f"Analyzing directory: {target_dir}")
    stats, total = analyze_directory(target_dir)
    print_table(stats, total)
