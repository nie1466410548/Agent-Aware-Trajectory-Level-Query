import os
print(os.getcwd())
print(os.listdir('.'))
print(os.listdir('results') if os.path.isdir('results') else 'no results dir')