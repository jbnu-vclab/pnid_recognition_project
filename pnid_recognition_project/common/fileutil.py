import os

def remove_files_in_dir(dir):
    for file in os.listdir(dir):
        existing_filepath = os.path.join(dir, file)
        if os.path.isfile(existing_filepath):
            os.remove(existing_filepath)

def dict_to_csv(dict):
    line = ""
    for k,v in dict.items():
        line += str(k) + "," + str(v) + ",\n"

    return line


def check_prompt(msg):
    yes = {'yes', 'y', 'ye', ''}
    no = {'no', 'n'}

    print(msg)
    choice = input().lower()
    if choice in yes:
        return True
    elif choice in no:
        return False
    else:
        print("Please respond with 'yes' or 'no'")