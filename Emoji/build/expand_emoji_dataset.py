#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script to expand emoji sentiment dataset from CSV file
Converts emoji sentiment data to the format used in config.py
"""

import csv
import os
import sys

def convert_position_to_sentiment(position):
    """
    Convert position (0-1 range) to sentiment score (-1 to +1 range)
    Position 0.5 = neutral (0.0)
    Position > 0.5 = positive (0.0 to 1.0)
    Position < 0.5 = negative (-1.0 to 0.0)
    """
    # Convert 0-1 range to -1 to +1 range
    # Formula: (position - 0.5) * 2
    return (float(position) - 0.5) * 2

def unicode_hex_to_unicode_string(hex_str):
    """
    Convert hex unicode string (e.g., '0x1f602') to unicode string format
    Returns format like '\U0001F602'
    """
    # Remove '0x' prefix and convert to int
    code_point = int(hex_str, 16)
    # Convert to unicode escape sequence
    return f"\\U{code_point:08X}"

def read_csv_and_convert(csv_path):
    """
    Read CSV file and convert to config.py format
    Returns list of tuples: (unicode_string, sentiment_score, emoji_char, name)
    """
    emoji_data = []
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                emoji_char = row['Emoji']
                unicode_hex = row['Unicode_codepoint']
                position = float(row['Position'])
                name = row['Unicode_name']
                
                # Skip replacement character and invalid entries
                if unicode_hex == '0xfffd' or not emoji_char or emoji_char == '':
                    continue
                
                # Convert position to sentiment score
                sentiment_score = convert_position_to_sentiment(position)
                
                # Convert hex to unicode string format
                unicode_str = unicode_hex_to_unicode_string(unicode_hex)
                
                emoji_data.append((unicode_str, sentiment_score, emoji_char, name))
            except (ValueError, KeyError) as e:
                print(f"Skipping row due to error: {e}")
                continue
    
    return emoji_data

def generate_config_code(emoji_data):
    """
    Generate Python code for config.py from emoji data
    """
    lines = []
    lines.append('"""')
    lines.append('Dictionary of emoji unicode to sentiment score mappings')
    lines.append('Expanded dataset from Emoji_Sentiment_Data_v1.0.csv')
    lines.append('')
    lines.append('Subset of data used from the following research paper')
    lines.append('    @article{Kralj2015emojis,')
    lines.append('    author={{Kralj Novak}, Petra and Smailovi{\'c}, Jasmina and Sluban, Borut and Mozeti\v{c}, Igor},')
    lines.append('    title={Sentiment of emojis},')
    lines.append('    journal={PLoS ONE},')
    lines.append('    volume={10},')
    lines.append('    number={12},')
    lines.append('    pages={e0144296},')
    lines.append('    url={http://dx.doi.org/10.1371/journal.pone.0144296},')
    lines.append('    year={2015}')
    lines.append('')
    lines.append('For more info see -> http://kt.ijs.si/data/Emoji_sentiment_ranking/index.html')
    lines.append('')
    lines.append('"""')
    lines.append('emoji2sentiment = {')
    
    # Sort by sentiment score for better readability
    sorted_data = sorted(emoji_data, key=lambda x: x[1], reverse=True)
    
    for unicode_str, sentiment_score, emoji_char, name in sorted_data:
        # Format: u'\U0001F602': 0.308920547,  # FACE WITH TEARS OF JOY
        lines.append(f"    u'{unicode_str}': {sentiment_score:.9f},  # {name}")
    
    lines.append('}')
    
    return '\n'.join(lines)

def main():
    # Path to CSV file
    csv_path = os.path.join(os.path.dirname(__file__), 'Emoji_Sentiment_Data_v1.0.csv')
    
    if not os.path.exists(csv_path):
        print(f"Error: CSV file not found at {csv_path}")
        sys.exit(1)
    
    print("Reading emoji sentiment data from CSV...")
    emoji_data = read_csv_and_convert(csv_path)
    print(f"Found {len(emoji_data)} emojis with sentiment data")
    
    # Generate config code
    print("Generating config.py code...")
    config_code = generate_config_code(emoji_data)
    
    # Write to new config file
    output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config_expanded.py')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(config_code)
    
    print(f"Generated expanded config file: {output_path}")
    print(f"Total emojis: {len(emoji_data)}")
    print("\nTo use the expanded dataset:")
    print("1. Backup the current config.py")
    print("2. Replace config.py with config_expanded.py")
    print("   OR merge the new emojis into the existing config.py")

if __name__ == '__main__':
    main()

