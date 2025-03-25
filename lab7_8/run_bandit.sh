# List of repository directories
REPOS=("face_recognition" "faster-whisper" "markitdown")
RESULTS_DIR="../bandit_results"


# Loop through each repository
for REPO in "${REPOS[@]}"; do
    echo "Processing repository: $REPO"
    REPO_PATH="$(pwd)/$REPO"
    REPO_RESULTS_DIR="$RESULTS_DIR/$REPO"
    
    # Verify repository exists before proceeding
    if [[ ! -d "$REPO_PATH/.git" ]]; then
        echo "Error: Repository $REPO not found or not a Git repository. Skipping."
        continue
    fi
    
    cd "$REPO_PATH" || { echo "Failed to access $REPO"; exit 1; }
    mkdir -p "$REPO_RESULTS_DIR"
    
    # Fetch last 100 non-merge commits
    git log --pretty=format:"%H" -n 100 > commits.txt
    
    # Process each commit
    while read -r commit; do
        echo "Checking out commit: $commit"
        git checkout "$commit" --quiet || { echo "Failed to checkout $commit"; continue; }
        
        # Run Bandit and save the report
        bandit -r . -f json -o "$REPO_RESULTS_DIR/bandit_report_$commit.json"
        
        echo "Saved report for commit $commit"
    done < commits.txt
    
    # Return to the main branch
    git checkout main --quiet
    cd ..

done

echo "Ran Bandit on all repositories"
