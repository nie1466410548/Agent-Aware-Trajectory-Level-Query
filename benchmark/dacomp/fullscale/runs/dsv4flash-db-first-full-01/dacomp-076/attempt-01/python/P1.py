import importlib
for mod in ['sklearn', 'scipy', 'matplotlib', 'seaborn']:
    try:
        importlib.import_module(mod)
        print(mod, 'OK')
    except Exception as e:
        print(mod, 'MISSING', e)
