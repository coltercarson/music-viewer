import os

def print_folder_structure(root_path='.', max_depth=5, _prefix='', exclude=None):
    if exclude is None:
        exclude = {'.conda', '__pycache__', '.git'}

    try:
        items = sorted(os.listdir(root_path))
    except PermissionError:
        return

    for item in items:
        if item in exclude:
            continue
        full_path = os.path.join(root_path, item)
        print(f"{_prefix}├── {item}")
        if os.path.isdir(full_path) and max_depth > 1:
            print_folder_structure(full_path, max_depth=max_depth - 1, _prefix=_prefix + '│   ', exclude=exclude)

if __name__ == "__main__":
    print("📁 Project Folder Structure:\n")
    print_folder_structure('..')
