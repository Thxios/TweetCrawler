

import tweepy as tpy

from api_key import *



auth = tpy.OAuthHandler(API_KEY, API_KEY_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

API = tpy.API(auth)


usr_all = [

]
user_name = usr_all[2]
user_id = API.get_user(screen_name=user_name).id_str
print(user_id)
quit()

# user = API.get_user(screen_name=user_name)
# print(user.id_str)

feeds = {
    "user_id": user_id,
    "exclude_replies": True,
    "include_rts": False,
}

all_medias = []

cnt = 0
for tweet in tpy.Cursor(API.user_timeline, **feeds).items():
    cnt += 1
    tweet_id = tweet.id_str
    print(cnt, tweet.created_at, tweet.id_str)
    # print(tweet.text)
    if 'media' in tweet.entities:
        medias = tweet.extended_entities['media']
        # print(len(medias))
        for media in medias:
            url = ''
            media_type = media['type']
            print(media_type, end=' ')

            if media_type == 'photo':
                url = media['media_url_https'] + '?name=large'

            elif media_type == 'video':
                mx_bitrate = -1
                # print(media['video_info']['variants'])
                for variant in media['video_info']['variants']:
                    if 'bitrate' in variant:
                        if variant['bitrate'] > mx_bitrate:
                            mx_bitrate = int(variant['bitrate'])
                            url = variant['url']

            else:
                print('unexpected media type:', media_type)

            if url:
                print(url)
                all_medias.append([tweet_id, media_type, url])
        # print(tweet.extended_entities['media'])
    print(' ')

print(len(all_medias))
with open('seen/{}.pl'.format(user_id), 'w') as f:
    for tid, mtype, url in all_medias:
        f.write('{} {} {}\n'.format(tid, mtype, url))

