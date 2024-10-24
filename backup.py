import os
import time
import zipfile
from os import stat
from time import ctime
from colorama import Fore, Style


path = input('Enter the path for searching files, like C:\\ : ')
target_dir = input("Enter the path for making your backup, like C:\\ : ")
time_sort = input("Would you like to sort your files by creation date? (y/n): ")
extension_filter = input("Would you like to filter files by extension? (y/n): ")

data_list = []

if extension_filter.lower() == 'y':
    file_extensions = input('Enter the extensions of files you want to include in backup (comma separated: .exe, .txt): ')
    extension_filter = [ext.strip() for ext in file_extensions.split(',')]

teme = None
if time_sort.lower() == 'y':
    while True:
        try:
            teme = int(input('-- Enter the period of time during which the files for sorting were created (in seconds): '))
            if teme < 0:
                print("Please enter a non-negative number.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

for address, dirs, files in os.walk(path):
    for file in files:
        full_path = os.path.join(address, file)

        if extension_filter and not any(full_path.endswith(ext) for ext in extension_filter):
            continue  

        if time_sort.lower() == 'y':
            if teme is not None and (time.time() - os.path.getctime(full_path)) < teme:
                continue  

        data_list.append(full_path)

utf1 = ''
while True:
    utf = input("Enter the number (8; 16; 32) of encoding you prefer (utf-8; utf-16; utf-32): ")
    if utf == '8' or utf.lower() == 'utf-8':
        utf1 = 'utf-8'
        break
    elif utf == '16' or utf.lower() == 'utf-16':
        utf1 = 'utf-16'
        break
    elif utf == '32' or utf.lower() == 'utf-32':
        utf1 = 'utf-32'
        break
    else:
        print('Incorrect encoding')
        continue

zip_file_path = os.path.join(target_dir, "backup_package.zip")
file_path = os.path.join(target_dir, "backup_metadata.txt")

if not os.path.exists(file_path):
    with open(file_path, 'w', encoding=utf1) as file:
        file.write('\n')  
    print(f'File "{file_path}" has been created.')
else:
    print(f'File "{file_path}" already exists.')

def file_metadata(file_name):
    stat_info = stat(file_name)
    mode = oct(stat_info.st_mode)
    with open(file_path, 'a', encoding=utf1) as f:
        f.write(f'\n\tMode: {mode}\n')

    created = ctime(stat_info.st_ctime)
    with open(file_path, 'a', encoding=utf1) as f:
        f.write(f'\tCreated: {created}\n')

    accessed = ctime(stat_info.st_atime)
    with open(file_path, 'a', encoding=utf1) as f:
        f.write(f'\tAccessed: {accessed}\n')

    modified = ctime(stat_info.st_mtime)
    with open(file_path, 'a', encoding=utf1) as f:
        f.write(f'\tModified: {modified}\n')

def processing():
    with zipfile.ZipFile(zip_file_path, 'w') as zipf:
        for full_path in data_list:  
            zipf.write(full_path, os.path.relpath(full_path, path))
            file_metadata(full_path)  
            with open(file_path, 'a', encoding=utf1) as f:
                f.write(f'{full_path}\n')

processing()  

print(Fore.GREEN + 'Backup successfully created at', zip_file_path, Style.RESET_ALL)
input("Press 'Enter' to escape...")
