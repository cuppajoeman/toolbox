#!/bin/bash

# Default parameter values
SILENCE_DURATION=0.05
NOISE_TOLERANCE=0.001
OUTPUT_DIR="./output"
MIN_DURATION=0.50
DRY_RUN=false

# Function to show help text
function show_help() {
  echo "Usage: split_on_silence.sh [options] -i input_file"
  echo ""
  echo "Options:"
  echo "  -i, --input            Specify the input audio file (required)"
  echo "  -d, --silence-duration Set silence duration threshold in seconds (default: $SILENCE_DURATION)"
  echo "  -n, --noise-tolerance  Set noise tolerance level (default: $NOISE_TOLERANCE)"
  echo "  -m, --min-duration     Set minimum duration for saving segments in seconds (default: $MIN_DURATION)"
  echo "  -o, --output-dir       Specify the output directory for split files (default: $OUTPUT_DIR)"
  echo "  --dry-run              Show what would be done without making changes"
  echo "  -h, --help             Show this help message"
  echo ""
  echo "Noise Tolerance Explanation:"
  echo "  The noise tolerance parameter sets the minimum amplitude level that"
  echo "  will be considered silence. A higher value means that the script will"
  echo "  treat low-level noise as silence. For example, a tolerance of 0.001"
  echo "  means that sounds quieter than this level will be considered silence."
  echo "  Adjusting this value can help in noisy environments to avoid splitting"
  echo "  on unwanted low-level sounds."
  exit 0
}

# Parse command-line arguments
while [[ "$1" != "" ]]; do
  case $1 in
    -i | --input )          shift
                            INPUT_FILE="$1"
                            ;;
    -d | --silence-duration) shift
                            SILENCE_DURATION="$1"
                            ;;
    -n | --noise-tolerance) shift
                            NOISE_TOLERANCE="$1"
                            ;;
    -m | --min-duration)    shift
                            MIN_DURATION="$1"
                            ;;
    -o | --output-dir )     shift
                            OUTPUT_DIR="$1"
                            ;;
    --dry-run )             DRY_RUN=true
                            ;;
    -h | --help )           show_help
                            ;;
    * )                     echo "Unknown parameter: $1"
                            show_help
                            ;;
  esac
  shift
done

# Ensure input file is specified
if [[ -z "$INPUT_FILE" ]]; then
  echo "Error: Input file must be specified!"
  show_help
fi

# Create output directory if it doesn't exist
if [[ ! -d "$OUTPUT_DIR" ]]; then
  mkdir -p "$OUTPUT_DIR"
fi

# Detect silence and gather timestamps for silence_end and silence_start
timestamps=$(ffmpeg -i "$INPUT_FILE" -af "silencedetect=n=$NOISE_TOLERANCE:d=$SILENCE_DURATION" -f null - 2>&1 | \
  awk '/silence_end:/ {print $5; getline; print $3}' | grep -E '^[0-9]+(\.[0-9]+)?$')

# Print out the detected silence end and start timestamps
echo "Detected silence end and start timestamps:"
echo "$timestamps"

# Read timestamps into an array
readarray -t time_array < <(echo "$timestamps")

# Initialize variables for splitting
file_index=1

# Function to calculate segment duration
function get_segment_duration() {
  local start=$1
  local end=$2
  echo "$end - $start" | bc
}

# Iterate through the timestamps, creating segments from silence end to the next silence start
for ((i=0; i<${#time_array[@]}-1; i+=2)); do
  silence_end="${time_array[i]}"        # End of silence
  silence_start="${time_array[i+1]}"    # Start of next silence

  # Calculate duration of the segment
  duration=$(get_segment_duration "$silence_end" "$silence_start")

  # Check if the duration meets the minimum duration requirement
  if (( $(echo "$duration >= $MIN_DURATION" | bc -l) )); then
    output_file=$(printf "%s/output_%02d.mp3" "$OUTPUT_DIR" "$file_index")

    if [[ "$DRY_RUN" == true ]]; then
      echo "Dry run: Would split from $silence_end to $silence_start into $output_file (Duration: $duration seconds)"
    else
      ffmpeg -i "$INPUT_FILE" -ss "$silence_end" -to "$silence_start" -c copy "$output_file"
      echo "Saved segment: $output_file (Duration: $duration seconds)"
    fi

    file_index=$((file_index + 1))
  else
    echo "Skipped segment from $silence_end to $silence_start due to short duration ($duration seconds)"
  fi
done

# Handle the last segment if necessary (from last silence end to end of file)
if [[ -n "${time_array[-1]}" ]]; then
  last_silence_end="${time_array[-1]}"
  output_file=$(printf "%s/output_%02d.mp3" "$OUTPUT_DIR" "$file_index")

  # Get the duration of the last segment (end of file)
  last_duration=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$INPUT_FILE")
  segment_duration=$(get_segment_duration "$last_silence_end" "$last_duration")

  if (( $(echo "$segment_duration >= $MIN_DURATION" | bc -l) )); then
    if [[ "$DRY_RUN" == true ]]; then
      echo "Dry run: Would split from $last_silence_end to end of file into $output_file (Duration: $segment_duration seconds)"
    else
      ffmpeg -i "$INPUT_FILE" -ss "$last_silence_end" -c copy "$output_file"
      echo "Saved last segment: $output_file (Duration: $segment_duration seconds)"
    fi
  else
    echo "Skipped last segment due to short duration ($segment_duration seconds)"
  fi
fi

echo "Splitting complete."
