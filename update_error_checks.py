import os
import re

# Path to the file
avize_path = r'e:\NEW_python\RGT\StudiiFezabilitate\Avize\Iasi\avize.py'

# Read the content of the file
with open(avize_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Count occurrences before replacement
count_before = content.count("if errors:")

# Replace all instances of "if errors:" with the corrected check
modified_content = content.replace(
    "if errors:",
    "# Check if errors is a DocumentGenerationResult and if it's an error result\n        if errors is not None and not errors.is_success():"
)

# Count occurrences after replacement
count_after = modified_content.count(
    "if errors is not None and not errors.is_success():")

# Write the modified content back to a new file for safety
with open(avize_path + '.modified', 'w', encoding='utf-8') as f:
    f.write(modified_content)

# Log the changes
with open(r'e:\NEW_python\RGT\update_log.txt', 'w') as f:
    f.write(f"Replacements made: {count_after}\n")
    f.write(f"Original 'if errors:' count: {count_before}\n")

print(f"File processed. Replacements made: {count_after}")
print(f"Original 'if errors:' count: {count_before}")
print("Check the .modified file for changes.")
