import os
import json
import pandas as pd

BANDIT_REPORTS_FOLDER = "bandit_results"

def extract_totals(data):
    """Extracts confidence and severity totals from Bandit report data."""
    totals = data.get("metrics", {}).get("_totals", {})
    return {
        "confidence_high": totals.get("CONFIDENCE.HIGH", 0),
        "confidence_medium": totals.get("CONFIDENCE.MEDIUM", 0),
        "confidence_low": totals.get("CONFIDENCE.LOW", 0),
        "severity_high": totals.get("SEVERITY.HIGH", 0),
        "severity_medium": totals.get("SEVERITY.MEDIUM", 0),
        "severity_low": totals.get("SEVERITY.LOW", 0),
    }

def extract_unique_cwes(data):
    """Extracts unique CWE IDs from the Bandit report results."""
    return ", ".join(
        {str(issue["issue_cwe"]["id"]) for issue in data.get("results", []) if "issue_cwe" in issue and "id" in issue["issue_cwe"]}
    )

def process_report(repo_path, report_file):
    """Processes a single JSON Bandit report and returns extracted data."""
    commit_id = report_file.replace("bandit_report_", "").replace(".json", "")
    report_path = os.path.join(repo_path, report_file)
    
    with open(report_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    totals = extract_totals(data)
    totals["unique_cwes"] = extract_unique_cwes(data)
    
    return {"commit_id": commit_id, **totals}

def process_repository(repo):
    """Processes all Bandit reports in a repository folder and saves results as CSV."""
    repo_path = os.path.join(BANDIT_REPORTS_FOLDER, repo)
    
    if not os.path.isdir(repo_path):
        return
    
    results = [process_report(repo_path, file) for file in sorted(os.listdir(repo_path)) if file.endswith(".json")]
    df = pd.DataFrame(results)
    df = df[["commit_id", "confidence_high", "confidence_medium", "confidence_low", "severity_high", "severity_medium", "severity_low", "unique_cwes"]]  # Ensure commit_id is the first column
    csv_filename = os.path.join(BANDIT_REPORTS_FOLDER, f"{repo}_bandit_analysis.csv")
    df.to_csv(csv_filename, index=False)
    print(f"Analysis completed for {repo}. Results saved to {csv_filename}")

def main():
    """Main function to iterate over all repositories and process Bandit reports."""
    for repo in os.listdir(BANDIT_REPORTS_FOLDER):
        process_repository(repo)

if __name__ == "__main__":
    main()
