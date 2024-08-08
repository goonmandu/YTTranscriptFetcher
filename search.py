import os
import re
import sys

def find_string_in_transcripts(search_string, base_transcript_dir):
    search_results = []

    # Walk through all subdirectories and files in the base directory
    for root, dirs, files in os.walk(base_transcript_dir):
        for file in files:
            if file.endswith(".txt"):
                video_id = os.path.splitext(file)[0]
                file_path = os.path.join(root, file)

                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        # Extract the timestamp and text from the line
                        match = re.match(r'\[(\d{2}:\d{2}:\d{2})\] (.+)', line)
                        if match:
                            timestamp = match.group(1)
                            text = match.group(2)

                            # Check if the search string is in the line
                            if search_string.lower() in text.lower():
                                search_results.append((video_id, timestamp))

    return search_results

def format_timestamp_to_seconds(timestamp):
    """Convert timestamp (hh:mm:ss) to seconds."""
    hours, minutes, seconds = map(int, timestamp.split(':'))
    return hours * 3600 + minutes * 60 + seconds

def print_results(search_string, base_transcript_dir):
    results = find_string_in_transcripts(search_string, base_transcript_dir)

    if results:
        for video_id, timestamp in results:
            timestamp_seconds = format_timestamp_to_seconds(timestamp)
            timestamp_url = f"https://youtu.be/{video_id}?t={timestamp_seconds}"
            print(f"Found '{search_string}' at {timestamp_url}")
    else:
        print(f"No instances of '{search_string}' found in any transcripts.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("You must provide one keyword to search for.")
        exit(1)
    base_transcript_dir = "transcripts"
    search_string = sys.argv[1]  # Replace with the word you're searching for

    print_results(search_string, base_transcript_dir)
