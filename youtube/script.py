from __future__ import print_function
import requests
import json
import sys
import os

from yt_channels_list import dump_to_file

api_key = "AIzaSyBBrX78q8Q9VP1BxZEWr0s7Xa7vWI8yA8A"
base_url = "https://www.googleapis.com/youtube/v3"

# get channel info
# https://www.googleapis.com/youtube/v3/channels?id={channel Id}&key={API key}&part=contentDetails
# get videolist
# https://www.googleapis.com/youtube/v3/playlistItems?order=date&part=snippet,contentDetails&
# playlistId=UU8butISFwT-Wl7EV0hUK0BQ&maxResults=25&key=AIzaSyBBrX78q8Q9VP1BxZEWr0s7Xa7vWI8yA8A

# structure
'''

youtube_channels : {
	channel_id : {
		"title": string,
		"some more details" : string,
		"videos" : [
			{
				video_id : string,
				title : string,
				"description" : string
				comments : [
					{
						"authorname": string,
						"message" : string,
						"publish date" : string 
					}
				]
			}
		]
	}
}
'''

def log(s):
	print(s, file=sys.stderr)

def print_json(j):
	log(json.dumps(j, indent=4))

def load_channel_list():
	if os.path.isfile("yt_channels_list.json"):
		pass
	else:
		dump_to_file()
	json_data = open("yt_channels_list.json", 'r').read()
	store = json.loads(json_data)
	return store["yt_channels_list"]

def channel_description(channel_id):
	channel_detail = {}
	part = "snippet,contentDetails,statistics"
	log("Setting url for channel description...")
	url = base_url + "/channels?id=" + channel_id + "&key=" + api_key + "&part=" + part
	log("Sending request for channel description...")
	response = requests.get(url)
	log("parsing response json for channel description")

	rjson = json.loads(response.content)
	playlist_id = rjson["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
	statistics = rjson["items"][0]["statistics"]
	snippet = rjson["items"][0]["snippet"]
	# print_json(rjson)
	channel_detail["title"] = snippet["title"]
	channel_detail["country"] = snippet["country"]
	channel_detail["publishedAt"] = snippet["publishedAt"]
	channel_detail["description"] = snippet["description"]
	channel_detail["commentCount"] = statistics["commentCount"]
	channel_detail["viewCount"] = statistics["viewCount"]
	channel_detail["videoCount"] = statistics["videoCount"]
	channel_detail["subscriberCount"] = statistics["subscriberCount"]
	videos = video_description(playlist_id)
	channel_detail["videos"] = videos
	return channel_detail
	# print_json(channel_detail)
	log("Done channel detail")

def video_description(playlist_id):
	log("getting all videos....")
	part = "snippet,contentDetails"
	next_page = ""
	log("Setting url for video description..")
	videos = []
	while True:
		url = base_url + "/playlistItems?"+next_page+"order=date&part=" + part + "&playlistId=" + playlist_id + \
				"&maxResults=50&key=" + api_key
		log("Sending request for video description...")
		response = requests.get(url)
		rjson = json.loads(response.content)
		log("parsing response json for all videos...")
		for item in rjson["items"]:
			video_detail = {}
			video_id = item["contentDetails"]["videoId"]
			published_at = item["contentDetails"]["videoPublishedAt"]
			snippet = item["snippet"]
			video_detail["video_id"] = video_id
			video_detail["title"] = snippet["title"]
			video_detail["description"] = snippet["description"]
			video_detail["publishedAt"] = published_at
			video_detail["video_no."] = snippet["position"]
			video_detail["comments"] = get_comment(video_id)
			videos.append(video_detail)
		if("nextPageToken" in rjson):
			log("next page of videos")
			next_page="pageToken=" + rjson["nextPageToken"] + "&"
		else:
			log("Done Video detail")
			break
	# log(videos)
	return videos

def get_comment(video_id):
	log("Getting comment for " + video_id)
	part = "snippet,replies"
	next_page = ""
	comments = []
	while True:
		url = base_url + "/commentThreads?" + next_page + "videoId=" + video_id + "&maxResults=100&key=" + api_key + "&part=" + part
		log("Sending request for comments...")
		response = requests.get(url)
		rjson = json.loads(response.content)
		for item in rjson["items"]:
			comment={}
			topLevelComment = item["snippet"]["topLevelComment"]
			comment["author_name"] = topLevelComment["snippet"]["authorDisplayName"]
			comment["message"] = topLevelComment["snippet"]["textDisplay"]
			comment["published_at"] = topLevelComment["snippet"]["publishedAt"]
			replycount = item["snippet"]["totalReplyCount"]
			# log(replycount)
			comments.append(comment)
			if(replycount > 0):
				# get replies item["replies"]
				for com in item["replies"]["comments"]:
					comment={}
					snippet = com["snippet"]
					comment["author_name"] = snippet["authorDisplayName"]
					comment["message"] = snippet["textDisplay"]
					comment["published_at"] = snippet["publishedAt"]
					comments.append(comment)
		# log(comments)
		if("nextPageToken" in rjson):
			log("next page of comments")
			next_page="pageToken=" + rjson["nextPageToken"] + "&"
		else:
			log("Done Comment section for " + video_id)
			break
	# print_json(rjson)
	return comments


if __name__ == "__main__":

	channel_list = load_channel_list()
	youtube_channels = {}
	for channel in channel_list:
		log("getting data for channel " + channel)
		youtube_channels[channel] = channel_description(channel)
		
	print_json(youtube_channels)