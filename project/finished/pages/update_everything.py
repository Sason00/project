import os
import subprocess

# Create the "code" directory if it does not exist
if not os.path.exists('code'):
    os.makedirs('code')

# Find all .ui files in the current directory
for filename in os.listdir():
    if filename.endswith('.ui'):
        # Use pyside6-uic to convert the .ui file to Python code
        subprocess.run(['pyside6-uic', filename, '-o', 'code/' + filename.replace('.ui', '.py')])
