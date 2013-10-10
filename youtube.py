import gdata.youtube
import gdata.youtube.service
import getpass
from wordpress_xmlrpc import Client, WordPressPost, WordPressTerm
from wordpress_xmlrpc.methods import taxonomies
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost, EditPost
from wordpress_xmlrpc.methods.users import GetUserInfo

youtube = True

"""
Quick script I wrote to post a bunch of pregnancy by week videos.
Planning to update to imporve MedTwice automation
Need to save SecureFiles as encrypted data, load and decrypt on password
"""

if youtube:
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
	yt_service.client_id = 'MedTwicePoster'

	yt_service.ProgrammaticLogin()

	# print developer_key

	uri ='https://gdata.youtube.com/feeds/api/users/default/uploads'

	entries = []
	def GetVideoEntries(uri,numEntries):
		feed = yt_service.GetYouTubeVideoFeed(uri + '?max-results=' + str(numEntries))
		for entry in feed.entry:
			entries.append(entry)

	GetVideoEntries(uri,38)

	entries = entries[::-1]
	urls = [entry.media.player.url[32:43] for entry in entries]
	titles = [entry.media.title.text for entry in entries]
	print urls
	# print [entry.media.title.text for entry in entries]

	def updateTitles():
		for i in range(4,42):
			print entries[i-4].media.title.text
			title = 'Pregnancy by Weeks - Week ' + str(i)
			entries[i-4].media.title.text = title
			print title
			yt_service.UpdateVideoEntry(entries[i-4])

	def updateDescriptions():
		for i in range(4,42):
			description = 'For more information and related videos: \
http://medtwice.com/pregnancy-by-weeks-week-'+str(i)
			print description
			entries[i-4].media.description.text = description
			yt_service.UpdateVideoEntry(entries[i-4])

	urls = urls[::-1]
	titles = titles[::-1]


#wordpress section
user,pw = eval(open('/Users/JAG/Dropbox/Workspace/SecureFiles/WPData.ignore','r').read())

wp = Client('http://medtwice.com/xmlrpc.php',user,pw)
taxes = wp.call(taxonomies.GetTaxonomies())


def wordPressPost():
	for i in range(38):
		content = """<iframe src="//www.youtube-nocookie.com/embed/""" + urls[i] + """?rel=0" \
height="360" width="640" allowfullscreen="" frameborder="0"></iframe>"""

		post = WordPressPost()
		post.title = titles[i]
		post.content = content
		print titles[i]
		print content
		post.link = 'http://medtwice.com/pregnancy-by-week-week-'+str(i+4)
		post.post_status = 'publish'
		category = wp.call(taxonomies.GetTerm('category', 44))
		post.terms.append(category)
		post.id = wp.call(NewPost(post))


# wordPressPost()
def updatePosts():
	posts = wp.call(GetPosts({'number':38}))
	i = 3
	for post in posts:
		i += 1
		post.slug = 'pregnancy-by-weeks-week-' + str(i)
		post.title = 'Pregnancy By Weeks - Week ' + str(i)
		wp.call(EditPost(post.id, post))
		print post.slug







