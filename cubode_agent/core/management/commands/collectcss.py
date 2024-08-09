from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.staticfiles import finders
from django.core.files.storage import get_storage_class

## READ THIS IF YOU DONT KNOW WHAT IT IS:
# Custom management command for Django to selectively collect CSS files.
# 
# This command is used to collect CSS static files into the local 'staticfiles/css/' directory,
# allowing them to be served directly by Nginx in a production environment.
# 
# In this setup, the standard Django 'collectstatic' command collects and uploads other static files 
# (like JavaScript, images, etc.) to an AWS S3 bucket to be served via a CDN.
# 
# The 'collectcss' command ensures that CSS files remain local and are served efficiently 
# by Nginx, which is beneficial for scenarios where CSS files need to be served with lower latency 
# or specific configurations not easily achievable via the CDN.

# This code is needed so that the CSS files are served from the server
# and have the same CORS.

# Example Use Case
# Suppose you have the following file structure in your project:

# static/
#     css/
#         style.css
#         main.css
#     js/
#         app.js
# When you run python manage.py collectcss, the command will:

# Find all files under static/css/.
# Copy style.css and main.css to staticfiles/css/style.css and staticfiles/css/main.css, respectively.
# Leave other files (e.g., js/app.js) untouched, as they do not reside in the css/ directory.
# This setup is useful in scenarios where you want Nginx to serve the CSS files directly from your server, while other static files might be served from a CDN or another storage backend.



class Command(BaseCommand):
    help = 'Collects CSS files to be served by Nginx'

    def handle(self, *args, **kwargs):
        # Retrieve the custom storage class for CSS files as defined in the Django settings.
        # This storage class specifies where and how the CSS files will be stored.
        storage = get_storage_class(settings.CSS_FILE_STORAGE)()

        # Iterate over all the configured static file finders.
        # Static file finders are responsible for locating static files in the project's directories.
        for finder in finders.get_finders():
            for path, storage_instance in finder.list([]):
                if path.startswith('css/'):
                    # Get the absolute path to the file
                    source_path = finder.find(path)
                    if source_path:
                        # Remove the first 'css/' prefix
                        relative_path = path[len('css/'):]
                        
                        # Save the file directly under 'staticfiles/css/'
                        destination_path = relative_path
                        
                        with open(source_path, 'rb') as file:
                            storage.save(destination_path, file)
                            self.stdout.write(f'Copied {path} to {destination_path}')
