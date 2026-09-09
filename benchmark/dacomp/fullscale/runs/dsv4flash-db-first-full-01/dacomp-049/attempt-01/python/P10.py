import os
os.makedirs('work', exist_ok=True)
os.makedirs('/work', exist_ok=True)
print(os.getcwd())
print(os.listdir('.'))