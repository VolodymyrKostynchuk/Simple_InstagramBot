from const import browzer
from selenium.webdriver.common.keys import Keys

import math
import os 
import requests
import time 
# like and subscribe as las 


def autorization(login, password):
	browzer.get('https://www.instagram.com/')
	time.sleep(3)

	username_input = browzer.find_element_by_name('username')
	username_input.send_keys(login)
	time.sleep(1)
	password_input = browzer.find_element_by_name('password')
	password_input.send_keys(password)

	password_input.send_keys(Keys.ENTER)
	time.sleep(3)

def close_browzer():
	browzer.quit()

def get_url_photo():
	hrefs = browzer.find_elements_by_tag_name('a')
	return [item.get_attribute('href') for item in hrefs if '/p/' in item.get_attribute('href')]

def las(post_url, by_hachtag=False, by_nickname=False):
	# by hachtag needed because if we run "lash" we will feel different users every time
	# by nickname we subscribe only once 
	for url in post_url:
		browzer.get(url)
		time.sleep(2)
		like_button = browzer.find_element_by_xpath('/html/body/div[1]/section/main/div/div/article/div/div[2]/div/div[2]/section[1]/span[1]/button').click()
		time.sleep(1)
		if by_hachtag:
			subscrive_button = browzer.find_element_by_xpath('/html/body/div[1]/section/main/div/div[1]/article/div/div[2]/div/div[1]/div/header/div[2]/div[1]/div[2]/button/div').click()
			time.sleep(1)
	if by_nickname:
			subscrive_button = browzer.find_element_by_xpath('/html/body/div[1]/section/main/div/div/article/div/div[2]/div/div[1]/div/header/div[2]/div[1]/div[2]/button/div').click()
			time.sleep(1)
	time.sleep(3)

def get_count_post(count_post_on_page_xpath):
	count_post = browzer.find_element_by_xpath(count_post_on_page_xpath).text
	return float(count_post.replace(' ', ''))

def count_scroll(count_post):
	# there is a restriction because more than 1400 posts cannot be liked on Instagram
	if count_post > 1400:
		count_post = 1400 
	scrolls = count_post / 12 
	scrolls = math.ceil(scrolls) 
	return scrolls

def scroll(scrolls):
	for scroll in range(1, scrolls):
		browzer.execute_script('window.scrollTo(0, document.body.scrollHeight);') 
		time.sleep(2)
	time.sleep(3)

def add_url_photo(post_url):
	with open('url_post.txt', 'a') as file:
		for url in post_url:
			file.write(url + '\n')

def get_url_on_clear():
	with open('url_post.txt', 'r+') as file:
		url_on_clear = []
		for url in file:
			url_on_clear.append(url) 
		file.truncate(0)
	return url_on_clear

def clear_las(url_on_clear):
	for url in url_on_clear:
		browzer.get(url)
		time.sleep(1)
		unsuscribe_user()
	
def unsuscribe_user():
	like_button = browzer.find_element_by_xpath('/html/body/div[1]/section/main/div/div/article/div/div[2]/div/div[2]/section[1]/span[1]/button').click()
	subscribe_button_text = browzer.find_element_by_xpath('/html/body/div[1]/section/main/div/div[1]/article/div/div[2]/div/div[1]/div/header/div[2]/div[1]/div[2]/button/div').text
	time.sleep(1)
	# works only in English browser
	if subscribe_button_text == 'Відстежується':
		unsubscribe_button = browzer.find_element_by_xpath('/html/body/div[1]/section/main/div/div[1]/article/div/div[2]/div/div[1]/div/header/div[2]/div[1]/div[2]/button/div').click()
		time.sleep(1)
		unsubscribe_button = browzer.find_element_by_xpath('/html/body/div[6]/div/div/div/div[3]/button[1]').click()
	time.sleep(1)

def media_src(media_xpath):
	media_src = browzer.find_element_by_xpath(media_xpath).get_attribute('src')
	return media_src

def get_first_xpath(tagname, attribute):
	imgs = browzer.find_elements_by_tag_name(tagname)
	img_src = [item.get_attribute(attribute) for item in imgs ]
	return img_src[0]

def get_namefile():
	namefile = browzer.current_url.split('/')[-2]
	return namefile

def get_nameforder(xpath_to_nickname):
	nameforder = browzer.find_element_by_xpath(xpath_to_nickname).text
	return nameforder

def xpath_forder(nameforder, format_media):
	xpath_forder = f'media\\{nameforder}\\{format_media}'
	return xpath_forder

def create_forder(nameforder):
	forders = ('img', 'stories', 'video', 'avatar')
	xpath_forder = f'media\\{nameforder}\\'
	if not os.path.isdir(xpath_forder):
		os.makedirs(f'{xpath_forder}')
		for forder in forders:
			os.makedirs(f'{xpath_forder}\\{forder}')

def download_img(img_src, nameforder, namefile, format_media):
	create_forder(nameforder)
	forder = xpath_forder(nameforder, format_media)
	get_img = requests.get(img_src)
	with open(f'{forder}\\{namefile}.png', 'wb') as file:
		file.write(get_img.content)

def download_video(media_src, nameforder, namefile, format_media):
	create_forder(nameforder)
	forder = xpath_forder(nameforder, format_media)
	get_video = requests.get(media_src, stream=True)
	with open(f'{forder}\\{namefile}.mp4', 'wb') as file:
		for cp in get_video.iter_content(chunk_size=1024*1024):
			if cp:
				file.write(cp)