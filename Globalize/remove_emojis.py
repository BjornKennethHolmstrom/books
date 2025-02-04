#!/usr/bin/env python3
import re
import os
import glob
import shutil
from datetime import datetime

def replace_emojis(text):
    # First remove the single quotes around emojis
    text = re.sub(r"'[✔✨🌍🚀📌]'", "", text)
    
    # Number replacements
    text = re.sub(r'1️⃣', '1.', text)
    text = re.sub(r'2️⃣', '2.', text)
    text = re.sub(r'3️⃣', '3.', text)
    text = re.sub(r'4️⃣', '4.', text)
    text = re.sub(r'5️⃣', '5.', text)
    text = re.sub(r'6️⃣', '6.', text)
    text = re.sub(r'7️⃣', '7.', text)
    text = re.sub(r'8️⃣', '8.', text)
    text = re.sub(r'9️⃣', '9.', text)
    
    # Book emoji
    text = re.sub(r'📖', '**Book:**', text)
    
    # Remove decorative emojis (both with and without quotes)
    emojis_to_remove = [
        r'🚀', r'📌', r'✨', r'🌍',  # Without quotes
        r"'🚀'", r"'📌'", r"'✨'", r"'🌍'"  # With quotes
    ]
    for emoji in emojis_to_remove:
        text = re.sub(emoji, '', text)
    
    # Replace checkmarks and crosses with markdown (both with and without quotes)
    text = re.sub(r'✔', '-', text)  # checkmark to bullet point
    text = re.sub(r"'✔'", '-', text)  # quoted checkmark to bullet point
    text = re.sub(r'🚫', '-', text)  # prohibition to bullet point
    text = re.sub(r"'🚫'", '-', text)  # quoted prohibition to bullet point
    
    # Replace arrows and other special characters
    text = re.sub(r'🔹', '-', text)  # small diamond to bullet point
    text = re.sub(r"'🔹'", '-', text)  # quoted small diamond to bullet point
    
    return text

def backup_directory(src_dir):
    """Create a backup of the src directory"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_dir = f'src_backup_{timestamp}'
    shutil.copytree(src_dir, backup_dir)
    print(f"Created backup at: {backup_dir}")
    return backup_dir

def process_file(filepath):
    # Read the file
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Replace emojis
    new_content = replace_emojis(content)
    
    # Only write if content has changed
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(new_content)
        print(f"Processed {filepath}")
    else:
        print(f"No changes needed in {filepath}")

def main():
    # Create backup first
    backup_dir = backup_directory('src')
    
    # Process all markdown files in src directory
    for filepath in glob.glob('src/*.md'):
        process_file(filepath)
    
    print(f"\nProcessing complete! Backup saved at: {backup_dir}")

if __name__ == "__main__":
    main()
