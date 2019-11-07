from urllib.parse import urlparse
from tld import get_tld
import re
import tldextract
vowel = "aeiou"
consonant = 'bcdfghjklmnpqrstvwxyz'


def length_fqdn(url):
    parsed_uri = urlparse(url)
    result = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    print(result)
    if url[:5] == "https":
        return abs(len(result) - 8)
    else:
        return abs(len(result) - 7)

a=length_fqdn("https://www.google.com/search?client=ubuntu&channel=fs&q=re.findall%28%27%5B%25s%5D%27+%25+vowel%2C+url%29&ie=utf-8&oe=utf-8")
print(a)