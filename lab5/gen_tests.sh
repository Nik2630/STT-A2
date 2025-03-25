#!/bin/bash

# Ensure script is executed in the project root
if [ ! -f "coverage_report.txt" ]; then
    echo "Error: coverage_report.txt not found! Run coverage analysis first."
    exit 1
fi

echo "Extracting modules with less than 100% coverage..."
grep -E "algorithms/.*\.py" coverage_report.txt | awk '$NF != "100%" {print $1}' | sed 's|/|.|g' | sed 's|.py$||' > uncovered_modules.txt

# Check if there are uncovered modules
if [ ! -s uncovered_modules.txt ]; then
    echo "All files have 100% coverage. No test generation required."
    exit 0
fi

echo "Generating tests for uncovered modules..."
export PYNGUIN_DANGER_AWARE=True
cat uncovered_modules.txt | parallel -j4 "pynguin --project-path=. --module-name={} --output-path=generated_tests"

echo "Organizing generated test files..."
# Move all generated test files to the main directory
find generated_tests -type f -name "*.py" -exec mv {} generated_tests/ \;
# Remove empty directories
find generated_tests -type d -empty -delete

