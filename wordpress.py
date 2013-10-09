from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.methods.users import GetUserInfo

user,pw = eval(open('/Users/JAG/Dropbox/Workspace/SecureFiles/WPData.ignore','r').read())

wp = Client('http://medtwice.com/xmlrpc.php',user,pw)

# posts = wp.call(GetPosts())