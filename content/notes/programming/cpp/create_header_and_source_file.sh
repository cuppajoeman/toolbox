#!/bin/bash

# Function to create C++ header and source files with include guards and an include directive
create_header_and_source_file() {
    # Prompt for the filename
    read -p "Enter the filename (without extension): " filename

    # Generate header file
    header_file="${filename}.hpp"
    source_file="${filename}.cpp"
    include_guard=$(echo "${filename}_hpp" | tr '[:lower:]' '[:upper:]')

    # Create header file
    echo "#ifndef ${include_guard}" > "$header_file"
    echo "#define ${include_guard}" >> "$header_file"
    echo "" >> "$header_file"
    echo "// Your header code here" >> "$header_file"
    echo "" >> "$header_file"
    echo "#endif // ${include_guard}" >> "$header_file"

    # Create source file
    echo "#include \"${header_file}\"" > "$source_file"
    echo "" >> "$source_file"
    echo "// Your source code here" >> "$source_file"

    echo "Files '${header_file}' and '${source_file}' have been generated."
}

# Run the function
create_header_and_source_file
