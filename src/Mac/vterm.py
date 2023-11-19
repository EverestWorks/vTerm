import os
import subprocess
import shutil
from pathlib import Path
import re
from difflib import get_close_matches
import pygame
import time
from tqdm import tqdm
import random

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
    "rm": "Remove a file or directory. Usage: rm filename or rm -r directory",
    "version": "Prints the terminal version",
    "celebrate": "Celebrates. What more do I need to tell you?"
}
S = "Sound"
pygame.init()
pygame.mixer.init()

tada = pygame.mixer.Sound(os.path.join(S,"tada2.wav"))
tada.set_volume(1.0)
startup = pygame.mixer.Sound(os.path.join(S,"Startup (3).wav"))
startup.set_volume(1.0)
error = pygame.mixer.Sound(os.path.join(S,"Error2.wav"))
err = pygame.mixer.SoundType(os.path.join(S, "Err.wav"))
shutdown = pygame.mixer.Sound(os.path.join(S,"Shutdown.wav"))
    

version = "vTerm 0.0.100 | MacOS"

def celebrate():
    print("yay!")
    tada.play()

def get_version_colored():
    print(f"\033[0;32m{version}\033")
    print("\033[1;34mCopyright: \033[1;36mEverestWorks @2023\033[0m\n")

def warning_colored():
    print("\033[1;31mWarning: This is a development environment, and there may be bugs.\033[0m")
    print("\033[1;34mCopyright: \033[1;36mEverest works @2023\033[0m")
    print("\033[0;37mType 'help -h' to view available commands\033[0m\n")


def stylized_prompt(current_directory):
    return f"\033[1;32m{current_directory}\033[0;35m: >> \033[0m"

def clear_screen():
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

def autocomplete_path(text, state):
    directory = os.path.dirname(text)
    matches = [str(p) for p in Path(directory).iterdir() if str(p).startswith(text)]
    return matches[state] if state < len(matches) else None

def display_help(command):
    available_commands = list(command_help.keys())
    
    if command == "-h":
        print("Available commands:")
        for cmd in available_commands:
            print(f"  - {cmd}")
        print("\nUse 'help <COMMAND>' to receive help on a specific command.")
    elif command in command_help:
        print(f"{command}:")
        print(command_help[command])
    else:
        print(f"Help for {command} not found. The command may not exist.")


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
    for i in tqdm (range (100), colour='green', desc="Booting..."):
        wtime = random.uniform(0.001, 0.05)
        time.sleep(wtime)
        pass
    clear_screen()
    warning_colored()
    startup.play()
    

    while True:
        current_directory = os.getcwd()
        try:
            user_input = input(stylized_prompt(current_directory)).strip()
            # print("Raw input:", repr(user_input))  #Print raw input for debugging
            if user_input.lower() == "exit":
                print("Shutting Down...")
                shutdown.play()
                time.sleep(0.35)
                break
            elif user_input.lower() == "version":
                get_version_colored()
            elif user_input.lower() == "celebrate":
                celebrate()
            elif user_input.lower() == "clear":
                clear_screen()
                warning_colored()
            elif "|" in user_input:
                commands = user_input.split("|")
                commands = [cmd.strip() for cmd in commands]
                output = execute_commands_with_pipes(commands)
                print(output)
            elif user_input.startswith("grep"):
                _, pattern = user_input.split(" ", 1)
                # Get the previous command's output from the user
                previous_output = input("Enter the output to grep: ")
                output = grep(pattern, previous_output)
                print(output)
            elif user_input.startswith("edit"):
                try:
                    _, filename = user_input.split(" ", 1)
                    edit_file(filename)
                except ValueError:
                    print("Argument needed. Usage: edit filename")
                    continue
            elif user_input.startswith("view"):
                try:
                    _, filename = user_input.split(" ", 1)
                    view_file(filename)
                except ValueError:
                    print("Argument needed. Usage: view filename")
                    continue
            elif user_input.startswith("touch"):
                try:
                    _, filename = user_input.split(" ", 1)
                    touch_file(filename)
                except ValueError:
                    print("Argument needed. Usage: touch filename")
                    continue
            elif user_input.startswith("rm"):
                try:
                    _, target = user_input.split(" ", 1)
                except ValueError:
                    print("Argument needed. Usage: rm file OR rm -r directory")
                    continue
                remove_file_or_directory(target)
            elif user_input.startswith("ls"):
                list_files_in_current_directory()
            elif user_input.startswith("cd"):
                try:
                    _, new_dir = user_input.split(" ", 1)
                except ValueError:
                    print("Argument needed. Usage: cd directory")
                    continue
                change_directory(new_dir)
            elif user_input.startswith("mkdir"):
                args = user_input.split()
                if len(args) > 1:
                    new_dir = args[1]
                else:
                    print("Argument needed. Usage: mkdir directory")
                    continue
                create_directory(new_dir)
            elif user_input.startswith("help"):
                args = user_input.split(" ", 1)
                if len(args) > 1:
                    display_help(args[1])
                else:
                    display_help()
            elif user_input.startswith("man"):
                args = user_input.split(" ", 1)
                if len(args) > 1:
                    display_help(args[1])
                else:
                    print("Argument needed. Usage: man command")
            elif user_input.startswith("python"):
                code = ""
                while True:
                    code_line = input("... ")
                    if code_line.lower() == "end":
                        break
                    code += code_line + "\n"
                output = execute_python_code(code)
                print(output)
            else:
                suggested_commands = suggest_commands(user_input)
                if suggested_commands:
                    print(f"Command not found: {user_input}. Did you mean one of these? {', '.join(suggested_commands)}")
                    err.play()
                else:
                    print("Command not found: " + user_input)
                    error.play()
        except KeyboardInterrupt:
            print("\nUse 'exit' to exit the terminal.")
            error.play()
            continue

if __name__ == "__main__":
    main()
