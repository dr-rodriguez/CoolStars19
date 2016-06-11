# Script to analyze and look at tweets from Cool Stars 19

from tweetloader import TweetLoader
from analysis import Analyzer
from helper_functions import print_dtm, top_factors, make_biplot
import pandas as pd
import matplotlib.pyplot as plt


# Load tweets
s2 = TweetLoader(filename='coolstars.json', track_location=False, path='coolstars19/data/')
s2.load()

df = s2.tweets.copy()
df.index = pd.DatetimeIndex(df['created_at'])

# Using the Analyzer class
max_words = 100
mod = Analyzer(df['text'], None, max_words=max_words, load_pca=False, load_svm=False,
               more_stop_words=['rt', 'cs19', 'cs19_uppsala'])

mod.get_words()
mod.create_dtm()
mod.run_pca()

# Exploration
print_dtm(mod.dtm, df['text'], 42)

# Top terms in components
top_factors(mod.load_squared, 0)

# Plots
make_biplot(mod.pcscores, None, mod.loadings, 0, 1)


# Loop plots
xval = range(0, 9, 2)
yval = [x+1 for x in xval]
for i, j in zip(xval, yval):
    make_biplot(mod.pcscores, None, mod.loadings, i, j)
    name = 'biplot_'+str(i)+'_'+str(j)+'.png'
    plt.savefig('coolstars19/figures/' + name)


