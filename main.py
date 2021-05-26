import ssl
import urllib.request
import re
import threading

phishingfeed = 'https://openphish.com/feed.txt'
sslContext = ssl.create_default_context()
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
ssl_context.verify_mode = ssl.CERT_NONE
ssl_context.check_hostname = False
ssl_context.load_default_certs()
https_handler = urllib.request.HTTPSHandler(context=ssl_context)
opener = urllib.request.build_opener(https_handler)


xbaltilinks = []
indexlinks = []

def check(url):

    #f = str(urllib.request.urlopen(url, timeout=5,context=sslContext ).read())
    f = str(opener.open(url, timeout=5).read())
    resultXBALTI = re.findall(r'XBALTI',f)
    resultINDEX = re.findall(r'Index',f)

    if(resultXBALTI.__len__()!=0):
        print(":XBALTI Found")
        xbaltilinks.append(url)
        return True

    if (resultINDEX.__len__()!=0):
        print(":Index Found")
        indexlinks.append(url)
        return True

    substrindex = url.__len__() - url.rfind('/')

    if substrindex <1:
        return False
    else:
        substr = url[:-substrindex]
        print("Current substr is ", substr)
        check(substr)

def getlinks():
    f = str(urllib.request.urlopen(phishingfeed).read())
    linksarray = f.split("\\n")
    i = 0
    print("Found ",  linksarray.__len__(), "links")


    for link in linksarray:
       print(i,'/',linksarray.__len__())
       try:
            i += 1
            if check(link):
                print(i,"Founded, url:", link )
            else:
                print(i, "Nothing Found")

       except Exception as ex:
           print(i, "Error , ", ex.args)

    print("Xbalti founded: ", xbaltilinks.__len__())
    print(xbaltilinks)

    print("index links founded: ", indexlinks.__len__())
    print(indexlinks)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    getlinks()


