from imgur_python import Imgur #https://pypi.org/project/imgur-python/
							   #https://stackoverflow.com/questions/37486480/how-do-you-get-access-token-and-refresh-token-from-imgur

def imagelink(imgname):
	imgur_client = Imgur({
	"client_id": "",
	"client_secret": "",
	"access_token": "",
	"expires_in": "",
	"token_type": "",
	"refresh_token": "",
	"account_username": "",
	"account_id": 
	})
	image = imgur_client.image_upload(imgname, imgname, 'cen450')
	# image_id = image['response']['data']['id']
	return(image['response']['data']['link'])