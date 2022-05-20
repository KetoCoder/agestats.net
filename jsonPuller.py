
'''
This one stores all of the JSON results from the API!
'''

import json
import requests
import time

# Default timestamp picked is one second before the first reported game of Age of Empires 2 DE.
# 1575463332

data = None

# The "librarian" stores the most recent tome index and game time,
# so that way we can pick up where we left off if it gets interrupted
# or gets all the available data.  Max tome size is 1000.
LIBRARIANPATH = "librarian.txt"
TOMESIZE = 1000

lib = open(LIBRARIANPATH, "r")
libdata = lib.readlines()
lib.close()
index = 0
lasttime = 1575463332

# We have the defaults set above, but let's get them from the librarian if they're there.
if len(libdata) > 0:
    index = int(libdata[0])
    lasttime = int(libdata[1])

# Looping as long as we either just started or we're getting 1000 results
while data == None or len(data) == TOMESIZE:

    # Build the API link that'll give us the data, and then get it
    urlhook = f"https://aoe2.net/api/matches?game=aoe2de&count={TOMESIZE}&since={lasttime}"
    data = requests.get(url = urlhook).json()

    # Write it to a file (it'll go in the same directory as this program)
    tomepath = f"tome_{index}.txt"
    tome = open(tomepath, "w")
    tome.write(json.dumps(data))
    tome.close()
    
    # Now we need to find the highest game time in our JSON;
    # it's not necessarily the last game, as they're not ordered by time
    maxtime = 0
    
    tome = open(tomepath, "r")
    tomedata = json.loads(tome.readlines()[0])
    
    for game in tomedata:
        gametime = game["opened"]
        if gametime > maxtime:
            maxtime = gametime
    
    lasttime = maxtime
    
    # We did it!  Let the user know it was successful.
    print(f"Tome {index} has been written!  Includes games up to timestamp {lasttime}.")
    
    index += 1
    
    # Write the new time and index out to the librarian
    if len(data) == TOMESIZE:
        lib = open(LIBRARIANPATH, "w")
        lib.write(str(index))
        lib.write('\n')
        lib.write(str(lasttime))
        lib.close()
