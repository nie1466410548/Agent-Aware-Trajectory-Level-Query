import os
for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith('.png'):
            print(os.path.join(root, f))
    # limit depth
    if root.count(os.sep) > 2:
        dirs[:] = []
print("cwd:", os.getcwd())
print(os.listdir('.'))