import os
import json
import sys

unpermitted_dirs = []

def listDir(dir_path):
    global unpermitted_dirs
    dir_name = dir_path.split("/")[-1]
    try:
        if not os.path.isdir(dir_path):
            return dir_name
        content = os.listdir(dir_path)
        return {dir_name:[listDir(f'{dir_path}/{d}') for d in content]}
    except PermissionError:
        unpermitted_dirs.append(dir_name)
        return {dir_name: []}

def save(data, filename="output.json"):
    if input("Save data? [Y/n]: ").lower() in ["no", "n"]:
        print("Stopped saving data")
        return

    with open(filename, "w") as file:
        json.dump(data, file, indent=2)

    print("Data saved to", filename)

def main():
    try:
        # Check if a command-line argument is provided
        if len(sys.argv) > 1:
            directory = sys.argv[1].replace("\\", "/")
        else:
            # Ask the user whether to use the current directory
            use_current = input("No directory argument provided. Use the current directory? [Y/n]: ").lower()
            if use_current in ["no", "n"]:
                directory = input("Please provide a directory path: ").replace("\\", "/")
            else:
                directory = os.getcwd()

        dir_structure = listDir(directory)
        print(json.dumps(dir_structure, indent=2))

        if unpermitted_dirs:
            print("\nWarning: Permission denied for the following directories:")
            for dir_name in unpermitted_dirs:
                print(f"- {dir_name}")

        save(dir_structure)

    except Exception as e:
        print(f"An uncaught error occurred: {e}")

if __name__ == "__main__":
    main()
