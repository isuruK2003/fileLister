import os
import json

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
        json.dump(data, file, indent = 2)

    print("Data saved to", filename)


def main():
    try: 
        directory = input("Enter the directory path: ").replace("\\", "/")
    
        if not directory:
            print("Current directory will be used")
            directory = os.getcwd()

        if not os.path.isdir(directory):
            print("Directory path does not point to a directory")
            return

        tree = listDir(directory)

        print(tree)

        if unpermitted_dirs:
            print("\nThese directories were not permitted to open:")
            print("\n".join(unpermitted_dirs), "\n")
        
        output_filename = directory.lower().replace("/", "_").replace(":", "_") + ".json"

        save(tree, f"data/{output_filename}")

    except KeyboardInterrupt:
        print("\nProgram aborted!")

if __name__ == "__main__":
    main()