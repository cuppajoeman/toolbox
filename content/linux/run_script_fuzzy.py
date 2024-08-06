import argparse
import subprocess
import sys
import re
import curses
from pathlib import Path

def fuzzy_search(query, items):
    """Simple fuzzy matching implementation."""
    pattern = '.*'.join(re.escape(c) for c in query)
    regex = re.compile(pattern, re.IGNORECASE)
    return [item for item in items if regex.search(item)]

def select_script(stdscr, scripts):
    """Use curses to display and select a script from the list."""
    curses.curs_set(0)  # Hide the cursor
    stdscr.nodelay(1)  # Non-blocking input
    stdscr.timeout(500)  # Screen refresh rate (milliseconds)

    current_index = 0
    query = ""
    filtered_items = scripts

    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        # Display query input and key commands
        stdscr.addstr(0, 0, f"Search: {query}")
        stdscr.addstr(1, 0, "Use UP/DOWN arrow keys to navigate | ESC to cancel | ENTER to select")

        # Display filtered items
        for idx, item in enumerate(filtered_items):
            if idx == current_index:
                # Highlight the selected item
                item_str = item[:width-1]  # Ensure it fits within the width
                stdscr.addstr(idx + 2, 0, item_str, curses.A_REVERSE)
            else:
                # Normal display
                item_str = item[:width-1]  # Ensure it fits within the width
                stdscr.addstr(idx + 2, 0, item_str)

            # Check if we exceed the height of the terminal
            if idx + 2 >= height - 1:
                break

        # Get user input
        ch = stdscr.getch()

        # Key navigation and input handling
        if ch == curses.KEY_UP:
            if current_index > 0:
                current_index -= 1
        elif ch == curses.KEY_DOWN:
            if current_index < len(filtered_items) - 1:
                current_index += 1
        elif ch == curses.KEY_ENTER or ch == 10:  # ENTER key
            return filtered_items[current_index]
        elif ch == 27:  # ESC key
            return None
        elif ch in (8, 127, curses.KEY_BACKSPACE):  # BACKSPACE key
            query = query[:-1]
        elif 32 <= ch <= 126:  # Printable characters
            query += chr(ch)

        # Update filtered items
        filtered_items = fuzzy_search(query, scripts)

def main(stdscr):
    parser = argparse.ArgumentParser(
        description="Select and execute shell or Python scripts from a specified directory."
    )
    parser.add_argument(
        'root_dir',
        type=str,
        help="The root directory to search for scripts."
    )
    args = parser.parse_args()

    root_dir = Path(args.root_dir)

    if not root_dir.is_dir():
        print(f"Error: {root_dir} is not a valid directory.")
        sys.exit(1)

    # Find .sh and .py files recursively
    scripts = [str(file) for file in root_dir.rglob('*.sh')] + [str(file) for file in root_dir.rglob('*.py')]

    if not scripts:
        print("No scripts found.")
        sys.exit(1)

    executable = curses.wrapper(lambda stdscr: select_script(stdscr, scripts))

    if not executable:
        print("No script selected.")
        sys.exit(1)

    print(f"Script: {executable} selected")
    print("\n-------------------------")
    print("------SCRIPT-SOURCE------")
    print("-------------------------\n")

    with open(executable, 'r') as file:
        print(file.read())

    print("\n-------------------------")
    print("-------------------------")
    print("-------------------------")

    input_arguments = input("Now provide arguments: ").split()

    if executable.endswith('.sh'):
        interpreter = 'sh'
    elif executable.endswith('.py'):
        interpreter = 'python3'
    else:
        print("Unsupported script type.")
        sys.exit(1)

    print(f"Running: {interpreter} {executable} {' '.join(input_arguments)}")
    
    # Run the selected script
    subprocess.run([interpreter, executable] + input_arguments)

    # Exit the program safely after the subprocess completes
    print("Script execution complete. Exiting...")

if __name__ == "__main__":
    curses.wrapper(main)
