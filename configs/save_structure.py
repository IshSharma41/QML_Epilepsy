import os

def save_directory_structure(root_dir, output_file, depth_rules=None, exclude_dirs=None, default_max_depth=99):
    depth_rules = depth_rules or {}
    exclude_dirs = exclude_dirs or []

    with open(output_file, 'w', encoding='utf-8') as f:
        for dirpath, dirnames, filenames in os.walk(root_dir):
            rel_path = os.path.relpath(dirpath, root_dir)
            level = 0 if rel_path == "." else rel_path.count(os.sep)

            # Top-most folder in this path
            parts = rel_path.split(os.sep) if rel_path != "." else []
            top_folder = parts[0] if parts else os.path.basename(root_dir)

            # Depth rule for this top-level folder
            max_depth = depth_rules.get(top_folder, default_max_depth)

            # Handle "only list folder contents" case when depth == rule
            if level == max_depth and max_depth in depth_rules.values():
                indent = '│   ' * level + '├── '
                f.write(f"{indent}{os.path.basename(dirpath)}/\n")

                # List contents like a flat dir
                subindent = '│   ' * (level + 1)
                for name in sorted(dirnames + filenames):
                    f.write(f"{subindent}└── {name}\n")

                # Prevent further walking
                dirnames.clear()
                continue

            # Skip if deeper than allowed
            if level > max_depth:
                dirnames.clear()
                continue

            # Filter excluded dirs
            dirnames[:] = [d for d in dirnames if d not in exclude_dirs]

            # Sort
            dirnames.sort()
            filenames.sort()

            # Write directory
            indent = '│   ' * level + '├── '
            f.write(f"{indent}{os.path.basename(dirpath)}/\n")

            # Write files
            subindent = '│   ' * (level + 1)
            for file in filenames:
                f.write(f"{subindent}└── {file}\n")

# === Usage ===

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, os.pardir))
output_txt = os.path.join(project_root, 'project_structure.txt')

save_directory_structure(
    root_dir=project_root,
    output_file=output_txt,
    depth_rules={
        "libs": 0,
        "data": 1,
        "experiments":0
    },
    exclude_dirs=["venv4qml"],
    default_max_depth=4
)
