import os
os.makedirs('work', exist_ok=True)
print("work dir created:", os.path.exists('work'))
print(os.listdir('.'))
