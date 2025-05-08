#!/bin/bash

if [ -f .env ]; then
    source .env
else
    echo "No .env file found"
fi

current_date=$(date '+%Y-%m-%d %H:%M:%S')
commit_file="latest_commit.txt"
folder_path=$FOLDER_PATH

log_file="$folder_path/deploy_log.log"


echo "Current Branch: $BRANCH"

# Get the latest commit id from the remote branch
latest_commit=$(git ls-remote origin $BRANCH | awk '{print $1}')
echo "Lastest Commit id: $latest_commit"

# Get the saved commit id from the file
saved_commit=$(cat "$commit_file" | head -n 1)
echo "Saved Commit id:  $saved_commit"

if [[ "$latest_commit" == "$saved_commit" ]]; then
    echo "No new commit found"
else
    echo "New commit found"
    git pull
    # Get the new commit id from pulled changes
    new_commit_id=$(git log -1 --pretty=format:"%H")
    commit_message=$(git log -1 --pretty=format:"%s")
    # Update the commit file with the new commit id
    echo "====== Deployment Done on - $current_date ======= " >> "$log_file"
    echo "Latest Commit id: $new_commit_id" >> "$log_file"
    echo "Commit Message  : $commit_message" >> "$log_file"
    echo "----------------------------------------------------" >> "$log_file"
    echo "$new_commit_id" > "$commit_file" # Need to echo only then > will save the file 
fi