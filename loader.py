
import os
import tqdm
import re
import random as rd

import tweepy as tpy
from urllib import request, error

from api_key import *


auth = tpy.OAuthHandler(API_KEY, API_KEY_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

API = tpy.API(auth)

_seen_dir = 'seen/'
_save_media_dir = 'load/'


def get_media_list_by_name(user_name):
    print('finding', user_name)
    user_id = API.get_user(screen_name=user_name).id_str
    print('user id:', user_id)

    feeds = {
        "user_id": user_id,
        "exclude_replies": True,
        "include_rts": False,
    }

    save_path = os.path.join(_seen_dir, user_id + '.pl')
    print(save_path)
    if os.path.exists(save_path):
        preload = True
        print(' ')
        print('preload data exist')

        with open(save_path, 'r') as f:
            preload_lines = f.readlines()

        last_id = preload_lines[0].split()[0]
        feeds['since_id'] = last_id
        print('n_preload:', len(preload_lines))
        print('start from id:', last_id)

    else:
        preload = False


    print(' ')

    all_medias = []
    cnt = 0
    for tweet in tpy.Cursor(API.user_timeline, **feeds).items():
        tweet_id = tweet.id_str
        # print(tweet.text)
        if 'media' in tweet.entities:
            medias = tweet.extended_entities['media']
            # print(len(medias))
            for media in medias:
                url = ''
                media_type = media['type']
                # print(media_type, end=' ')

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
                    print('{: 4d}  {}  {}  {}'.format(cnt, tweet.id_str, media_type, url))
                    all_medias.append([tweet_id, media_type, url])
        cnt += 1
    if cnt:
        print(' ')

    if preload:
        for line in preload_lines:
            try:
                tweet_id, media_type, url = line.split()
            except ValueError:
                continue

            all_medias.append([tweet_id, media_type, url])

    print('finished loading all media list')
    print('number of medias:', len(all_medias))

    if cnt:
        print('save loaded data')
        os.makedirs(_seen_dir, exist_ok=True)
        with open(save_path, 'w') as f:
            for tid, mtype, url in all_medias:
                f.write('{} {} {}\n'.format(tid, mtype, url))

    return all_medias, cnt


def get_filename_from_url(url):
    p = re.compile('[0-9a-zA-z_-]+[.][\w]+')
    try:
        res = p.findall(url)[1]
    except IndexError:
        print('error', url)
        res = '{:04d}'.format(rd.randint(0, 9999))
        print('generate random name', res)
    return res


def save_all_medias_by_name(user_name):
    user_id = API.get_user(screen_name=user_name).id_str
    user_save_dir = os.path.join(_save_media_dir, user_name)

    all_medias, n_new = get_media_list_by_name(user_name)
    # all_medias = [*reversed(all_medias)]

    print('start saving files...')
    os.makedirs(user_save_dir, exist_ok=True)
    with open(os.path.join(user_save_dir, user_id), 'w'):
        pass
    cnt = 0
    for tid, mtype, url in tqdm.tqdm(all_medias):
        fname = str(tid) + '_' + get_filename_from_url(url)
        save_path = os.path.join(user_save_dir, fname)
        if not os.path.exists(save_path):
            try:
                request.urlretrieve(url, save_path)
            except error.URLError:
                print('passed', cnt, url)
        cnt += 1
    print('save done')






