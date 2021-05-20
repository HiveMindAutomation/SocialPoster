# Social Media Poster for YouTube Creators

## Concept

This Script utilizes the YouTube API to retrieve the details of the most recently uploaded video including the VideoID, Title and thumbnail.
The script then generates a Social Media Post for Twitter, Instagram and Facebook, and uses the relevant API's to post them.

## Preparation

Fill out authkeys-template.py and save as authkeys.py

[Instructions for getting a YouTube API Key - Follow Step 1 only](https://www.wonderplugin.com/youtube-api-key-and-playlist-id/#:~:text=Step%202%20%2D%20Find%20your%20YouTube%20playlist%20ID&text=Login%20your%20YouTube%20account%2C%20click,the%20playlist%20to%20edit%20it.&text=2.,ID%20from%20the%20Share%20URL))

You'll also need to get your Channel ID in your authkeys.py file.
[Get YouTube Channel ID](https://support.google.com/youtube/answer/3250431?hl=en)

[How to get a Facebook API Key](https://developers.facebook.com/docs/pages/getting-started/)

[Obtaining Twitter Authentication Tokens](https://developer.twitter.com/en/docs/authentication/oauth-1-0a/obtaining-user-access-tokens)

And your Instagram Username and password you should already know.... I hope

You'll also need a mySQL Database with a Table called "videos" with the following fields:  
|Field Name|Field Type|Field Length|Field Collation|Is Primary Key|
|---|---|---|---|---|
|video_id|VARCHAR|1024|utf8_bin|YES
|videoTitle|VARCHAR|1024|utf8-bin|NO
|link|VARCHAR|1024|utf8-bin|NO
|thumbnail|longblob| | |NO

___

## Requirements

Requires the following Libraries to be installed. you can use `pip 3 install {packagename}` to install them

`google-api-python-client`  
`instabot`  
`matplotlib`  
`tweepy`  
`facebook-sdk`  
`mysql-connector-python`  
`wget`

other libraries SHOULD be installed by default.  
Alternatively, run `install -r requirements.txt` however this is likely to install libraries you may not need that I had in my configuration during development

## Usage

### To run fully automated

In my environment, I have a cron job in my crontab that looks like this:  
`*/15 * * * * cd /Users/stuart/Nextcloud/Dev/YoutubeAPI/ && ./SocialPoster.sh >> /Users/stuart/Nextcloud/Logs/SocialPoster.log 2>&1`  
Which runs the Shell Script `SocialPoster.sh` every 15 minutes.  
If you're setting up the same system, you'll need to modify the paths in the Shell script and in the CRON job.  
I know using the crontab is wrong, I'll fix it later.  
___

### To run independently

To run the script independently of any crontab etc, ensure the requirements are installed and run:  
`python3 ./SocialPoster.py` from the folder the script is in.  
the output will only show the "WGET" progress.
