import os
# Find where the files were saved
for root, dirs, files in os.walk('/'):
    for f in files:
        if f.endswith('.png') and 'category' in f:
            print(os.path.join(root, f))
            break
    else:
        continue
    break

# Also check the working directory
print("CWD:", os.getcwd())
print("ls:", os.listdir('.'))
print("ls work:", os.listdir('/work'))