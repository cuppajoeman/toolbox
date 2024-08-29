class Command:
    def __init__(self, prompt, help_info, is_required=False):
        self.prompt = prompt
        self.help_info = help_info
        self.is_required = is_required

    def get_input(self):
        while True:
            user_input = input(f"{self.prompt} (type 'help' for more info): ").strip()
            if user_input.lower() == "help":
                self.print_help()
                continue
            if not self.is_required and user_input == "":
                return None
            if self.is_required and user_input == "":
                print("This field is required. Please enter a value.")
                continue
            return user_input

    def print_help(self):
        print(self.help_info)


def format_commit_message(
    commit_type, scope, description, detailed_message, breaking_change, issue_reference
):
    commit_message = f"{commit_type}"
    if scope:
        commit_message += f"({scope})"
    commit_message += f": {description}"

    if detailed_message:
        commit_message += f"\n\n{detailed_message}"

    if breaking_change:
        commit_message += f"\n\nBREAKING CHANGE: {breaking_change}"

    if issue_reference:
        commit_message += f"\n\nCloses: {issue_reference}"

    return commit_message


def main():
    print("Conventional Commits Interactive Helper")

    # Define prompts and help information in tuples
    command_specs = [
        (
            "Select the type of change you are committing",
            "\nCommit Types Descriptions:\n"
            + "\nfeat - A new feature"
            + "\nfix - A bug fix"
            + "\ndocs - Documentation only changes"
            + "\nstyle - Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc.)"
            + "\nrefactor - A code change that neither fixes a bug nor adds a feature"
            + "\nperf - A code change that improves performance"
            + "\ntest - Adding missing tests or correcting existing tests"
            + "\nbuild - Changes that affect the build system or external dependencies (example scopes: gulp, broccoli, npm)"
            + "\nci - Changes to our CI configuration files and scripts (example scopes: Travis, Circle, BrowserStack, SauceLabs)"
            + "\nchore - Other changes that don’t modify src or test files"
            + "\nrevert - Reverts a previous commit",
        ),
        (
            "Enter the scope of the change (optional, leave empty to skip)",
            "\nScope represents a specific aspect of the code that your commit affects. It's a way to provide additional context about what part of the codebase is being changed."
            + "\nFor example, if you're working on a system and one of its subsystems has a name, that could be a good choice for the scope."
            + "\nIn a multiplayer game, the scope might be 'networking' if you're working on the networking subsystem."
            + "\nIn another context, such as a compiler or interpreter, the scope might be 'parser' if you're making changes to the code that parses input.",
        ),
        (
            "Enter a short description of the change",
            "\nThis is a brief summary of the change being made. It should be concise and informative, giving a clear idea of what the commit is about.",
            True,
        ),
        (
            "Enter a longer description of the change (optional, leave empty to skip)",
            "\nThis is an extended description that can provide additional details about the change, such as why the change was made or any additional context that might be useful.",
        ),
        (
            "Does this commit introduce breaking changes? (y/n)",
            "\nA breaking change is a modification that causes existing functionality to break or requires changes to be made in dependent systems. If this commit introduces such changes, provide a description.",
        ),
        (
            "Reference any issues this commit closes (optional, leave empty to skip)",
            "\nIf this commit resolves an issue or bug, you can reference it here. Typically, this would be the issue number or ID from your project's issue tracker.",
        ),
    ]

    # Create Command instances using a loop
    commands = [
        Command(
            prompt=spec[0],
            help_info=spec[1],
            is_required=spec[2] if len(spec) > 2 else False,
        )
        for spec in command_specs
    ]

    # Get commit type input from the first command
    commit_types = {
        "feat": "A new feature",
        "fix": "A bug fix",
        "docs": "Documentation only changes",
        "style": "Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc.)",
        "refactor": "A code change that neither fixes a bug nor adds a feature",
        "perf": "A code change that improves performance",
        "test": "Adding missing tests or correcting existing tests",
        "build": "Changes that affect the build system or external dependencies (example scopes: gulp, broccoli, npm)",
        "ci": "Changes to our CI configuration files and scripts (example scopes: Travis, Circle, BrowserStack, SauceLabs)",
        "chore": "Other changes that don’t modify src or test files",
        "revert": "Reverts a previous commit",
    }

    print("Select the type of change you are committing:")
    for i, (commit_type, description) in enumerate(commit_types.items(), 1):
        print(f"{i}. {commit_type} - {description}")

    type_choice = input("Enter the number corresponding to your choice: ").strip()
    if type_choice.lower() == "help":
        print("\nCommit Types Descriptions:")
        for commit_type, description in commit_types.items():
            print(f"{commit_type} - {description}")
        type_choice = input(
            "\nNow, enter the number corresponding to your choice: "
        ).strip()

    commit_type = list(commit_types.keys())[int(type_choice) - 1]

    # Get user inputs for the rest of the fields
    scope = commands[1].get_input()
    description = commands[2].get_input()
    detailed_message = commands[3].get_input()
    breaking_change = commands[4].get_input()
    issue_reference = commands[5].get_input()

    if breaking_change == "y":
        breaking_change_description = input("Describe the breaking changes: ").strip()
        breaking_change = breaking_change_description

    # Format and print the commit message
    commit_message = format_commit_message(
        commit_type,
        scope,
        description,
        detailed_message,
        breaking_change,
        issue_reference,
    )

    print("\nGenerated Commit Message:\n")
    print(commit_message)
    print("\nReady to use this commit message?")


if __name__ == "__main__":
    main()
