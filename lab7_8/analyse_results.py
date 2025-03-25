import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

RESULTS_DIR = "bandit_results"

def analyze_rq1(repo_name, df):
    """RQ1: When are high severity vulnerabilities introduced and fixed?"""
    print(f"\n--- RQ1 Analysis for {repo_name} ---")
 
    df['commit_index'] = range(len(df), 0, -1) # Add commit index for timeline plotting (reverse order)

    plt.figure(figsize=(12, 6))
    sns.lineplot(x='commit_index', y='severity_high', data=df)
    plt.title(f'RQ1: High Severity Vulnerabilities Over Commits - {repo_name}')
    plt.xlabel('Commit (Recent -> Older)')
    plt.ylabel('Number of High Severity Vulnerabilities')
    plt.grid(True)
    plot_filename = os.path.join(RESULTS_DIR, f"{repo_name}_rq1_plot.png")
    plt.savefig(plot_filename)
    plt.show() # Or plt.savefig(plot_filename) to save instead of showing

    # Basic analysis - find commits with high severity issues
    high_severity_commits = df[df['severity_high'] > 0]
    if not high_severity_commits.empty:
        print("\nCommits with High Severity Vulnerabilities:")
        print(high_severity_commits[['commit_id', 'severity_high']])
    else:
        print("\nNo high severity vulnerabilities found in the analyzed commits.")

    print(f"Results: Plot saved to {plot_filename} and commits with high severity issues listed above.")
    

def analyze_rq2(repo_name, df):
    """RQ2: Do vulnerabilities of different severities have the same pattern?"""
    print(f"\n--- RQ2 Analysis for {repo_name} ---")
    
    df['commit_index'] = range(len(df), 0, -1)

    plt.figure(figsize=(12, 6))
    sns.lineplot(x='commit_index', y='severity_high', data=df, label='High Severity')
    sns.lineplot(x='commit_index', y='severity_medium', data=df, label='Medium Severity')
    sns.lineplot(x='commit_index', y='severity_low', data=df, label='Low Severity')
    plt.title(f'RQ2: Vulnerability Severity Patterns Over Commits - {repo_name}')
    plt.xlabel('Commit (Recent -> Older)')
    plt.ylabel('Number of Vulnerabilities')
    plt.legend()
    plt.grid(True)
    plot_filename = os.path.join(RESULTS_DIR, f"{repo_name}_rq2_plot.png")
    plt.savefig(plot_filename)
    plt.show() # Or plt.savefig(plot_filename)

    print(f"Results: Plot saved to {plot_filename}.")
    

def analyze_rq3(all_repo_dfs):
    """RQ3: Which CWEs are the most frequent across different OSS repositories?"""
    print("\n--- RQ3 Analysis Across All Repositories ---")
    
    all_cwes = []
    for repo_name, df in all_repo_dfs.items():
        for cwe_string in df['unique_cwes'].dropna(): # Handle NaN values
            cwes = [cwe.strip() for cwe in cwe_string.split(',')] # Split comma-separated CWEs
            all_cwes.extend(cwes)

    cwe_counts = pd.Series(all_cwes).value_counts().head(10) # Count CWE occurrences, get top 10

    print("\nResults: Top 10 Most Frequent CWEs Across All Repositories:")
    print(cwe_counts)

    plt.figure(figsize=(10, 6))
    cwe_counts.plot(kind='bar')
    plt.title('RQ3: Top 10 Most Frequent CWEs Across Repositories')
    plt.xlabel('CWE ID')
    plt.ylabel('Frequency')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plot_filename = os.path.join(RESULTS_DIR, "rq3_cwe_frequency_plot.png")
    plt.savefig(plot_filename)
    plt.show() # Or plt.savefig(plot_filename)

    print(f"Plot saved to {plot_filename}.")
  

def main():
    repo_names = [repo for repo in os.listdir(RESULTS_DIR) if os.path.isdir(os.path.join(RESULTS_DIR, repo))] # Get repo names from result folders
    repo_dfs = {}
    for repo_name in repo_names:
        csv_file = os.path.join(RESULTS_DIR, f"{repo_name}_bandit_analysis.csv")
        if os.path.exists(csv_file):
            repo_dfs[repo_name] = pd.read_csv(csv_file)
        else:
            print(f"CSV file not found for {repo_name}. Skipping.")

    if not repo_dfs:
        print("No CSV files found to analyze. Please run tables.py first.")
        return

    for repo_name, df in repo_dfs.items():
        analyze_rq1(repo_name, df)
        analyze_rq2(repo_name, df)

    analyze_rq3(repo_dfs)


if __name__ == "__main__":
    main()