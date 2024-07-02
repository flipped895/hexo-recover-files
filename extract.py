import os
import shutil
import json
import convert_html
from bs4 import BeautifulSoup


def find_path(name, path):
    for root, dirs, files in os.walk(path):
        if name in dirs:
            return os.path.join(root, name)

def get_post_folders(post_parent_folders, static_folder):
	folder_paths = []
	folder_names = [ html_filename + '/index.html' for html_filename in post_parent_folders]
	for directory in post_parent_folders:
		folder_paths.append(static_folder + '/' + directory)

	return folder_paths, folder_names

# year_folders = [item for item in os.listdir("website/") if item[:2] == '20']

with open('./hexo-recover-files/locations.json') as json_data:
    d = json.load(json_data)
    static_folder = d['static_folder']
    hexo_project_folder = d['hexo_project_folder']
    post_parent_folders = d['post_parent_folders']

# Traverse directories two levels down
folder_paths, folder_names  = get_post_folders(post_parent_folders, static_folder)

# if os.path.exists('posts'):
# 	shutil.rmtree("posts")

if not os.path.exists('posts'):
	os.mkdir(hexo_project_folder + '/posts')

for index, folder in enumerate(folder_paths):
	try:
		shutil.copytree(folder, 'posts/' + folder_names[index])
	except:
		print('Folder already copied.')

for post in folder_names:
	try:
		convert_html.build_file(post)
		print("Built " + post)
		os.remove("posts/" + post + "/index.html")
	except:
		print("No file")