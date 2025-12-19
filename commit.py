import subprocess

#chatgpt

def run_command(command):
    """Run a shell command and print output if there is any."""
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)

def main():
    # Stage all changes (including deletions)
    run_command("git add -A")
    
    # Ask for commit message
    commit_message = input("Enter commit message: ").strip()
    if not commit_message:
        print("Commit message cannot be empty.")
        return
    
    # Commit changes
    run_command(f'git commit -m "{commit_message}"')
    
    # Push changes to the current branch
    run_command("git push")

if __name__ == "__main__":
    main()
