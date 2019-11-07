from urllib.parse import urlparse
from tld import get_tld
import re
import tldextract
vowel = "aeiou"
consonant = 'bcdfghjklmnpqrstvwxyz'

def protocol(url):
    if "https" in url[:5]:
        return 1
    else:
        return 0


def nof_vowels(url):
    return len(re.findall('[%s]' % vowel, url))


def nof_consonants(url):
    return len(re.findall('[%s]' % consonant, url))


def nof_special_sym(url):
    return len(re.findall(r"[~!@#$%^&*()_+{}\":;'\[\]]", url))

def nof_at(url):
    #return len(re.findall(r"[~!@#$%^&*()_+{}\":;'\[\]]", url))

    return url.count("@")


def nof_digits(url):
    return len(re.findall("\d", url))


def nof_alpha(url):
    return len(re.findall('[a-z,A-Z]', url))


def nof_alphanumeric(url):
    return nof_alpha(url) + nof_digits(url)


def nof_ques(url):
    return url.count("?")


def nof_dollar(url):
    return url.count("$")


def nof_percent(url):
    return url.count("%")


def nof_at(url):
    return url.count("@")


def nof_dash(url):
    return url.count("-")


def nof_dots(url):
    return url.count(".")


def nof_dir(url):
    return url.count("/")


def nof_www(url):
    return url.count("www")


def nof_http(url):
    return url.count("http")


def nof_eq(url):
    return url.count("=")


def vowel_consonant_ratio(url):
    try:
        return nof_consonants(url)/nof_vowels(url)
    except:
        return 0


def len_url(url):
    return len(url)


def length_fqdn(url):
    parsed_uri = urlparse(url)
    result = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    if url[:5] == "https":
        return abs(len(result) - 8)
    else:
        return abs(len(result) - 7)


def length_freeurl(url):
    return (len_url(url) - length_fqdn(url))


def dots_freeurl(url):
    if "https" in url[:5]:
        return nof_dots(url[(len_url(url) - length_freeurl(url) + 8):])
    else:
        return nof_dots(url[(len_url(url) - length_freeurl(url) + 7):])


def dig_in_hostname(url):
    if "https" in url[:5]:
        return len(re.findall('\d', url[:length_fqdn(url) + 8]))
    else:
        return len(re.findall('\d', url[:length_fqdn(url) + 7]))


def alph_digit_ratio(url):
    try:
        return float(nof_alpha(url)) /(nof_digits(url))
    except:
        return float(nof_alpha(url))


def host_dig_let_ratio(url):
    if "https" in url[:5]:
        return alph_digit_ratio(url[:length_fqdn(url) + 8])
    else:
        return alph_digit_ratio(url[:length_fqdn(url) + 7])


def subdomain_len(url):
    ext = tldextract.extract(url)
    return len(ext.subdomain)


def dash_in_path(url):
    parsed_uri = urlparse(url)
    return parsed_uri.path.count("/")


def terms_in_url(url):
    return len(re.findall(r"\w+", url))


def longest_token(url):
    mylist = list(re.findall(r"\w+", url))
    return len(max(mylist, key=len))


def longest_token_hostname(url):
    return longest_token(url[:length_fqdn(url) + 8])


def length_of_domains(url):
    a = tldextract.extract(url)
    return len(a.domain)


def terms_in_subdomain(url):
    ext = tldextract.extract(url)
    return len(re.findall(r"\w+", ext.subdomain))


#a=longest_token_hostname("https://www.google.com/search?client=ubuntu&channel=fs&q=re.findall%28%27%5B%25s%5D%27+%25+vowel%2C+url%29&ie=utf-8&oe=utf-8")
#print(a)