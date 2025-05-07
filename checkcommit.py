from github import Github
from dotenv import load_dotenv
import os
import subprocess
from git import Repo
 
# Load environment variables from .env file
load_dotenv()

GIT_TOKEN = os.getenv("GIT_TOKEN")
BRANCH = os.getenv("BRANCH")
commit_file = 'latest_commit.txt'

# Auth the Repo
github_access = Github(GIT_TOKEN)

# Check the GitHub user info
user = github_access.get_user()
print("Authenticated as:", user.login)

# Get Repo Access
repo = github_access.get_repo("thirumalai-py/ci-cd-html")
# Get repository details
print(repo.full_name)
print(repo.description)

# Current Repo Path
repo_path = os.getcwd()
repo_src = Repo(repo_path)

# Get commits
commits = repo.get_commits(sha=BRANCH)

# Get the latest commit
latest_commit = commits[0]
recent_commit = latest_commit.sha
print("Latest Commit: ", recent_commit)


# Get the last commit from the file
def update_last_commit(recent_commit):
    with open(commit_file, 'w') as file:
        file.write(recent_commit)

# Read the last commit from the file
def read_last_commit():
    if os.path.exists(commit_file):
        with open(commit_file, 'r') as file:
            return file.readline().strip()
    return None

if os.path.exists(commit_file):
    last_commit = read_last_commit()
    if recent_commit==last_commit:
        print("No new commits found")
    else:
        # If the file doesn't exist, create it and write the current commit
        script_dir = os.path.dirname(os.path.abspath(__file__))
        deploy_script_path = os.path.join(script_dir, "deploy.sh")

        subprocess.run(["bash", deploy_script_path], check=True)
        
        print("Git pull completed successfully!")
        # Save the last commit
        with open(commit_file, 'w') as file:
            file.write(recent_commit)
else:
    # If the file doesn't exist, create it and write the current commit
    script_dir = os.path.dirname(os.path.abspath(__file__))
    deploy_script_path = os.path.join(script_dir, "deploy.sh")

    subprocess.run(["bash", deploy_script_path], check=True)

    # Save the last commit
    update_last_commit(recent_commit)






