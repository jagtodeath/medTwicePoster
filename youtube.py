import gdata.youtube
import gdata.youtube.service
import getpass

try:
	developer_key = eval(open('/Users/JAG/Dropbox/Workspace/SecureFiles/YTKey.ignore','r').read())
except IOError:
	print 'Developer Key:',
	developer_key = raw_input()
try:
	user,pw = eval(open('/Users/JAG/Dropbox/Workspace/SecureFiles/GoogleLogin.ignore','r').read())
except IOError:
	print 'Google Email:',
	user = raw_input()
	pw = getpass.getpass()

yt_service = gdata.youtube.service.YouTubeService()

yt_service.developer_key = developer_key
yt_service.email = user
yt_service.password = pw

yt_service.ProgrammaticLogin()