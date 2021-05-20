#!/usr/bin/env python3

import json
import os
import ssl
import facebook
from googleapiclient.discovery import build
from instabot import Bot
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import mysql.connector
import tweepy
import wget
import shutil
import logging

import authkeys


ssl._create_default_https_context = ssl._create_unverified_context

# Instantiate Logging
logging.basicConfig(filename='SocialPoster.log',format='%(asctime)s %(levelname)-8s %(message)s',encoding='utf-8',level=logging.INFO,datefmt='%Y-%m-%d %H:%M:%S')
logging.info('-----------------------------------   STARTING SOCIAL MEDIA POSTER    --------------------------------')

##############################################   VARIABLES   ################################################

videoNumber = 0

sqlHost = "192.168.1.20"
sqlDatabase = "YouTube"

#################################   Connect to MySQL       ##################################################

mydb = mysql.connector.connect(
  host=sqlHost,
  user=authkeys.sqlUser,
  password=authkeys.sqlPass,
  database=sqlDatabase,
)

#################################   FUNCTION DEFINITIONS   ##################################################

### Get Video Title ###
def getLatestVideo(ytApiKey, chanID):

    
    URLPrefix = "https://youtube.com/watch?v="

    youtube = build('youtube', 'v3', developerKey=ytApiKey)

    #### DEBUGGING ####
    ## List channel Content ##
    request = youtube.channels().list(
        part='contentDetails',
        id=chanID
    )
    ## Execute Request
    response = request.execute()

    ## Find playlist of all uploads and print the Playlist ID
    uploadsPlaylist = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    # print(uploadsPlaylist)

    ## Output response to query into a JSON file.
    # with open('channelDetails.json', 'w') as outfile:
    #     json.dump(response, outfile)

    # Use PlayID to define playlist we want the latest video for.
    playlist = youtube.playlistItems().list(
        part="contentDetails",
        playlistId=uploadsPlaylist
    )
    # Execute API Command and get response
    playlistResponse = playlist.execute()
    # Break Response out into Video ID of latest video 
    # Variable - videonumber - defined at top of script comes into play here.
    videoID = playlistResponse['items'][videoNumber]['contentDetails']['videoId']
    # Define API Lookup to get Video Details
    video = youtube.videos().list(
        part='snippet,contentDetails,statistics',
        id=videoID
        )
    videoResponse = video.execute()
    # Gest Video Title from Response.
    videoTitle = videoResponse['items'][0]['snippet']['localized']['title']
    # Generate URL from URLPrefix and videoID
    videoLink = f'{URLPrefix}{videoID}'
    # Generate Post Content
    postContent = f'Check out my latest YouTube video: {videoTitle}\n{videoLink}'

    # Generate Log messages:
    logging.info(f'Latest Video Found ID: {videoID}')
    logging.info(f'Latest Video Found Title: {videoTitle}')
    logging.info(f'Latest Video Link: {videoLink}')
    # print(postContent)

    # img = mpimg.imread(thumbnail)
    # imgplot = plt.imshow(img)
    # plt.show()

    return postContent, videoTitle, videoLink, videoID

### Get Video Thumbnail ###
def getThumb(ytApiKey, videoID):

    # Instantiate YouTube API
    youtube = build('youtube', 'v3', developerKey=ytApiKey)
    # Define API Lookup
    video = youtube.videos().list(
        part='snippet,contentDetails,statistics',
        id=videoID
        )
    # Execute API Lookup
    videoResponse = video.execute()
    #Get Video Thumbnail URL
    videoThumb = videoResponse['items'][0]['snippet']['thumbnails']['maxres']['url']

    # print(videoThumb)
    # Get Video Title
    videoTitle = videoResponse['items'][0]['snippet']['localized']['title']
    # Log details to logfile
    logging.info(f'Pulling Thumbnail from YouTube: {videoTitle}')
    # Download thumbnail file
    thumbnail = wget.download(videoThumb, out=f'{videoTitle}.jpg')

    img = mpimg.imread(thumbnail)
    # imgplot = plt.imshow(img)
    # plt.show()

    return img


### Post to Twitter ###
def post_to_twitter(postText, video_title):
    # Log Details
    logging.info('Authenticating to Twitter')
    # Authentication Details
    auth = tweepy.OAuthHandler(authkeys.consumer_API_Key, authkeys.consumer_API_Key_Secret)
    auth.set_access_token(authkeys.access_token, authkeys.access_token_secret)
    # Aunthenticate to tweepy
    api = tweepy.API(auth)
    # Define post text
    tweet_text = postText
    ## Post to Twitter
    logging.info('Posting to Twitter')
    # Post to Twitter
    api.update_with_media(f'{video_title}.jpg', tweet_text)

### Post to Instagram ###
def instagram_post(video_title, videoLink):
    #Instantiate InstaBot
    bot = Bot()
    # Login to Instagram
    logging.info('Logging into Instagram')
    bot.login(username = authkeys.instagramUsername, password = authkeys.instagramPassword)
    logging.info('Login Successful')
    # create caption
    caption_text = f'Check out my YouTube Video: {video_title}\n {videoLink} #HomeAutomation #HomeAssistant #SmartHome #Gadgets #GadgetNerd #SmartHomeIdeas #HomeAutomationIdeas'
    # Upload to Instagram
    logging.info('Posting to Instagram')
    bot.upload_photo(f'{video_title}.jpg', caption=caption_text)

### Post to FaceBook ###
def facebook_post(post_Text, videoLink):
    
    ##Instantiate facebook
    fb = facebook.GraphAPI(access_token=authkeys.faceBook_API_USER_Access_Token)
    # Post to FaceBook
    logging.info('Posting to FaceBook')
    fb.put_object(parent_object="me", connection_name="feed", message=post_Text, link=videoLink)

# Log to mySQL Database - This is OVERKILL
def logToSQL(video_id, video_title, videoLink, thumbnail):
    #Instantiate MySQL Cursor
    mycursor = mydb.cursor()
    # Open Thumbnail file
    thumbfile = open(f'{video_title}.jpg', 'rb').read()

    sql = "INSERT INTO videos (video_id, VideoTitle, link, thumbnail) VALUES (%s, %s, %s, %s)"
    val = (video_id, video_title, videoLink, thumbfile)
    
    try:
        mycursor.execute(sql, val)
        logging.info('Posting to MySQL Database')
    except mysql.connector.IntegrityError as err:
        logging.error(f"Error: {err}")
        return False

    respond = mydb.commit()

    # print(mycursor.rowcount, "record inserted.")
    # print(f"Record ID: {mycursor.lastrowid}")

    if respond == None:
        return True
    
        

#############################################################################################################

### Call VideoTitle Function ###
post = getLatestVideo(authkeys.youTube_key,authkeys.channelID)

### Call Thumbnail Function ###
videoThumbnail = getThumb(authkeys.youTube_key,post[3])

posting = logToSQL(post[3], post[1], post[2], videoThumbnail)

if posting == True:
    ### Call Twitter Post function ###
    post_to_twitter(post[0], post[1])

    ### Call Instagram Post function ###
    instagram_post(post[1], post[2])

    ### Call Facbook Post function ###
    facebook_post(post[0], post[2])

    ## Output
    logging.info(f"{post[1]} posted to Socials")
    logging.info("Cleaning up Files.....")
    logging.info('')
    os.remove(f"{post[1]}.jpg.REMOVE_ME")
    try:
        shutil.rmtree('config')
    except OSError as e:
        logging.error("#######################################")
        logging.error("Error: %s : %s" % ('config', e.strerror))
        logging.error('#######################################')
    logging.info('-----------------------------------       END RUN     -----------------------------------')
    logging.info('')

else:
    logging.error(f"{post[1]} Already posted to Socials. Skipping.")
    logging.info("Cleaning Up Files.....")
    os.remove(f"{post[1]}.jpg")
    logging.info('-----------------------------------       END RUN     -----------------------------------')
    logging.info('')
    