
import loader


with open('targets.txt', 'r') as f:
    usr_all = list(map(lambda s: s.strip(), f.readlines()))
idx = 39
user_name = usr_all[idx-1]

# loader.get_media_list_by_name(user_name)
loader.save_all_medias_by_name(user_name)
