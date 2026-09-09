import os
# Check where the files are
print("CWD:", os.getcwd())
print("Files in CWD:", os.listdir('.'))
print("Absolute path of a file:", os.path.abspath('health_score_distribution.png'))
# Check if workspace root is accessible
ws_root = '/data/nly/Agent-Aware-Trajectory-Level-Query'
print("Workspace root exists:", os.path.exists(ws_root))
print("Work dir:", os.path.abspath('.'))
# Is there a symlink?
print("Work dir stats:", os.stat('.'))
# Link from work to workspace?
if os.path.exists(ws_root):
    print("Contents of workspace root:", os.listdir(ws_root)[:10])
    # Try to copy files to workspace
    import shutil
    for f in os.listdir('.'):
        if f.endswith('.png'):
            shutil.copy(f, os.path.join(ws_root, f))
            print(f"Copied {f} to {ws_root}")
    print("Files in workspace root now:", [f for f in os.listdir(ws_root) if f.endswith('.png')])