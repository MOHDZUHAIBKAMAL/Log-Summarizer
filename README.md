# Log Summarizer

A simple Python tool that reads text log files and generates a frequency summary of events.

## What It Does

- Reads any `.txt` file
- Extracts the first word from each line (treated as the event name)
- Counts occurrences of each event
- Generates a formatted summary report with frequencies and percentages

## How to Run

1. Place your log file in the same directory as the script (or have the path ready)
2. Run the program:
   ```bash
   python app.py
   ```
3. Follow the prompts:
   - Choose option `1` to run the summarizer
   - Select a log file from the list or enter a custom path
   - Choose whether to overwrite existing summary files or create a new one
4. Check the output file (default: `summary.txt`)

## Input Format

Your log file should have one entry per line. The script reads the **first word** of each line as the event name.

**Example log file (`log.txt`):**
```
UPLOAD file7.txt
LOGOUT user1
LOGIN user2
FAILED Password attempt
UPLOAD file8.txt
DOWNLOAD file9.txt
LOGOUT user2
```

## Output Format

The summary file (`summary.txt`) contains:

- Total number of entries
- Number of unique events
- Number of skipped/blank lines
- Complete frequency table sorted by count (highest to lowest)
- Percentage breakdown for each event

**Example output:**
```
============================================================
Log Events Summary
============================================================

Total entries parsed: 29
Unique events: 8
Skipped/blank lines: 3

------------------------------------------------------------
Event Frequencies (sorted by count):
------------------------------------------------------------
UPLOAD                   7 times (24.1%)
LOGIN                    6 times (20.7%)
LOGOUT                   6 times (20.7%)
DOWNLOAD                 3 times (10.3%)
ERROR                    3 times (10.3%)
FAILED                   2 times ( 6.9%)
RANDOM                   1 times ( 3.4%)
TIMEOUT                  1 times ( 3.4%)

============================================================
```

## AI Assistance Disclosure

This project used AI assistance in the following ways:
- **Generated test data**: AI helped create a sample `log.txt` file with hackathon-themed events for testing purposes
- **Code enhancement**: AI assisted in creating the `write_summary()` function to improve the formatting and readability of the summary output

## Requirements

- Python 3.6 or higher
## Notes

- Empty lines are automatically skipped and counted separately
- Event names are converted to uppercase for consistency
- The script is case-insensitive when finding `.txt` files
- Works with any plain text format where the first word represents an event type
