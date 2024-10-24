import os
import time
import zipfile
from os import stat
from time import ctime

path = input('Enter the path for searching files, like C:\\ : ')
target_dir = input("Enter the path for making your backup, like C:\\ : ")
time_sort = input("Would you like to sort your files by creation date? (y/n): ")
extension_filter = input("Would you like to filter files by extension? (y/n): ")

# sorting by extension (if needed)
if extension_filter == 'y':
    file_extension = input('Enter the extension of files you want to include in backup (.exe; .txt): ')

# requesting the period of time
teme = None
if time_sort == 'y':
    while True:
        try:
            teme = int(
                input('-- Enter the period of time during which the files for sorting were created (in seconds): '))
            if teme < 0:
                print("Please enter a non-negative number.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

data_list = []
# collecting files in data_list
for adress, dirs, files in os.walk(path):
    for file in files:
        full_path = os.path.join(adress, file)

        # sorting by extension if needed
        if extension_filter == 'y' and not full_path.endswith(file_extension):
            continue

        # sorting by creating time if needed
        if time_sort == 'y':
            if teme is not None and (time.time() - os.path.getctime(full_path)) < teme:
                data_list.append(full_path)
        else:
            data_list.append(full_path)

# sorting by creating time (if needed)
if time_sort == 'y' and teme is not None:
    data_list.sort(key=os.path.getctime)

# request for choosing endocing
utf1 = ''
while True:
    utf = input("Enter the number (8; 16; 32) of encoding you prefer (utf-8; utf-16; utf-32): ")
    if utf == '8' or utf == 'utf-8':
        utf1 = 'utf-8'
        break
    elif utf == '16' or utf == 'utf-16':
        utf1 = 'utf-16'
        break
    elif utf == '32' or utf == 'utf-32':
        utf1 = 'utf-32'
        break
    else:
        print('Incorrect encoding')
        continue

zip_file_path = os.path.join(target_dir, "backup_package.zip")
file_path = os.path.join(target_dir, "backup_metadata.txt")

if not os.path.exists(file_path):
    with open(file_path, 'w', encoding=utf1) as file:
        file.write('\n')  # initializing the file
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


# Opening zip file for adding data
with zipfile.ZipFile(zip_file_path, 'w') as zipf:
    for full_path in data_list:  # using sorted list
        zipf.write(full_path, os.path.relpath(full_path, path))
        file_metadata(full_path)  # metadata collection
        with open(file_path, 'a', encoding=utf1) as f:
            f.write(f'{full_path}\n')

print('Backup successfully created at', zip_file_path)
input()
