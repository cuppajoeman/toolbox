#include <stdio.h>
#include <filesystem>
#include <iostream>

namespace fs = std::filesystem;

/**
 * precondition:
 *  the build directory is in the root of the project
 *  argv[0] contains the path to the executable (which is in the build directory)
 *
 * note:
 *  https://stackoverflow.com/a/2051031/6660685 
 * 
 */
int main(int argc, char *argv[]){

    char *executable_path_string = argv[0];
    const fs::path executable_path = executable_path_string;
    const fs::path absolute_executable_path = fs::absolute(executable_path);

    const fs::path project_root = absolute_executable_path.parent_path();

    std::cout << "parent path is: " << project_root << "\n";
}
