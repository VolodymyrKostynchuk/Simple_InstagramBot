import argparse
import logic as l 
import time 
# like and subscribe as las  


class Instagrambot:

	def __init__(self, login, password, browzer):
		self.login = login 
		self.password = password 
		self.browzer = browzer 
#-----------------------------------------------------------------------------------

	def main(self):		
		args = self.get_options()
		self.parser(args)

#-----------------------------------------------------------------------------------
	# functions for iteration  	

	def las_nickname(self, nickname):
		self.browzer.get(f'https://www.instagram.com/{nickname}/')
		time.sleep(3)
		count_post = l.get_count_post('/html/body/div[1]/section/main/div/header/section/ul/li[1]/div/span')
		count_scroll =  l.count_scroll(count_post)
		l.scroll(count_scroll)
		post_url = l.get_url_photo() 
		l.las(post_url, by_hachtag=False, by_nickname=True)
		l.add_url_photo(post_url)

	def las_hachtag(self, hachtag):
		self.browzer.get(f'https://www.instagram.com/explore/tags/{hachtag}/')
		time.sleep(3)
		count_post = l.get_count_post('/html/body/div[1]/section/main/header/div[2]/div/div[2]/div/span')
		count_scroll = l.count_scroll(count_post)
		l.scroll(count_scroll)
		post_url = l.get_url_photo() 
		l.las(post_url, by_hachtag=True, by_nickname=False)
		l.add_url_photo(post_url)

	def las_clear(self):
		url_on_clear = list(l.get_url_on_clear())
		l.clear_las(url_on_clear)

	def download_photo(self, url):
		self.browzer.get(url)
		time.sleep(2)
		img_src = l.get_first_xpath('img', 'src')
		namefile = l.get_namefile()
		nameforder = l.get_nameforder('/html/body/div[1]/section/main/div/div[1]/article/div/div[2]/div/div[1]/div/header/div[2]/div[1]/div[1]/div[1]/span/a')
		format_media = 'img'
		l.download_img(img_src, nameforder, namefile, format_media)
		print('[+] Photo successfully download')

	def download_avatar(self, nickname):
		self.browzer.get(f'https://www.instagram.com/{nickname}/')
		time.sleep(2)
		avatar_src = l.media_src('/html/body/div[1]/section/main/div/header/div/div/span/img')
		namefile = l.get_namefile()
		nameforder = l.get_nameforder('/html/body/div[1]/section/main/div/header/section/div[1]/h2')
		format_media = 'avatar'
		l.download_img(avatar_src, nameforder, namefile, format_media)
		print('[+] Avatar successfully download')

	def download_stories(self, url):
		self.browzer.get(url)
		time.sleep(2)
		miss_button = self.browzer.find_element_by_xpath('/html/body/div[1]/section/div[1]/div/section/div/div[1]/div/div/div/div[3]/button').click()
		# this nedded because stories can be both video and photo
		try:
			stories_src =  l.media_src('/html/body/div[1]/section/div[1]/div/section/div/div[1]/div/div/video/source')
		except:	
			stories_src = l.media_src('/html/body/div[1]/section/div[1]/div/section/div/div[1]/div/div/img')
		namefile = l.get_namefile()
		nameforder = l.get_nameforder('/html/body/div[1]/section/div[1]/div/section/div/header/div[2]/div[1]/div/div/div/div/a')
		format_media = 'stories'
		l.download_video(stories_src, nameforder, namefile, format_media)
		print('[+] Stories successfully download')
		
	def download_video(self, url):
		self.browzer.get(url)
		time.sleep(2)
		video_src = l.media_src('/html/body/div[1]/section/main/div/div[1]/article/div/div[1]/div/div/div/div/div/video')
		namefile = l.get_namefile()
		nameforder = l.get_nameforder('/html/body/div[1]/section/main/div/div[1]/article/div/div[2]/div/div[1]/div/header/div[2]/div[1]/div[1]/div/span/a')
		format_media = 'video'
		l.download_video(video_src, nameforder, namefile, format_media) 
		print('[+] Video successfully download')
		
#-----------------------------------------------------------------------------------

	def get_options(self):
		parse = argparse.ArgumentParser()

		parse.add_argument('--lasn', help='[+] Write here nickname on which will to tale plase "las"')
		parse.add_argument('--lash', help='[+] Write here hachrag on which will to tale plase "las"')
		parse.add_argument('--lasc', help='[+] Clear "las" which before this will be likes', action='store_const', const=True)
		parse.add_argument('--dp', help='[+] Download photo on url')
		parse.add_argument('--da', help='[+] Download photo on nickname')
		parse.add_argument('--ds', help='[+] Download stories on url')
		parse.add_argument('--dv', help='[+] Download stories on url')
		
		args = parse.parse_args()
		return args 

	def parser(self, args):
		l.autorization(self.login, self.password)

		if args.lasn: self.las_nickname(args.lasn)
		if args.lash: self.las_hachtag(args.lash)
		if args.lasc: self.las_clear()
		if args.dp: self.download_photo(args.dp)
		if args.da: self.download_avatar(args.da)
		if args.ds: self.download_stories(args.ds)
		if args.dv: self.download_video(args.dv)
		
		l.close_browzer()