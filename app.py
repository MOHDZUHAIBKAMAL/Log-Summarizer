import os

DEFAULT_SUMMARY = "summary.txt"

# Grab the first word from each line in the log file
def read_log(filepath):
    event_list = []
    skipped_lines = 0

    try:
        with open(filepath, "r", encoding="utf-8") as reader:
            for raw in reader:
                line = raw.strip()
                if not line:
                    skipped_lines += 1
                    continue
                parts = line.split()
                if not parts:
                    skipped_lines += 1
                    continue
                event_list.append(parts[0].upper())

    except FileNotFoundError:
        print(f"Couldn't find the file: {filepath}")
        return [], 0
    except PermissionError:
        print(f"No permission to read the file: {filepath}")
        return [], 0
    except Exception as err:
        print(f"Something went wrong reading '{filepath}': {str(err)}")
        return [], 0

    return event_list, skipped_lines


# Count how many times each event appears
def build_summary(events, blanks):
    freq = {}
    for event in events:
        freq[event] = freq.get(event, 0) + 1
    
    sorted_events = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    
    return {
        "total": len(events),
        "unique": len(freq),
        "sorted_events": sorted_events,
        "ignored": blanks
    }


# Write the summary to a text file
def write_summary(summary_data, out_file):
    try:
        with open(out_file, "w", encoding="utf-8") as report:
            report.write("=" * 60 + "\n")
            report.write("Log Events Summary\n")
            report.write("=" * 60 + "\n\n")

            report.write(f"Total entries parsed: {summary_data['total']}\n")
            report.write(f"Unique events: {summary_data['unique']}\n")
            report.write(f"Skipped/blank lines: {summary_data['ignored']}\n\n")

            report.write("-" * 60 + "\n")
            report.write("Event Frequencies (sorted by count):\n")
            report.write("-" * 60 + "\n")

            if summary_data['sorted_events']:
                for evt, cnt in summary_data['sorted_events']:
                    pct = (cnt / summary_data['total'] * 100) if summary_data['total'] else 0
                    report.write(f"{evt:20} {cnt:5} times ({pct:4.1f}%)\n")
            else:
                report.write("No events found.\n")

            report.write("\n" + "=" * 60 + "\n")
        return True
    except Exception as err:
        print(f"Couldn't write the summary: {str(err)}")
        return False


# Ask what to do if the output file already exists
def choose_summary_filename(default_name):
    if not os.path.exists(default_name):
        return default_name

    print(f"\nFile '{default_name}' already exists.")
    print("1. Overwrite")
    print("2. Choose new name")
    print("3. Cancel")

    while True:
        choice = input("Enter choice: ").strip()
        if choice == "1":
            return default_name
        elif choice == "2":
            new_name = input("New filename (.txt): ").strip()
            if not new_name:
                continue
            if not new_name.endswith('.txt'):
                new_name += ".txt"
            return new_name
        elif choice == "3":
            return None
        else:
            print("Invalid choice. Pick 1, 2, or 3.")


# Look for text files in the current folder
def find_log_files():
    try:
        return sorted(f for f in os.listdir('.') 
                     if os.path.isfile(f) and f.lower().endswith(('.txt')))
    except:
        return []


# Let the user pick a file from the list or type a path
def select_file(log_list):
    if not log_list:
        path = input("No logs found. Enter path manually (or blank to cancel): ").strip()
        return path if path else None

    print("\nAvailable logs:")
    for i, f in enumerate(log_list, 1):
        print(f"{i}. {f}")

    choice = input("Pick file number or name: ").strip()
    if not choice:
        return None
    if choice.isdigit() and 1 <= int(choice) <= len(log_list):
        return log_list[int(choice) - 1]
    elif choice in log_list:
        return choice
    else:
        print("Invalid selection.")
        return None


# Show the main menu options
def menu():
    print("\n" + "=" * 60)
    print("Log File Analyzer")
    print("=" * 60)
    print("1. Run log summarizer")
    print("2. Quit")
    return input("Your pick: ").strip()


def main():
    print("\nWelcome to the Log Summarizer!")

    while True:
        option = menu()
        if option == "1":
            logs = find_log_files()
            selected = select_file(logs)
            if not selected:
                print("Cancelled.")
                continue

            print(f"\nReading from: {selected}")
            evts, skips = read_log(selected)

            if not evts:
                print("No valid data to process.")
                continue

            result = build_summary(evts, skips)
            outfile = choose_summary_filename(DEFAULT_SUMMARY)

            if not outfile:
                print("No output file selected. Skipping.")
                continue

            print(f"\nWriting results to: {outfile}")
            success = write_summary(result, outfile)

            if success:
                print("Done! Check the report for details.")
        elif option == "2":
            print("Goodbye!")
            break
        else:
            print("Try again? Pick 1 or 2.")


if __name__ == "__main__":
    main()