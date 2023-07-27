#!/bin/bash
script_file=$1.sh

touch $script_file
echo "#!/bin/bash" > $script_file
chmod +x $script_file

nvim $script_file
