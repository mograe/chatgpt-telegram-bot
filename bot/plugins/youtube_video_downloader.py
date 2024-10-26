import logging
import re
from typing import Dict

from pytubefix import YouTube

from .plugin import Plugin


class YouTubeVideoDownloaderPlugin(Plugin):
    """
    A plugin to download a YouTube video
    """

    def get_source_name(self) -> str:
        return "YouTube Video Downloader"

    def get_spec(self) -> [Dict]:
        return [{
            "name": "download_youtube_video",
            "description": "Download a YouTube video",
            "parameters": {
                "type": "object",
                "properties": {
                    "youtube_link": {"type": "string", "description": "YouTube video link to download"}
                },
                "required": ["youtube_link"],
            },
        }]

    async def execute(self, function_name, helper, **kwargs) -> Dict:
        link = kwargs['youtube_link']
        try:
            video = YouTube(link)
            stream = video.streams.get_highest_resolution()
            output = re.sub(r'[^\w\-_\. ]', '_', video.title) + '.mp4'
            stream.download(filename=output)
            return {
                'direct_result': {
                    'kind': 'file',
                    'format': 'path',
                    'value': output
                }
            }
        except Exception as e:
            logging.warning(f'Failed to download YouTube video: {str(e)}')
            return {'result': 'Failed to download video'}