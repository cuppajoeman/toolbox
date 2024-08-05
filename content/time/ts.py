import time
import argparse
import threading

def timer(seconds):
    """
    Sets a timer for a specified number of seconds and then prints a message when time is up.
    """
    print(f"Timer set for {seconds} seconds.")
    time.sleep(seconds)
    print("Time's up!")

def stopwatch():
    """
    Starts a stopwatch that displays elapsed time. It stops when the user presses Enter.
    """
    def input_thread():
        """
        Waits for the user to press Enter and then sets the stop_event to signal the main thread to stop.
        """
        input()  # Waits for the user to press Enter
        nonlocal stop_event
        stop_event.set()  # Signal the main thread to stop the stopwatch

    print("Stopwatch started. Press Enter to stop...")
    
    # Create an event object to signal when the stopwatch should stop
    stop_event = threading.Event()

    # Start a separate thread to handle user input
    thread = threading.Thread(target=input_thread)
    thread.start()
    
    start_time = time.time()
    
    # Main loop to update and display elapsed time
    while not stop_event.is_set():
        elapsed_time = time.time() - start_time
        minutes, seconds = divmod(elapsed_time, 60)
        hours, minutes = divmod(minutes, 60)
        formatted_time = f"\rElapsed time: {int(hours):02}:{int(minutes):02}:{seconds:05.2f}"
        print(formatted_time, end="")
        time.sleep(0.1)  # Update every 0.1 seconds
    
    thread.join()  # Wait for the input thread to finish
    print("Stopwatch stopped.")

def main():
    """
    Parses command-line arguments and calls the appropriate function based on the user's input.
    """
    parser = argparse.ArgumentParser(description="A simple timer and stopwatch application.")
    
    subparsers = parser.add_subparsers(dest="command")

    timer_parser = subparsers.add_parser("timer", help="Set a timer for a specified number of seconds.")
    timer_parser.add_argument("seconds", type=int, help="The number of seconds for the timer.")

    stopwatch_parser = subparsers.add_parser("stopwatch", help="Start a stopwatch.")

    args = parser.parse_args()

    if args.command == "timer":
        timer(args.seconds)
    elif args.command == "stopwatch":
        stopwatch()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
