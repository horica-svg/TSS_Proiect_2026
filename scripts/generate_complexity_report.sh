#!/bin/bash
# Script to generate cyclomatic complexity report using radon

REPORT_FILE="docs/complexity_report.md"

echo "# Cyclomatic Complexity Report" > $REPORT_FILE
echo "Generated on: $(date)" >> $REPORT_FILE
echo "" >> $REPORT_FILE
echo "## Summary" >> $REPORT_FILE
echo "\`\`\`" >> $REPORT_FILE
radon cc App/Tax_Calculator.py -s >> $REPORT_FILE
echo "\`\`\`" >> $REPORT_FILE

echo "Report generated in $REPORT_FILE"
