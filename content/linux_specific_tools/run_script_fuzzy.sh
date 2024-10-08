#!/bin/bash

# Script Documentation
print_help() {
    cat << EOF
Usage: $(basename "$0") DIRECTORY [OPTIONS]

This script allows you to select a shell or Python script from the specified 
directory, view its content, and execute it with user-provided arguments. 

Arguments:
  DIRECTORY         The path to the directory containing the scripts.

Options:
  -h, --help        Show this help message and exit
  -p, --print       Print the source of the selected script before execution
  -c, --copy        Copy the selected script and arguments to the clipboard

Example:
  $(basename "$0") /path/to/scripts -p

EOF
}

# Check if fzf and xclip are installed
if ! command -v fzf &> /dev/null; then
    echo "fzf is not available on this system, please install it first"
    exit 1
fi

if ! command -v xclip &> /dev/null; then
    echo "xclip is not available on this system, please install it first"
    exit 1
fi

# Parse command-line options
print_source=false
copy_to_clipboard=false

while [[ "$1" =~ ^- ]]; do
    case "$1" in
        -h|--help)
            print_help
            exit 0
            ;;
        -p|--print)
            print_source=true
            shift
            ;;
        -c|--copy)
            copy_to_clipboard=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            print_help
            exit 1
            ;;
    esac
done

# Check for the required DIRECTORY argument
if [[ -z "$1" ]]; then
    echo "Error: DIRECTORY argument is required."
    print_help
    exit 1
fi

# Verify that the provided DIRECTORY exists
scripts_dir="$1"
if [[ ! -d "$scripts_dir" ]]; then
    echo "Error: The directory '$scripts_dir' does not exist."
    exit 1
fi

# Function to run a script with user-defined arguments
run_script() {
    local script="$1"

    while true; do
        echo "Script: $script selected"

        if $print_source; then
            echo
            echo "-------------------------"
            echo "------SCRIPT-SOURCE------"
            echo "-------------------------"
            echo
            cat "$script"
            echo
            echo "-------------------------"
            echo "-------------------------"
            echo "-------------------------"
        fi

        # Prompt for arguments
        echo "Now provide arguments (use quotes for multi-word arguments or press Enter to use no arguments)."
        echo "Note: Adding '&' at the end will run the process in the background and won't be parsed as an argument."
        read -r input_arguments_line

        # Check if the last argument is "&"
        if [[ "$input_arguments_line" =~ \&$ ]]; then
            run_in_background=true
            input_arguments_line="${input_arguments_line%&}"
        else
            run_in_background=false
        fi

        # Use `eval` to correctly parse the arguments, handling quoted strings
        eval "input_arguments=($input_arguments_line)"

        # Determine the interpreter based on file extension
        case "$script" in
            *.sh)
                interpreter="sh"
                ;;
            *.py)
                interpreter="python3"
                ;;
            *)
                echo "Unsupported script type: $script"
                exit 1
                ;;
        esac

        # Prepare the command to be executed
        command_to_run="$interpreter \"$script\" ${input_arguments[@]}"

        if $copy_to_clipboard; then
            echo "$command_to_run" | xclip -selection clipboard
            echo "Command copied to clipboard: $command_to_run"
        fi

        # Execute the script
        if $run_in_background; then
            echo "Running in background: $command_to_run"
            nohup $interpreter "$script" "${input_arguments[@]}" &>/dev/null &
        else
            echo "Executing: $command_to_run"
            if $interpreter "$script" "${input_arguments[@]}"; then
                echo -e "\e[1;32mCommand executed successfully!\e[0m"
            else
                echo -e "\e[1;31mCommand execution failed!\e[0m"
            fi
        fi

        # Ask if the user wants to run the same script with different arguments
        echo "Press Enter to run the same script again with different arguments, type 'ano' to select a different script, or type 'exit' to quit."
        read -r user_input
        if [[ "$user_input" == "exit" ]]; then
            echo "Exiting..."
            exit 0
        elif [[ "$user_input" == "ano" ]]; then
            return 0  # Return to the main loop to select a different script
        elif [[ -z "$user_input" ]]; then
            continue  # Run the same script with different arguments
        fi
    done
}

# Main loop to allow running multiple scripts
while true; do
    # Find and select a script (shell or Python)
    executable=$(find "$scripts_dir" -name "*.sh" -o -name "*.py" | fzf)

    if [[ -z "$executable" ]]; then
        echo "No script selected, exiting..."
        exit 1
    fi

    # Run the selected script
    run_script "$executable"

    # Ask if the user wants to run another script
    echo "Do you want to run another script? (type 'done' to exit)"
    read -r user_input
    if [[ "$user_input" == "done" ]]; then
        echo "Exiting..."
        exit 0
    fi
done
