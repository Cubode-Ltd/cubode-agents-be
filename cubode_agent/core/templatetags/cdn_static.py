from django import template
from django.conf import settings
from django.templatetags.static import static

## READ THIS IF YOU DONT KNOW WHAT IT IS:
# Custom template tag for serving static files.
#
# This tag is designed to differentiate between CSS files and other static files.
# In this configuration the server is serving the css files, and the cdn of aws is serving the rest of files.
# that is why its needed that the html templates can point to the cdn url (for js, imgs, media...) or to the server url (for css)

# The main purpose of this whole development was to avoid the css CORS in the js files when importing css files 


# When rendering templates, the 'cdn_static' tag checks if the requested static file is a CSS file
# (by examining if the path starts with 'css/'). 
#
# - If it is a CSS file, the tag returns a URL pointing to the local CSS files served by Nginx,
#   using the 'CSS_STATIC_URL' defined in the Django settings.
# - For all other static files, the tag returns a URL that points to the CDN where these files
#   are hosted, using the standard 'STATIC_URL'.
#
# This approach allows you to serve CSS files directly from your server via Nginx, while other
# static files are served from a CDN, optimizing both performance and resource delivery.

register = template.Library()

@register.simple_tag
def cdn_static(path):
    if path.startswith('css/'):
        return f"{settings.CSS_STATIC_URL}{path[4:]}"
    return f"{settings.STATIC_URL}{path}"
