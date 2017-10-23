#!/usr/bin/python

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

#pip install --upgrade google-api-python-client
#pip install --upgrade oauth2client

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "AIzaSyBwNVR6_l9EMoNsWVReIJy1MQ3c7j3fcEI"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# def youtube_search(options):
def youtube_search(query, maxResults):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  # Call the search.list method to retrieve results matching the specified
  # query term.
  # search_response = youtube.search().list(
  #   q=options.q,
  #   part="id,snippet",
  #   maxResults=options.max_results
  # ).execute()

  search_response = youtube.search().list(
    q=query,
    part="id,snippet",
    maxResults=maxResults
  ).execute()


  videos = []
  channels = []
  playlists = []
  ids = []

  # Add each result to the appropriate list, and then display the lists of
  # matching videos, channels, and playlists.
  for search_result in search_response.get("items", []):
    if search_result["id"]["kind"] == "youtube#video":
      videos.append("%s (%s)" % (search_result["snippet"]["title"],
                                 search_result["id"]["videoId"]))
      ids.append(search_result["id"]["videoId"])
    elif search_result["id"]["kind"] == "youtube#channel":
      channels.append("%s (%s)" % (search_result["snippet"]["title"],
                                   search_result["id"]["channelId"]))
    elif search_result["id"]["kind"] == "youtube#playlist":
      playlists.append("%s (%s)" % (search_result["snippet"]["title"],
                                    search_result["id"]["playlistId"]))


    # for id in ids:
    #   print id
  return ids
   # print "Videos:\n", "\n".join(videos), "\n"
  # print "Channels:\n", "\n".join(channels), "\n"
  # print "Playlists:\n", "\n".join(playlists), "\n"


if __name__ == "__main__":
  argparser.add_argument("--q", help="Search term", default="Google")
  argparser.add_argument("--max-results", help="Max results", default=25)
  args = argparser.parse_args()

  try:
    youtube_search(args)
  except HttpError, e:
    print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)
