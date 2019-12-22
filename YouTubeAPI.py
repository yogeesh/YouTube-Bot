# -*- coding: utf-8 -*-

# Sample Python code for youtube.liveBroadcasts.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os
import json
import pickle

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

class YouTubeAPI:

	def __init__(self):
		self.YouTube = None # Set in function set_youtube_object
		self.set_youtube_object()



	def set_youtube_object(self):
		try:
			with open("YouTube.Object", "rb") as f:
				self.YouTube = pickle.load(f)
		except:
			return self.YouTube

		# retreive Youtube object from disk cache
		if str(type(self.YouTube)) == "<class 'googleapiclient.discovery.Resource'>":
			return

		self.scopes = ["https://www.googleapis.com/auth/youtube.readonly", "https://www.googleapis.com/auth/youtube.force-ssl"]
		# Disable OAuthlib's HTTPS verification when running locally.
		# *DO NOT* leave this option enabled in production.
		os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

		api_service_name = "youtube"
		api_version = "v3"
		client_secrets_file = "client_secretm.json"

		# Get credentials and create an API client
		flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, self.scopes)
		credentials = flow.run_console()
		self.YouTube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)

		with open("YouTube.Object", "wb") as f:
			pickle.dump(self.YouTube, f, pickle.HIGHEST_PROTOCOL)

		return self.YouTube

	def getLiveChatId(self):
		# [TODO] optimize: not necesssary to call youtube api to live chat id always
		request = self.YouTube.liveBroadcasts().list(
			part="snippet",
			broadcastStatus="active",
			broadcastType="all"
		)
		response = request.execute()

		try:
			self.live_chat_id = response["items"][0]["snippet"]["liveChatId"]
		except:
			# Mostly Stream offline
			self.live_chat_id = None

		return self.live_chat_id
		
	def get_live_chat_messages(self):
		live_chat_id = self.getLiveChatId()

		request = self.YouTube.liveChatMessages().list(
			liveChatId=live_chat_id,
			part="snippet"
		)
		response = request.execute()

		messages = []
		for item in response["items"]:
			messages.append(item["snippet"]["displayMessage"])

		return messages

	def send_message(self, message):
		live_chat_id = self.getLiveChatId()
		request = self.YouTube.liveChatMessages().insert(
			part="snippet",
			body={
				"snippet": {
				"liveChatId": live_chat_id,
				"type": "textMessageEvent",
				"textMessageDetails": {
					"messageText": message
				}
				}
			}
		)
		response = request.execute()

	def get_health_status(self):
		request = self.YouTube.liveStreams().list(
			part="snippet,cdn,contentDetails,status",
			mine=True
		)
		response = request.execute()

		print(response)

# Unit testing
def main():
	youtube_obj = YouTubeAPI()

	youtube_obj.get_health_status()
	# live_chat_id = youtube_obj.getLiveChatId()

	# print(youtube_obj.get_live_chat_messages())

	# welcome_message = \
	# 	"█▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█ "\
	# 	"█░░╦─╦╔╗╦─╔╗╔╗╔╦╗╔╗░░█ "\
	# 	"█░░║║║╠─║─║─║║║║║╠─░░█ "\
	# 	"█░░╚╩╝╚╝╚╝╚╝╚╝╩─╩╚╝░░█ "\
	# 	"█▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█"
	# print(youtube_obj.send_message(welcome_message))
	

if __name__ == "__main__":
    main()