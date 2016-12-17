import requests
import praw
import os
import json

DIR_NAME = '/home/ben/Pictures/Wallpapers'

if __name__ == '__main__':
    reddit = praw.Reddit('wallpaper')
    subreddit = reddit.subreddit('wallpapers')
    #if not os.path.exists(DIR_NAME):
    #    os.mkdir(DIR_NAME)
    for submission in subreddit.top('week', limit=5):
        print(submission.title)
        print(submission.url)
        response = requests.get(submission.url)
        response.raise_for_status()
        if 'gifv' in submission.url:
            continue
        if 'gfycat' in submission.url:
            json_url = 'https://gfycat.com/cajax/get/' + submission.url.split('/')[-1]
            response = requests.get(json_url)
            response.raise_for_status()
            json_dict = json.loads(response.text)
            mp4_url = json_dict['gfyItem']['mp4Url']
            response = requests.get(mp4_url)
            response.raise_for_status()
            filename = submission.url.split('/')[-1] + '.mp4'
        elif 'imgur' in submission.url:
            if 'imgur.com/a/' in submission.url:
                # don't both with albums
                print('Skipping album')
                continue
            elif 'i.imgur.com' in submission.url:
                # this is single image, linked directly
                print('Single image, direct link')
                filename = submission.url.split('/')[-1]
            else:
                print('Single image, not a direct link')
                continue
                # TODO
                #soup = BeautifulSoup(response.text)
                #image_url = soup.select('.image a')[0]['href']
                #response = requests.get(image_url)
                #response.raise_for_status()
                #filename = submission.url.split('/')[-1]
        else:
            filename = submission.url.split('/')[-1]
        filename = os.path.join(DIR_NAME, filename)
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(100000):
                f.write(chunk)
