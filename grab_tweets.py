# Grab tweets

from tweetloader import TweetLoader

s2 = TweetLoader(filename='coolstars.json', track_location=False, path='coolstars19/data/')
s2.load()
query = '#CS19'
s2.search(query, 2000, hard_remove=False, remove_rts=False)

# Clean up spam
bad = s2.tweets['text'].str.contains('FOLLOW')
s2.tweets['text'][bad]
# If this has entries, clear them:
if sum(bad) > 0:
    s2.tweets = s2.tweets[~bad]
s2.save()