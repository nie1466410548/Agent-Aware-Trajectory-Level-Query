# Check available ML packages
import pkg_resources
packages = [d for d in pkg_resources.working_set]
print([p.key for p in packages if 'learn' in p.key.lower() or 'scikit' in p.key.lower() or 'numpy' in p.key.lower() or 'pandas' in p.key.lower()])