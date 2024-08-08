import os
import sys
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound

api_key = 'AIzaSyBO_vkgnC4OM0m1q-OoBvj2SS7IIuF_6Qk'
youtube = build('youtube', 'v3', developerKey=api_key)


def get_video_ids_from_channel(channel_id):
    video_ids = []
    request = youtube.search().list(
        part="id",
        channelId=channel_id,
        maxResults=50,
        order="date"
    )

    while request:
        response = request.execute()
        for item in response['items']:
            if item['id']['kind'] == "youtube#video":
                video_ids.append(item['id']['videoId'])

        request = youtube.search().list_next(request, response)

    return video_ids


def get_channel_handle(channel_id):
    request = youtube.channels().list(
        part="snippet",
        id=channel_id
    )
    response = request.execute()
    if response["items"]:
        custom_url = response["items"][0]["snippet"].get("customUrl", None)
        return custom_url.replace("@", "") if custom_url else response["items"][0]["snippet"]["title"]
    return None


def get_transcripts(video_ids):
    transcripts = {}
    for idx, video_id in enumerate(video_ids, 1):
        print(f"Getting transcript for https://www.youtube.com/watch?v={video_id} ({idx}/{len(video_ids)})")
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            transcripts[video_id] = transcript
        except (TranscriptsDisabled, NoTranscriptFound):
            print(f"No transcript available for https://www.youtube.com/watch?v={video_id}.")
        except Exception:
            print(f"An error occurred while fetching https://www.youtube.com/watch?v={video_id}.")
    return transcripts


def save_transcripts_to_files(transcripts, channel_name, base_output_dir):
    channel_dir = os.path.join(base_output_dir, channel_name)
    if not os.path.exists(channel_dir):
        os.makedirs(channel_dir)

    idx = 1
    total = len(transcripts)

    for video_id, transcript in transcripts.items():
        print(f"Saving transcript for https://www.youtube.com/watch?v={video_id} ({idx}/{total})")
        file_path = os.path.join(channel_dir, f"{video_id}.txt")
        with open(file_path, 'w', encoding='utf-8') as f:
            for entry in transcript:
                start_time = entry['start']
                text = entry['text']
                # Format the timestamp in hh:mm:ss format
                start_time_formatted = format_timestamp(start_time)
                f.write(f"[{start_time_formatted}] {text}\n")
        print(f"Saved transcript for video ID {video_id} to {file_path}")
        idx += 1


def format_timestamp(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"


def main(channel_id, base_output_dir):
    channel_name = get_channel_handle(channel_id)
    if not channel_name:
        print("Channel not found.")
        return

    # Use the channel name to create the directory
    video_ids = get_video_ids_from_channel(channel_id)
    transcripts = get_transcripts(video_ids)
    save_transcripts_to_files(transcripts, channel_name, base_output_dir)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("You must provide one channel ID you wish to get the transcripts for.")
        exit(1)
    channel_id = sys.argv[1]
    base_output_dir = "transcripts"  # the base folder name the transcript files should be saved to.
    print(f"Starting transcript download for {get_channel_handle(channel_id)}!")
    main(channel_id, base_output_dir)
