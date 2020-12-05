import requests,random,json,time,webbrowser

#List of 4chan boards, and dict to act as a cache for already looked up board catalogs
boards = ['c']
cache  = {cache: '' for cache in boards}

#Returns [ random image URL, random image's thread URL ]
def r4chan():
    #Select a board
    board = random.choice(boards)

    #Request board catalog, and get get a list of threads on the board; then sleeping for 1.5 seconds
    threadnums = list()
    data = ''

    #If a board's catalog has already been requested, just use that stored data instead
    if (cache[board] != ''):
        data = cache[board]
    #else request the catalog, and sleep for 1.5 seconds; storing that data for future use
    else:
        data = (requests.get('http://a.4cdn.org/' + board + '/catalog.json')).json()
        cache[board] = data
        time.sleep(1.5)

    #Get a list of threads in the data
    for page in data:
        for thread in page["threads"]:
            threadnums.append(thread['no'])

    #Select a thread
    thread = random.choice(threadnums)

    #Request the thread information, and get a list of images in that thread; again sleeping for 1.5 seconds
    imgs = list()
    pd = (requests.get('http://a.4cdn.org/' + board + '/thread/' + str(thread) + '.json')).json()
    for post in pd['posts']:
        #Ignore key missing error on posts with no image
        try:
            imgs.append(str(post['tim']) + str(post['ext']))
        except:
            pass
    time.sleep(1.5)

    #Select an image
    image = random.choice(imgs)

    #Assemble and return the urls
    imageurl = 'https://i.4cdn.org/' + board + '/' + image
    return [imageurl]

#Opens x amount of image URLs in web browser; printing a link to the parent threads in console for reference
def main(numberOfImages):
    for i in range(numberOfImages):
        url = r4chan()
        webbrowser.open(url[0])
        time.sleep(1.5)

main(1)
