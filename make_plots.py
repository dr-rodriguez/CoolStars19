# Make some plots

from tweetloader import TweetLoader
import matplotlib.pyplot as plt
import matplotlib.dates as dates
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from scipy.misc import imread
import pandas as pd

s2 = TweetLoader(filename='coolstars.json', track_location=False, path='coolstars19/data/')
s2.load()

df = s2.tweets.copy()
df.index = pd.DatetimeIndex(df['created_at'])

# Make a word cloud
words = ' '.join(df['text'])

# Remove URLs, 'RT' text, screen names, etc
my_stopwords = ['RT', 'amp', 'lt']
words_no_urls = ' '.join([word for word in words.split()
                          if 'http' not in word and word not in my_stopwords and not word.startswith('@')
                          ])

# Add stopwords, if needed
stopwords = STOPWORDS.copy()
stopwords.add("RT")
stopwords.add('amp')
stopwords.add('lt')

# Load up a logo as a mask & color image
logo = imread('coolstars19/logos/bd_white.jpg')

# Generate colors
image_colors = ImageColorGenerator(logo)

# Generate plot
wc = WordCloud(stopwords=stopwords, mask=logo, color_func=image_colors, scale=0.8,
               max_words=200, background_color='white', random_state=42, prefer_horizontal=0.95)

wc.generate(words_no_urls)

size = 10
plt.figure(figsize=(size, size))
plt.imshow(wc)
plt.axis("off")
plt.savefig('coolstars19/figures/word_cloud.png')


# Tweets per hour
df = df.sort_index()

rng = pd.date_range('2016-6-1', '2016-6-13 16:00:00', freq='H')
counts = []
for i in range(len(rng)-1):
    num = df['id'][rng[i]:rng[i+1]].count()
    counts.append(num)
    # print('{0} - {1}: {2}'.format(rng[i], rng[i+1], num))

# Chart tweets with time
fig, ax = plt.subplots()
ax.plot_date(rng[1:], counts, '-', lw=2)
ax.set_ylabel('Number of Tweets')
# ax.xaxis.set_minor_locator(dates.WeekdayLocator(byweekday=(1), interval=1))  # Once per week
ax.xaxis.set_minor_locator(dates.DayLocator(interval=1))
ax.xaxis.set_minor_formatter(dates.DateFormatter('%d\n%a'))
# ax.xaxis.grid(True, which="minor")
# ax.yaxis.grid()
ax.xaxis.set_major_locator(dates.MonthLocator())
ax.xaxis.set_major_formatter(dates.DateFormatter('\n\n\n%b\n%Y'))
plt.tight_layout()

plt.savefig('coolstars19/figures/tweets_time.png')

# Add word cloud for fun
newax = fig.add_axes([0.04, 0.3, 0.52, 0.52], zorder=10)
newax.imshow(wc)
newax.axis('off')

plt.savefig('coolstars19/figures/tweets_time_cloud.png', dpi=200)  # Increased DPI to make the cloud more readable

