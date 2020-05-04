import os
import json
import flatten_json
import datetime

def main():
    print()
    print('-----------------------------------------------')
    print('| BerserkParser: TikTok JSON parser by BTF117 |')
    print('-----------------------------------------------')
    print('......................................................................................................................................................')
    print('. This dirty script will find all the JSON files in given directory and subdirectories and search them for relevant information about a Tik Tok user .')
    print('. To collect these files, use a proxy and connect a smartphone/emulator to it.                                                                       .')
    print('. Export all the sessions with the string \'aweme/v1\' in the URL as JSON files.                                                                       .')
    print('. (For example, in Fiddler, File->Export->Selected Sessions->Raw Files)                                                                              .')
    print('......................................................................................................................................................\n')

    dirName=input('\nEnter the directory you want to parse: ')
        
    # Get the list of all the files in directory at given path
    listOfFiles = list()
    for (dirpath, dirnames, filenames) in os.walk(dirName):
        listOfFiles += [os.path.join(dirpath, file) for file in filenames]

    # init variables/kw
    search_list = ['user_unique_id', 'user_nickname', 'user_uid', 'aweme_list_0_author_short_id', 'user_birthday', 'user_city', 'user_province', 'user_location', 'aweme_list_0_author_region', 'user_gender', 'user_signature', 'user_signature_language', 'aweme_list_0_author_language', 'user_avatar_larger_url_list_0', 'aweme_list_0_author_video_icon_url_list', 'user_aweme_count', 'user_ins_id', 'user_twitter_id', 'user_twitter_name', 'user_youtube_channel_id', 'user_youtube_channel_title', 'user_apple_account', 'user_follower_count', 'user_following_count', 'user_total_favorited']

    ext_search_list = ['unique_id_modify_time', 'download_prompt_ts', 'region', 'region_of_residence', 'bind_phone', 'has_email', 'school_name', 'google_account', 'weibo_name']

    video_search_list = ['aweme_id', 'create_time', 'desc', 'music_play_url_url_list_0', 'statistics_comment_count', 'statistics_digg_count', 'statistics_download_count', 'statistics_play_count', 'statistics_share_count', 'statistics_whatsapp_share_count', 'video_play_addr_url_list_0', 'video_download_addr_url_list_0']

    user_unique_id=[]
    extra_now_bingo=[]
    extra_now_dict={}

    #find lowest/highest extra_now (timestamp at the beginning of the JSON files)
    for elem in listOfFiles:
        if elem.endswith('.json'):
            with open(elem, encoding='utf-8-sig') as f:
                datastore=flatten_json.flatten(json.load(f))
                if datastore.get('extra_now') is not None:
                    extra_now_dict.update({elem:datastore.get('extra_now')})
                else:
                    continue                    
    extra_now_min = min(extra_now_dict.values())
    extra_now_max = max(extra_now_dict.values())
    
    #find/extract/print uniqueid for target
    for item in search_list:
        for elem in listOfFiles:
            if elem.endswith('.json'):
                with open(elem, encoding='utf-8-sig') as f:
                    datastore=flatten_json.flatten(json.load(f))
                    #find the file with the lowest extra_now to open the profile of the target and not the one visited later
                    if datastore.get('extra_now') is not None and datastore.get('extra_now') == extra_now_min and datastore.get('user_unique_id') is not None:
                        user_unique_id.append(datastore.get('user_unique_id'))
    user_unique_id_set=(set(datastore.fromkeys(filter(None, (user_unique_id)))))

    print('\n** Profile for TikTok user ' + str(*user_unique_id_set) +':\n')

    #find extra_now for follower's profile
    for elem in listOfFiles:
        if elem.endswith('.json'):
            with open(elem, encoding='utf-8-sig') as f:
                datastore=flatten_json.flatten(json.load(f))
                if datastore.get('user_unique_id') not in user_unique_id_set and datastore.get('user_unique_id') != None:
                    extra_now_bingo.append(datastore.get('extra_now'))
    extra_now_bingo = min(extra_now_bingo)

    #find/extract/print basic info from target profile by parsing JSON file with lowest extra_now
    print('** Basic information:')
    for item in search_list:
        item_list=[]
        for elem in listOfFiles:
            if elem.endswith('.json'):
                with open(elem, encoding='utf-8-sig') as f:
                    datastore=flatten_json.flatten(json.load(f))
                    if datastore.get('extra_now') is not None and datastore.get('extra_now') == extra_now_min:
                        item_list.append(datastore.get(item))
        item_p=(str(item.replace('_',' ')))
        if item == 'aweme_list_0_author_short_id':
            print()
            print('Short ID:')
        elif item == 'aweme_list_0_author_region':
            print()
            print('Author Region:')
        elif item =='aweme_list_0_author_language':
            print()
            print('Author Region:')
        elif item == 'user_avatar_larger_url_list_0':
            print()
            print('Larger Avatar URL:')
        elif item == 'aweme_list_0_author_video_icon_url_list':
            print()
            print('Video Icon URL:')
        elif item == 'user_aweme_count':
            print()
            print('Number of videos:')
        elif item == 'user_ins_id':
            print()
            print('Instagram ID:')
        else:
            print('\n' + item_p.capitalize() +': ')
        item_list=filter(None, (item_list))
        print(*item_list)

    print('\n..............................................................................................................')

    #find/extract/print extended information from followers_X
    print('\n** Extended information found in metadata (following):')
    for elem in listOfFiles:
        if elem.endswith('.json'):
            with open(elem, encoding='utf-8-sig') as f:
                datastore=flatten_json.flatten(json.load(f))
                if datastore.get('extra_now') is not None and datastore.get('extra_now') > extra_now_bingo:
                    for x in range(20):
                        s=('followers_'+ str(x) +'_')
                        if datastore.get(s + 'unique_id') in user_unique_id_set:
                            for item in ext_search_list:
                                item_list=[]
                                item_list.append(datastore.get(s + str(item)))
                                while("[]" in item_list):
                                    item_list.remove("[]")
                                item_p=(str(item.replace('_',' ')))
                                print('\n' + item_p.capitalize() +': ')
                                if item == 'unique_id_modify_time' or item == 'download_prompt_ts' and item_list != [0] :
                                    print(*item_list)
                                    print(datetime.datetime.fromtimestamp(int(*item_list)).strftime('%d-%m-%Y %H:%M:%S'))
                                else:
                                    print(*item_list)

    print('\n..............................................................................................................')

    #find/extract/print videos list
    print('\n** List of videos seen while browsing:\n')
    for elem in listOfFiles:
        if elem.endswith('.json'):
            with open(elem, encoding='utf-8-sig') as f:
                datastore=flatten_json.flatten(json.load(f))
                if datastore.get('extra_now') is not None and datastore.get('extra_now') < extra_now_bingo:
                    for x in range(20):                      
                        s=('aweme_list_'+ str(x) +'_')
                        authvid = datastore.get(s + 'author_unique_id')
                        if authvid in user_unique_id:
                            for item in video_search_list:
                                item_list=[]
                                item_list_vid = (datastore.get(s + item))
                                item_p=(str(item.replace('_',' ')))
                                if item_list_vid == None:
                                    continue
                                else:
                                    if item == 'aweme_id':
                                        print()
                                        print('Video ID: ')
                                    elif item == 'desc':
                                        print()
                                        print('Video description: ')
                                    elif item =='statistics_digg_count':
                                        print()
                                        print('Number of "diggs": ')
                                    elif item =='music_play_url_url_list_0':
                                        print()
                                        print('Video music/sound: ')
                                    elif item == 'statistics_comment_count':
                                        print()
                                        print('Number of comments: ')
                                    elif item == 'statistics_download_count':
                                        print()
                                        print('Number of downloads: ')
                                    elif item == 'statistics_play_count':
                                        print()
                                        print('Number of time video was played: ')
                                    elif item == 'statistics_whatsapp_share_count':
                                        print()
                                        print('Number of times video was shared on WhatsApp: ')
                                    elif item == 'video_play_addr_url_list_0':
                                        print()
                                        print('URL for video without watermarks (stickers still present): ')
                                    elif item == 'video_download_addr_url_list_0':
                                        print()
                                        print('URL for full video: ')
                                    else:
                                        print('\n' + item_p.capitalize() +': ')
                                    if item == 'create_time' and item_list_vid != [0] :
                                        print(item_list_vid)
                                        print(datetime.datetime.fromtimestamp(int(item_list_vid)).strftime('%d-%m-%Y %H:%M:%S'))
                                    else:
                                        print(item_list_vid)
                                    print('.')
                                    if item == ('video_download_addr_url_list_0'):
                                        print('******************************')

    print('\n..............................................................................................................')

    #find/extract/print following
    print('\n** List of following (nickname, unique ID and UID) seen while browsing:\n')
    for elem in listOfFiles:
        item_list_n=[]
        item_list_uni=[]
        item_list_uid=[]
        if elem.endswith('.json'):
            with open(elem, encoding='utf-8-sig') as f:
                datastore=flatten_json.flatten(json.load(f))
                if datastore.get('extra_now') is not None and datastore.get('extra_now') < extra_now_bingo:
                    for x in range(20):
                        s=('followings_'+ str(x) +'_')
                        item_list_n = (datastore.get(s + 'nickname'))
                        item_list_uni = (datastore.get(s + 'unique_id'))
                        item_list_uid = (datastore.get(s + 'uid'))

                        if item_list_n == None:
                            continue
                        else:
                            print(item_list_n)
                            print(item_list_uni)
                            print(item_list_uid)
                            print('.')

    print('\n..............................................................................................................')

    #find/extract/print followers
    print('\n** List of followers (nickname, unique ID and UID) seen while browsing:\n')
    for elem in listOfFiles:
        item_list_n=[]
        item_list_uni=[]
        item_list_uid=[]
        if elem.endswith('.json'):
            with open(elem, encoding='utf-8-sig') as f:
                datastore=flatten_json.flatten(json.load(f))
                if datastore.get('extra_now') is not None and datastore.get('extra_now') < extra_now_bingo:
                    for x in range(20):
                        s=('followers_'+ str(x) +'_')
                        item_list_n = (datastore.get(s + 'nickname'))
                        item_list_uni = (datastore.get(s + 'unique_id'))
                        item_list_uid = (datastore.get(s + 'uid'))
                        if item_list_n == None:
                            continue
                        else:
                            print(item_list_n)
                            print(item_list_uni)
                            print(item_list_uid)
                            print('.')
    print('\n..............................................................................................................')
    print('Done @ ' + str(datetime.datetime.now()))
    print()

def getListOfFiles(dirName):
    # create a list of files and sub directories names in the given directory 
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
    return allFiles       

                
if __name__ == '__main__':
    main()