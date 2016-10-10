
import httplib2
import json

def get_images_urls(username, max_images):
	last_id = None
	limitation = 1000 # 1000 requests max, 20 items per request = 20000 items max
	images_info = []
	while limitation != 0:
		limitation -= 1
		content = __load_media_page(username, last_id)
		if content is not None:
			data, more_available, last_id = __extract_media_data(content)
			images_info.extend(data)
		else:
			print "Cannot fetch media for specified username (" + username + ")."
			print "Profile is private or invalid"
			quit()
		if (max_images <= len(images_info)) or (more_available is False):
			return images_info[:max_images]
	raise RuntimeError('get_images_info() -> Data acquisition loop limit was exceeded. Too many iterations.')

def __load_media_page(username, max_id_param=None):
	http = httplib2.Http()
	url = "https://www.instagram.com/" + username + "/media/"
	if max_id_param is not None:
		url += "?max_id=" + max_id_param
	resp, content = http.request(url, "GET")
	if resp['status'] == '200':
		return content
	return None

def __extract_media_data(content):
	json_data = json.loads(content)
	items = json_data['items']
	images_info = []
	last_id = ''
	for item in items:
		last_id = item['id']
		if item['type'] != 'image':
			continue
		images_info.append(item['images']['standard_resolution']['url'])
	return images_info, json_data['more_available'], last_id
	