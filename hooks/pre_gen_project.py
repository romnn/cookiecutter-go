import re
import sys

URL_REGEX = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

package = "{{ cookiecutter.public_import_path }}"
mock_url = "https://%s" % package

if not (re.match(URL_REGEX, mock_url) is not None):
    print(
        "ERROR: The packages import path (%s) is not a valid URL."
        % mock_url
    )

    # Exit to cancel project
    sys.exit(1)
