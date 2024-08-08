# YTTranscriptFetcher
Downloads the transcripts for all public videos of a YouTube channel, then searches them for a specific keyword.

Keyword search is performed across all channels.

All code in this repository was generated by ChatGPT using GPT-4o, then fine-tuned by me.  
You can find the full license (MIT) in the `LICENSE` file.

Please don't abuse my API key. Pretty please.

## Usage
Tested with Python 3.12.  
Probably should work with Python 3.8 or newer though.
```bash
# Install dependencies
pip3 install -r requirements.txt

# This saves all transcripts of a channel to a directory called "transcripts".
# The repository already has all transcripts for zy0xarchives saved.
# If that's all you need, you can skip running this command.
# You can get the channel ID with the channel handle from this website:
# https://www.streamweasels.com/tools/youtube-channel-id-and-user-id-convertor/
python3 fetcher.py channel_id

# This searches the saved transcript files for a specific keyword
# and prints the video timestamp where it is found.
# This only supports single-word keywords.
python3 search.py keyword
```