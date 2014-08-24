#!/usr/bin/env python

"""
    Thanks for the birthday greetings!
"""
import facebook
import requests
import re
import time

fb_access_token = ""
birthday_celebrant = "Ferdinand Silva"
code_url = "https://github.com/six519/thanks_to_birthday_greetings"

global_post_count = 0
global_is_done = False
global_fb_graph = None

def getPostData(url):
    ret = None
    try:
        req = requests.get(url)
        ret = req.json()
    except Exception as e:
        print "The error is: %s" % str(e)
    
    return ret

def parsePostData(posts):
    global global_post_count, global_is_done, global_data_storage

    try:

        for dat in posts["data"]:

            if re.search("^(2014-08-23|2014-08-24|2014-08-23|2014-08-22)",str(dat.get("created_time")).strip()):

                if (str(dat.get("type")) == "status" or str(dat.get("type")) == "photo") and str(dat.get("from")["name"].encode('utf-8', 'ignore')) != birthday_celebrant: 

                    global_post_count += 1

                    print "From: %s" % str(dat.get("from")["name"].encode('utf-8', 'ignore'))
                    print "Message: %s\n\n" % str(dat.get("message").encode('utf-8', 'ignore'))

                    global_fb_graph.put_comment(dat.get("id"), "Thanks %s! :)" % str(dat.get("from")["name"].encode('utf-8', 'ignore')))
                    global_fb_graph.put_like(dat.get("id"))

            else:
                global_is_done = True
                break

        if not global_is_done:

            next_posts = getPostData(posts["paging"]["next"])
            parsePostData(next_posts)
        else:
            global_fb_graph.put_object("me", "feed", message="Slamat po s %s ktaong bmati at nakaalala sa bday ko.Ang mensaheng i2 ay awtomatiko at pti n rin ang bwat isng likes/passlamat ko sa pagbati nyo.Paumanhin s mga hndi malalike/mappaslmatan ng code kong i2 at maaring may 'BUG' pa cya. %s" % (global_post_count, code_url))
            print "\n\nTotal greetings count: %s" % global_post_count

    except Exception as e:
        print "The error is: %s" % str(e)

if __name__ == "__main__":
    
    global_fb_graph = facebook.GraphAPI(fb_access_token)
    my_profile = global_fb_graph.get_object("me")

    first_page_posts = global_fb_graph.get_connections(my_profile['id'], 'feed')
    parsePostData(first_page_posts)

