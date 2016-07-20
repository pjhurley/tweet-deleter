import tweepy
import thread

# Twitter credentials found on 'developer' section go here.
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""

class myDate():
    month = 0
    year = 0

    def __init__(self, month, year):
        if month == 'Jan':
            self.month = 1
        elif month == 'Feb':
            self.month = 2
        elif month == 'Mar':
            self.month = 3
        elif month == 'Apr':
            self.month = 4
        elif month == 'May':
            self.month = 5
        elif month == 'Jun':
            self.month = 6
        elif month == 'Jul':
            self.month = 7
        elif month == 'Aug':
            self.month = 8
        elif month == 'Sep':
            self.month = 9
        elif month == 'Oct':
            self.month = 10
        elif month == 'Nov':
            self.month = 11
        elif month == 'Dec':
            self.month = 12
        self.year = year

def oauth_login(consumer_key, consumer_secret):
    #Authenticate with twitter using OAuth

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth_url = auth.get_authorization_url()

    verify_code = raw_input("Authenticate at %s and then enter you verification code here > " % auth_url)
    auth.get_access_token(verify_code)

    return tweepy.API(auth)

def isEarlierThan(deleteDate, tweetDate):
    if deleteDate.year < tweetDate.year:
        return 0
    elif deleteDate.year == tweetDate.year:
        if deleteDate.month < tweetDate.month:
            return 0
        else:
            return 1
    else:
        return 1

def deleteThread(api, objectID):
    try:
        api.destroy_status(objectID)
        print "Deleted: ", objectID
    except:
        print "Failed to delete: ", objectID

def deleteTweets(api, deleteDate):
    print "I am about to delete all tweets before your specified date. Type 'delete' to continue with the deletion process."
    yesORno = raw_input("> ")
    if yesORno.lower() == 'delete':
        for status in tweepy.Cursor(api.user_timeline).items():
            tweetDate = myDate(status.created_at.month, status.created_at.year)
            if isEarlierThan(deleteDate, tweetDate) == 1:
                try:
                    api.destroy_status(status.id)
                    print "Deleted: ", status.id
                except:
                    print "Failed to delete: ", status.id

def main():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    print "Authentification complete. Welcome, %s." %api.me().screen_name
    year = raw_input("From what year should I start deleting tweets? > ")
    month = raw_input("Enter a month in numerical representation (1-12). > ")
    deleteDate = myDate(int(month), int(year))
    deleteTweets(api, deleteDate)

if __name__ == '__main__': main()
