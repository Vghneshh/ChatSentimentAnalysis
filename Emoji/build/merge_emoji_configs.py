#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script to merge existing config.py with expanded emoji dataset
Preserves existing emojis and adds new ones from CSV
"""

import ast
import os
import sys
import csv

def convert_position_to_sentiment(position):
    """Convert position (0-1) to sentiment score (-1 to +1)"""
    return (float(position) - 0.5) * 2

def unicode_hex_to_unicode_string(hex_str):
    """Convert hex unicode to unicode string format"""
    code_point = int(hex_str, 16)
    return f"\\U{code_point:08X}"

def read_existing_config(config_path):
    """Read existing config.py and extract emoji mappings"""
    existing = {}
    
    with open(config_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Try to parse as AST first
    try:
        tree = ast.parse(content)
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == 'emoji2sentiment':
                        if isinstance(node.value, ast.Dict):
                            for k, v in zip(node.value.keys, node.value.values):
                                if isinstance(k, ast.Str):
                                    if isinstance(v, ast.Num):
                                        existing[k.s] = v.n
                                    elif isinstance(v, ast.UnaryOp) and isinstance(v.operand, ast.Num):
                                        # Handle negative numbers
                                        if isinstance(v.op, ast.USub):
                                            existing[k.s] = -v.operand.n
    except:
        pass
    
    # Fallback: read file line by line and extract manually
    if not existing:
        with open(config_path, 'r', encoding='utf-8') as f:
            for line in f:
                if "u'\\U" in line or "u\"\\U" in line:
                    # Extract unicode and value
                    try:
                        # Find unicode string
                        import re
                        match = re.search(r"u['\"](\\.*?)['\"]:\s*([-\d.]+)", line)
                        if match:
                            unicode_str = match.group(1)
                            score = float(match.group(2))
                            existing[unicode_str] = score
                    except:
                        continue
    
    return existing

def read_csv_emojis(csv_path):
    """Read emojis from CSV file"""
    emoji_data = {}
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                unicode_hex = row['Unicode_codepoint']
                position = float(row['Position'])
                name = row['Unicode_name']
                
                if unicode_hex == '0xfffd' or not unicode_hex:
                    continue
                
                unicode_str = unicode_hex_to_unicode_string(unicode_hex)
                sentiment_score = convert_position_to_sentiment(position)
                
                emoji_data[unicode_str] = (sentiment_score, name)
            except (ValueError, KeyError):
                continue
    
    return emoji_data

def merge_configs(existing_config_path, csv_path, output_path):
    """Merge existing config with CSV data"""
    print("Reading existing config.py...")
    existing = read_existing_config(existing_config_path)
    print(f"Found {len(existing)} emojis in existing config")
    
    print("Reading CSV file...")
    csv_data = read_csv_emojis(csv_path)
    print(f"Found {len(csv_data)} emojis in CSV")
    
    # Merge: keep existing, add new from CSV
    merged = {}
    added_count = 0
    updated_count = 0
    
    # Add existing emojis
    for unicode_str, score in existing.items():
        merged[unicode_str] = (score, "EXISTING")
    
    # Add/update with CSV data (CSV takes precedence for sentiment scores)
    for unicode_str, (score, name) in csv_data.items():
        if unicode_str in merged:
            # Update existing with CSV data
            merged[unicode_str] = (score, name)
            updated_count += 1
        else:
            # Add new emoji
            merged[unicode_str] = (score, name)
            added_count += 1
    
    print(f"\nMerged results:")
    print(f"  Total emojis: {len(merged)}")
    print(f"  New emojis added: {added_count}")
    print(f"  Existing emojis updated: {updated_count}")
    
    # Generate merged config file
    header = '''"""
Dictionary of emoji unicode to sentiment score mappings
Expanded dataset from Emoji_Sentiment_Data_v1.0.csv merged with existing config

Subset of data used from the following research paper
    @article{Kralj2015emojis,
    author={{Kralj Novak}, Petra and Smailovi{\'c}, Jasmina and Sluban, Borut and Mozeti\v{c}, Igor},
    title={Sentiment of emojis},
    journal={PLoS ONE},
    volume={10},
    number={12},
    pages={e0144296},
    url={http://dx.doi.org/10.1371/journal.pone.0144296},
    year={2015}

For more info see -> http://kt.ijs.si/data/Emoji_sentiment_ranking/index.html

"""
emoji2sentiment = {'''
    
    lines = [header]
    
    # Sort by sentiment score (handle None values)
    sorted_items = sorted(merged.items(), key=lambda x: x[1][0] if x[1][0] is not None else -999, reverse=True)
    
    for unicode_str, (score, name) in sorted_items:
        if score is not None:
            lines.append(f"    u'{unicode_str}': {score:.9f},  # {name}")
    
    lines.append('}')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f"\nGenerated merged config file: {output_path}")
    return output_path

def main():
    # Get the Emoji directory (parent of build directory)
    build_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(build_dir)
    
    existing_config = os.path.join(base_dir, 'config.py')
    csv_path = os.path.join(build_dir, 'Emoji_Sentiment_Data_v1.0.csv')
    output_path = os.path.join(base_dir, 'config.py')
    backup_path = os.path.join(base_dir, 'config.py.backup')
    
    if not os.path.exists(existing_config):
        print(f"Error: Existing config not found at {existing_config}")
        sys.exit(1)
    
    if not os.path.exists(csv_path):
        print(f"Error: CSV file not found at {csv_path}")
        sys.exit(1)
    
    # Backup existing config
    import shutil
    shutil.copy2(existing_config, backup_path)
    print(f"Backed up existing config to: {backup_path}")
    
    # Merge configs
    merge_configs(existing_config, csv_path, output_path)
    print(f"\nSuccessfully merged emoji datasets!")
    print(f"   Original config backed up to: config.py.backup")
    print(f"   New config saved to: config.py")

if __name__ == '__main__':
    main()

