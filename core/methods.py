# START Custom Global Methods Settings
def standardResponse(data=[], errors=[], **kwargs):
    return {"data":data, "errors":errors}

def pagination(page):
    if page:
        page = int(page)
        items_per_page = 5
        offset = (page - 1) * items_per_page
        limit = page * items_per_page
        return ( offset, limit )
    else:
        return False
# END Custom Global Methods Settings

# START Stackoverflow Snippet

# Source: http://stackoverflow.com/questions/2268417expire-a-view-cache-in-django/36845722#36845722
# Removes a cache of a certain page
# JUST USED A MANUAL CACHE as it is more flexible
# def invalidate_cache(path=''):
# 	''' this function uses Django's caching function get_cache_key(). Since 1.7, 
#       Django has used more variables from the request object (scheme, host, 
#       path, and query string) in order to create the MD5 hashed part of the
#       cache_key. Additionally, Django will use your server's timezone and 
#       language as properties as well. If internationalization is important to
#       your application, you will most likely need to adapt this function to
#       handle that appropriately.
#   '''
# 	from django.core.cache import cache
# 	from django.http import HttpRequest
# 	from django.utils.cache import get_cache_key
# 	import sys

# 	# Bootstrap request:
#   # request.path should point to the view endpoint you want to invalidate
#   # request.META must include the correct SERVER_NAME and SERVER_PORT as django uses these in order
#   # to build a MD5 hashed value for the cache_key. Similarly, we need to artificially set the 
#   # language code on the request to 'en-us' to match the initial creation of the cache_key. 
#   # YMMV regarding the language code.
# 	request = HttpRequest()
# 	request.META = {'HTTP_HOST':'localhost','SERVER_PORT':8000}
# 	request.LANGUAGE_CODE = 'en-us'
# 	request.path = path

# 	try:
# 		cache_key = get_cache_key(request)
# 		print "////"
# 		print cache_key
# 		if cache_key:
# 			print "dean"
# 			if cache.has_key(cache_key):
# 				print "armada"
# 				cache.delete(cache_key)
# 		else:
# 			raise ValueError('failed to create cache_key')
# 	except (ValueError, Exception) as e:
# 		print "guinto"
# 		print "%s - %s at line %s" % (sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2].tb_lineno)
# 		pass
# END Stackoverflow Snippet