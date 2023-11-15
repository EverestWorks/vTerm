import os
import platform
import subprocess
import sys
import shutil
from pathlib import Path
import re
from difflib import get_close_matches

command_help = {
    "copy": "Copy a directory from source to destination. Usage: copy source destination",
    "python": "Execute Python code interactively. Usage: python",
    "ls": "List files and directories in the current directory. Usage: ls",
    "cd": "Change the current directory. Usage: cd directory",
    "mkdir": "Create a new directory. Usage: mkdir directory",
    "clear": "Clear the terminal screen. Usage: clear",
    "man": "View descriptions of available commands. Usage: man command",
    "exit": "Exit the terminal. Usage: exit",
    "edit": "Edit or create a text file. Usage: edit filename",
    "view": "View the content of a text file. Usage: view filename",
    "touch": "Create an empty file. Usage: touch filename",
    "rm": "Remove a file or directory. Usage: rm filename or rm -r directory"
}

def print_warning_and_developer_info():
    print("\033[1;31mWarning: This is a development environment, and there may be bugs.")
    print("\033[1;34mCopyright: \033[1;36mEverest works @2023\033[0m\n")

def stylized_prompt(current_directory):
    return f"\033[1;32m{current_directory}\033[0;35m: >> \033[0m"

def clear_screen():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, text=True, capture_output=True)
        output = result.stdout
        return output
    except Exception as e:
        return str(e)

def execute_commands_with_pipes(commands):
    processes = []
    for cmd in commands:
        processes.append(subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True))
    output = processes[0].communicate()[0]
    for p in processes[1:]:
        output = p.communicate(input=output)[0]
    return output

def grep(pattern, text):
    lines = text.split('\n')
    matching_lines = [line for line in lines if re.search(pattern, line)]
    return '\n'.join(matching_lines)

def copy_directory(source, destination):
    try:
        shutil.copytree(source, destination)
        return f"Directory copied from {source} to {destination}"
    except Exception as e:
        return f"Error copying directory: {str(e)}"

def execute_python_code(code):
    try:
        exec_result = exec(code)
        return str(exec_result)
    except Exception as e:
        return str(e)

def list_files_in_current_directory():
    files = os.listdir()
    for file in files:
        print(file)

def change_directory(new_dir):
    try:
        os.chdir(new_dir)
        print(f"Changed directory to: {new_dir}")
    except FileNotFoundError:
        print(f"Directory not found: {new_dir}")

def create_directory(new_dir):
    try:
        os.mkdir(new_dir)
        print(f"Created directory: {new_dir}")
    except FileExistsError:
        print(f"Directory already exists: {new_dir}")

def display_help(command):
    if command in command_help:
        print(f"Help for {command}:")
        print(command_help[command])
    else:
        print(f"Help for {command} not found.")

def display_command_usage(command):
    if command in command_help:
        print(f"Usage: {command_help[command]}")
    else:
        print(f"Usage information for {command} not found.")

def edit_file(filename):
    try:
        with open(filename, 'r') as file:
            content = file.read()

        print("Enter your text. Press Ctrl+D to save and exit.")
        lines = []
        while True:
            try:
                line = input()
                lines.append(line)
            except EOFError:
                break

        content = '\n'.join(lines)

        with open(filename, 'w') as file:
            file.write(content)

        print(f"File '{filename}' saved successfully.")
    except Exception as e:
        print(f"Error editing file: {str(e)}")

def view_file(filename):
    try:
        with open(filename, 'r') as file:
            content = file.read()
            print(f"Content of '{filename}':\n")
            print(content)
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    except Exception as e:
        print(f"Error viewing file: {str(e)}")

def touch_file(filename):
    try:
        with open(filename, 'w'):
            pass
        print(f"Created empty file: {filename}")
    except Exception as e:
        print(f"Error creating file: {str(e)}")

def remove_file_or_directory(target):
    try:
        if os.path.isfile(target):
            os.remove(target)
            print(f"Removed file: {target}")
        elif os.path.isdir(target):
            shutil.rmtree(target)
            print(f"Removed directory and its contents: {target}")
        else:
            print(f"File or directory not found: {target}")
    except Exception as e:
        print(f"Error removing file or directory: {str(e)}")

def suggest_commands(mistyped_command):
    available_commands = list(command_help.keys())
    suggestions = get_close_matches(mistyped_command, available_commands, n=3, cutoff=0.6)
    return suggestions

def main():
    clear_screen()
    print_warning_and_developer_info()

    while True:
        current_directory = os.getcwd()
        try:
            user_input = input(stylized_prompt(current_directory))
            if user_input.lower() == "exit":
                print("Exiting the terminal.")
                break
            elif user_input.lower() == "clear":
                clear_screen()
            elif "|" in user_input:
                commands = user_input.split("|")
                commands = [cmd.strip() for cmd in commands]
                output = execute_commands_with_pipes(commands)
                print(output)
            elif user_input.startswith("grep "):
                _, pattern = user_input.split(" ", 1)
                # Get the previous command's output from the user
                previous_output = input("Enter the output to grep: ")
                output = grep(pattern, previous_output)
                print(output)
            elif user_input.startswith("edit "):
                _, filename = user_input.split(" ", 1)
                edit_file(filename)
            elif user_input.startswith("view "):
                _, filename = user_input.split(" ", 1)
                view_file(filename)
            elif user_input.startswith("touch "):
                _, filename = user_input.split(" ", 1)
                touch_file(filename)
            elif user_input.startswith("rm "):
                _, target = user_input.split(" ", 1)
                remove_file_or_directory(target)
            elif " " in user_input:
                command, args = user_input.split(" ", 1)
                if args.strip() == "":
                    display_command_usage(command)
                elif command.lower() == "copy":
                    _, source, destination = user_input.split(" ", 2)
                    output = copy_directory(source, destination)
                    print(output)
                elif command.lower() == "python":
                    code = ""
                    while True:
                        code_line = input("... ")
                        if code_line.lower() == "end":
                            break
                        code += code_line + "\n"
                    output = execute_python_code(code)
                    print(output)
                elif command.lower() == "ls":
                    list_files_in_current_directory()
                elif command.lower() == "cd":
                    change_directory(args)
                elif command.lower() == "mkdir":
                    create_directory(args)
                elif command.lower() == "help":
                    display_help(args)
                elif command.lower() == "man":  
                    display_help(args)
                else:
                    suggested_commands = suggest_commands(command)
                    if suggested_commands:
                        print(f"Command not found: {user_input}. Did you mean one of these? {', '.join(suggested_commands)}")
                    else:
                        print("Command not found: " + user_input)
            else:
                print("Command not found: " + user_input)
        except KeyboardInterrupt:
            print("\nUse 'exit' to exit the terminal.")
            continue

if __name__ == "__main__":
    main()
