import os

def print_file_content(file_path):
    with open(file_path, 'r') as file:
        print(f"Name: {os.path.basename(file_path)}")
        print(f"\n{file.read()}")

def process_directory(directory_path):
    for root, dirs, files in os.walk(directory_path):
        for file_name in files:
            if file_name.endswith(('.py', '.ui', '.css')):
                file_path = os.path.join(root, file_name)
                print_file_content(file_path)
                print('\n' * 2)

# Example usage:
path = r'C:\Users\Ariel\Desktop\python_projects\project\finished'
process_directory(path)
