import importlib.util

def importxl(module_path):
    spec = importlib.util.spec_from_file_location("example_module", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module