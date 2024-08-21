function ranger {
    # Set the Internal Field Separator (IFS) to handle whitespace correctly when parsing output.
    local IFS=$'\t\n'

    # Create a temporary file to store the directory path selected in ranger.
    local tempfile="$(mktemp -t tmp.XXXXXX)"

    # Create an array with the command to run ranger. 
    # --cmd="map Q chain shell echo %d > "$tempfile"; quitall"
    # This maps the key 'Q' in ranger to a sequence of actions:
    # 1. 'map Q': Binds the 'Q' key to a custom action.
    # 2. 'chain': Executes multiple commands in sequence.
    # 3. 'shell echo %d > "$tempfile"':
    #    - 'shell': Allows running a shell command from within ranger.
    #    - 'echo %d': Outputs the current directory path (represented by '%d').
    #    - '> "$tempfile"': Redirects the output to the temporary file, saving the directory path.
    # 4. 'quitall': Exits ranger after saving the directory path.
    local ranger_cmd=(
        command
        ranger
        --cmd="map Q chain shell echo %d > "$tempfile"; quitall"
    )

    # Execute the ranger command with any passed arguments.
    ${ranger_cmd[@]} "$@"

    # If the tempfile exists and its content (the directory path) is different from the current directory,
    # change to the directory stored in the tempfile.
    if [[ -f "$tempfile" ]] && [[ "$(cat -- "$tempfile")" != "$PWD" ]]; then
        cd -- "$(cat "$tempfile")" || return
    fi

    # Remove the temporary file.
    command rm -f -- "$tempfile" 2>/dev/null
}
