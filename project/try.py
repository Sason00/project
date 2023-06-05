import os

def list_files(directory):
    for root, _, files in os.walk(directory):
        level = root.replace(directory, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        sub_indent = ' ' * 4 * (level + 1)
        for file in files:
            print('{}{}'.format(sub_indent, file))

directory_path = r'C:\Users\Ariel\Desktop\python_projects\project\My Project'
list_files(directory_path)
