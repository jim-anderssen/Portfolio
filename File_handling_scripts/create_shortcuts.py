import os
import sys
import winshell

def create_shortcuts(input_file, output_folder):
    with open(input_file, 'r',encoding='utf-16') as f:
        paths = f.read().splitlines()

    for path in paths:
        if os.path.exists(path):
            base_name = os.path.basename(path)
            print('Path:',path)
            print('Base_name:',base_name)
            shortcut_name = os.path.join(output_folder, f"{base_name}.lnk")
            print('Shortcut name:',shortcut_name)
            print()
            try:
                desktop = winshell.desktop()
                with winshell.shortcut(shortcut_name) as shortcut:
                    shortcut.path = path
                    shortcut.icon = path, 0  # Example: Use the file's icon if available
                    shortcut.description = "Shortcut created using Python script"
                
                print(f"Shortcut created for {path}")
            except Exception as e:
                print(f"Failed to create shortcut for {path}: {e}")
        else:
            print(f"Path does not exist: {path}")

if __name__ == "__main__":
    #if len(sys.argv) < 3:
    #    print("Usage: python create_shortcuts.py <input_file> <output_folder>")
    #    sys.exit(1)
    
    #input_file = sys.argv[1]
    #output_folder = sys.argv[2]
    input_file = "z:\gemensamma_files_older_than_5_years.txt" 
    output_folder = "Z:/shortcuts_gemensamma_5_years"

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    create_shortcuts(input_file, output_folder)