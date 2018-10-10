import os
import pathlib
import glob
import shutil

# Check existances of file and directory
print('test.csv exists: ', os.path.exists('test.csv'))
print('test.csv is a file: ', os.path.isfile('test.csv'))
print('test.csv is a directory: ', os.path.isdir('test.csv'))

# Manipulate CSV file
os.rename('test.csv', 'renamed.csv')
print('test.csv is renamed to renamed.csv: ', os.path.isfile('renamed.csv'))
os.rename('renamed.csv', 'test.csv')
print('renamed back to test.csv: ', os.path.isfile('test.csv'))

# Manipulate directories
os.mkdir('test_dir')
print('test_dir directory is created: ', os.path.isdir('test_dir'))
os.rmdir('test_dir')
print('test_dir is removed: ', not os.path.exists('test_dir'))

# pathlib
pathlib.Path('empty.txt').touch()
print('empty.txt is created using pathlib: ', os.path.exists('empty.txt'))
os.remove('empty.txt')
print('empty.txt is removed: ', not os.path.exists('empty.txt'))

# glob & os.listdir & shutil
os.mkdir('test_dir1')
print('test_dir1 created: ', os.path.exists('test_dir1'))
os.mkdir('test_dir1/test_dir2')
print('test_dir1/test_dir2 created: ', os.path.exists('test_dir1/test_dir2'))
print('List of directories under test_dir1', os.listdir('test_dir1'))
pathlib.Path('test_dir1/test_dir2/empty.txt').touch()
shutil.copy('test_dir1/test_dir2/empty.txt', 'test_dir1/test_dir2/empty2.txt')
print('List of files under test_dir2: ', glob.glob('test_dir1/test_dir2/*'))
os.remove('test_dir1/test_dir2/empty.txt')
shutil.rmtree('test_dir1')
print('All the files under test_dir1 is removed: ', not os.path.exists('test_dir1'))

# Show current directory using os.getcwd()
print('Current directory: ', os.getcwd())
