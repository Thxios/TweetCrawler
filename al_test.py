
import loader


with open('targets.txt', 'r') as f:
    usr_all = list(map(lambda s: s.strip(), f.readlines()))
user_name = usr_all[-1]

loader.save_all_medias_by_name(user_name)

