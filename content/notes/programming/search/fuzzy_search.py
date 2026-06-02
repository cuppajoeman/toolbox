import curses
import re

def fuzzy_search(query, items):
    # Simple fuzzy matching implementation
    pattern = '.*'.join(re.escape(c) for c in query)
    regex = re.compile(pattern, re.IGNORECASE)
    return [item for item in items if regex.search(item)]

def main(stdscr):
    curses.curs_set(0)  # Hide the cursor
    stdscr.nodelay(1)  # Non-blocking input
    stdscr.timeout(500)  # Screen refresh rate (milliseconds)

    # Sample data
    items = [
        "apple", "banana", "grape", "orange", "strawberry", "blueberry", "kiwi", "pineapple"
    ]
    current_index = 0
    query = ""
    filtered_items = items

    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        # Display query input
        stdscr.addstr(0, 0, f"Search: {query}")

        # Display filtered items
        for idx, item in enumerate(filtered_items):
            if idx == current_index:
                stdscr.addstr(idx + 1, 0, item, curses.A_REVERSE)
            else:
                stdscr.addstr(idx + 1, 0, item)

        # Get user input
        ch = stdscr.getch()

        if ch == curses.KEY_UP:
            if current_index > 0:
                current_index -= 1
        elif ch == curses.KEY_DOWN:
            if current_index < len(filtered_items) - 1:
                current_index += 1
        elif ch == 10:  # Enter key
            break
        elif ch == 27:  # ESC key
            return
        elif ch in (8, 127, curses.KEY_BACKSPACE):  # Backspace key
            query = query[:-1]
        elif 32 <= ch <= 126:  # Printable characters
            query += chr(ch)

        # Update filtered items
        filtered_items = fuzzy_search(query, items)

    # Final result or action
    stdscr.addstr(height - 1, 0, f"Selected: {filtered_items[current_index]}")
    stdscr.refresh()
    stdscr.getch()  # Wait for any key before exiting

curses.wrapper(main)
