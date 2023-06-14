"""Code to download the transcripts from YouTube."""
import pathlib
import json
import logging
from typing import Dict, List, Union, Optional

import pytube
from youtube_transcript_api import YouTubeTranscriptApi


def get_playlist_info(url: str) -> Dict[str, str]:
    """Gets the video IDs and titles from a YouTube playlist.

    Args:
        url (str): The URL of the YouTube playlist.
    Returns:
        Dict[str, str]: A dictionary with the video titles as keys and the
            video IDs as values.
        """
    playlist = pytube.Playlist(url)

    # Dict to hold title-ID pairs
    video_dict = {}

    for video in playlist.videos:
        video_dict[video.title] = video.video_id

    return video_dict


def download_transcript(video_title: str,
                        video_id: str,
                        output_path: pathlib.Path,
                        logger: Optional[logging.Logger] = None) -> None:
    """Downloads the transcript of a YouTube video.

    Args:
        video_title (str): The title of the YouTube video.
        video_id (str): The ID of the YouTube video.
        output_path (pathlib.Path): The path to the output file.
        logger (logging.Logger): The logger.

    Raises:
        Exception: If the transcript cannot be downloaded.
    """
    try:
        # Download transcript with youtube_transcript_api
        transcript = YouTubeTranscriptApi.get_transcript(
            video_id, languages=['en', 'en-US'])

        # Save transcript to a JSON file
        with open(output_path, 'w', encoding='utf-8') as file:
            # Put the title and the video ID at the top of the JSON file and
            # then dump the transcript
            json.dump({
                'title': video_title,
                'video_id': video_id,
                'transcript': transcript}, file, ensure_ascii=False, indent=4)

        if logger is not None:
            logger.info(f'Transcript has been saved to {output_path}')

    except Exception as error_msg:
        if logger is not None:
            logger.error(f'An error occurred: {str(error_msg)}')

def download_playlist(url: str, data_path: pathlib.Path) -> None:
    """Downloads the transcripts of a YouTube playlist.

    Args:
        url (str): The URL of the YouTube playlist.
        data_path (pathlib.Path): The path to the data directory.
    """
    video_id_dict = get_playlist_info(url)

    for i, (video_title, video_id) in enumerate(video_id_dict.items()):
        output_file = data_path / 'raw' / f'Episode_{str(i + 1)}.json'
        download_transcript(video_title, video_id, output_file)


def _replace_newlines(json_file: dict) -> None:
    """Replaces \n with a space

    Args:
        json_file (dict): The JSON file.
        """
    for segment in json_file['transcript']:
        segment['text'] = segment['text'].replace('\n', ' ')


def create_chunked_data(file_path: pathlib.Path,
                        max_chunk_size: int,
                        min_overlap_size: int
                        ) -> List[Dict[str, Union[str, List[str]]]]:
    """Creates chunked data from a JSON file.

    Args:
        file_path (str): The path to the JSON file.
        max_chunk_size (int): The maximum size of a chunk.
        min_overlap_size (int): The minimum size of the overlap between two
            chunks.
    Returns:
        List[Dict[str, Union[str, List[str]]]]: A dictionary with the chunked
            data.
        """
    with open(file_path, 'r') as file:
        json_file = json.load(file)

    # Replace \n with a space
    _replace_newlines(json_file)

    segment_lengths = [len(json_file['transcript'][segment]['text']) for
                       segment in range(len(json_file['transcript']))]

    # Split the transcript into chunks
    chunks_indices = []

    current_beginning_index = 0
    current_ending_index = 0
    current_chunk_size = 0

    for current_index, segment_length in enumerate(segment_lengths):
        if current_chunk_size + segment_length + 1 < max_chunk_size:
            current_chunk_size += segment_length + 1
            current_ending_index = current_index
            continue
        chunks_indices.append((current_beginning_index, current_ending_index))
        current_chunk_size += segment_length
        current_ending_index = current_index

        while current_chunk_size > max_chunk_size - min_overlap_size + 1:
            current_chunk_size -= segment_lengths[current_beginning_index] + 1
            current_beginning_index += 1
        current_chunk_size += 1

    # Now that we have the chunk indices, we can create the chunks
    # chunks = [{
    #     'text': ' '.join(
    #         [segment['text'] for segment in
    #          json_file['transcript'][chunk_index[0]:chunk_index[1] + 1]]),
    #     'start': json_file['transcript'][chunk_index[0]]['start'],
    #     'duration': sum(
    #         segment['duration'] for segment in
    #         json_file['transcript'][chunk_index[0]:chunk_index[1] + 1]),
    #     'url': json_file['url'],
    #     'title': json_file['title']}
    #     for chunk_index in chunks_indices]

    base_url = 'https://www.youtube.com/watch?v='
    video = pytube.YouTube(base_url + json_file['video_id'])
    thumbnail_url = video.thumbnail_url
    chunks = []
    for chunk_index in chunks_indices:
        text_list = []
        duration_sum = 0
        start, end = chunk_index
        for segment in json_file['transcript'][start:end + 1]:
            text_list.append(segment['text'])
            duration_sum += segment['duration']
        timestamp = str(int(json_file['transcript'][chunk_index[0]]['start']))
        chunks.append({
            'text': ' '.join(text_list),
            'start': json_file['transcript'][chunk_index[0]]['start'],
            'duration': duration_sum,
            'url': base_url + json_file['video_id'] + f'&t={timestamp}s',
            'title': json_file['title'],
            'thumbnail': thumbnail_url
        })

    return chunks
