# Social Media Poster for YouTube Creators

## Preparation

Fill out authkeys-template.py and save as authkeys.py

[Instructions for getting a YouTube API Key - Follow Step 1 only](https://www.wonderplugin.com/youtube-api-key-and-playlist-id/#:~:text=Step%202%20%2D%20Find%20your%20YouTube%20playlist%20ID&text=Login%20your%20YouTube%20account%2C%20click,the%20playlist%20to%20edit%20it.&text=2.,ID%20from%20the%20Share%20URL))

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

Requires the following Libraries to be installed. you can use `pip 3 install` to install them

`google-api-python-client`  
`instabot`  
`matplotlib`  
`tweepy`  
`facebook-sdk`
`mysql-connector-python`
`wget`


