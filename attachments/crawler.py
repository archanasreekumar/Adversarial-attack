import sys
import os
import csv
import requests
import datetime
import json
import socket
import ssl
import tldextract
from selenium import webdriver
#sample comment
# from selenium.common.exceptions import InvalidSessionIdException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import ScreenshotException
from selenium.common.exceptions import WebDriverException
from interruptingcow import timeout

## using this to squash warnings, but I think this is a current bug in URLLib3 maybe fixed in future
## See this : https://github.com/SeleniumHQ/selenium/issues/6869
## TODO update Urlib so we don't have to supress these warnings in future.

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def print_url(request_object, *args, **kwargs):
    redirects.append(request_object.url)
    # TODO there must be a better more code readable way to do this.


def getcert(addr, timeout=None):
    try:
        with socket.create_connection(addr, timeout=timeout) as sock:
            context = ssl.create_default_context()
            with context.wrap_socket(sock, server_hostname=addr[0]) as sslsock:
                return sslsock.getpeercert()
    except (ValueError, socket.error, socket.gaierror, socket.herror, socket.timeout):
        return "NaN"

input_file = sys.argv[1]
output_file = sys.argv[2]
os.system('mkdir {}'.format(output_file))
source_file = open(input_file, 'r+')

###customizing chrome driver using selenium
options = webdriver.ChromeOptions()
WINDOW_SIZE = "1920,1080"
prefs = {"profile.default_content_setting_values.notifications": 0}
options.add_experimental_option("prefs", prefs)
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-running-insecure-content')
options.add_argument('--headless')
options.add_argument('--window-size=%s' % WINDOW_SIZE)
options.add_argument('--no-sandbox')


with open(output_file + ".csv", 'a', encoding='utf-8') as destination:
    writer = csv.writer(destination)

    for url in source_file.readlines():
        url = url.rstrip()
        print(url)
        try:
            with timeout(300, exception=RuntimeError):

                ### REQUESTS TRY
                try:
                    redirects = []
                    req = requests.get(url, verify=False, hooks={'response': print_url})#false--> no certificate verification,hook-->response- stores the response
                    header_info = req.headers
                    request_history = req.history
                    if not redirects:  # pythonic way to check for empty lists.
                        redirects = "NaN"
                except requests.exceptions.RequestException:
                    print("Request timed out")
                    redirects, header_info, request_history = "NaN", "NaN", "NaN"
                except Exception:
                    redirects, header_info, request_history = "NaN", "NaN", "NaN"

                ### TLDextract TRY
                if url[:5].lower() == 'https':  # more robust check for HTTPS
                    try:
                        a_list = tldextract.extract(url)
                        domain_name = a_list.domain + '.' + a_list.suffix
                        # print(domain_name) ## not sure why this was printing, we don't need it
                        certificate_information = (json.dumps(getcert((domain_name, 443)), indent=2, sort_keys=True))

                    except ssl.SSLError:
                        print("An SSL exception Occured")
                        certificate_information = "NaN"  # keep variable names the same type, certs are strings,
                                                          # so the none on this should be a string.
                else:
                    certificate_information = "NaN"

                ### SELENIUM TRY
                try:
                    # Create the web driver
                    driver = webdriver.Chrome(options=options)
                    driver.set_page_load_timeout(60)
#                    driver.implicitly_wait(3)
                    driver.get(url)
                    driver.implicitly_wait(15)
                    title = driver.title
                    source_code = driver.page_source
                except UnexpectedAlertPresentException:
                    print("Java Script Present")

                except TimeoutException:
                    print("A Selenium Timeout Exception Occured")
                    if driver.service.process is not None:
                        continue
                    else:
                        driver.quit()
                        driver = webdriver.Chrome(options=options)
                        continue

                except WebDriverException as wbe:
                    print("Selenium exception that is : {}".format(wbe))
                    if driver.service.process is not None:
                        continue
                    else:
                        driver.quit()
                        driver = webdriver.Chrome(options=options)

                ### Screenshot TRY
                try:
                    date_stamp = str(datetime.datetime.now()).split('.')[0]
                    date_stamp = date_stamp.replace(" ", "_").replace(":", "_").replace("-", "_")
                    file_name = date_stamp + ".png"
                    driver.save_screenshot(file_name)
                    os.system('mv {} {}'.format(file_name, output_file))
                except ScreenshotException:
                    print("Error in getting Screenshot")
                    file_name = "NaN"

                except TimeoutException:
                    print("A Selenium Timeout Exception Occured")
                    if driver.service.process is not None:
                        continue
                    else:
                        driver.quit()
                        driver = webdriver.Chrome(options=options)
                        continue

                ### SAVE TO FILE!
                try:
                    title
                except NameError:
                    title = "NaN"
                try:
                    source_code
                except NameError:
                    source_code = "NaN"

                packed_contents = [str(datetime.datetime.now()), url.rstrip(), title, source_code,
                                   redirects, request_history, header_info, file_name, certificate_information]
                writer.writerow(packed_contents)
                driver.quit()
        except RuntimeError:
            print("Intterupting Cow Runtime Error \n {} \n taking too long to process".format(url))
            driver.quit()
        except UnexpectedAlertPresentException:
            print("Java Script Present")
