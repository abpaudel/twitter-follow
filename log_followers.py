import os
import datetime
import pandas as pd
import twitter #pip install python-twitter

# Go to https://apps.twitter.com and
# create a new app to get the keys and secret.

CONSUMER_KEY = 'your_key_here'
CONSUMER_SECRET = 'your_key_here'
ACCESS_TOKEN_KEY = 'your_key_here'
ACCESS_TOKEN_SECRET = 'your_key_here'

FILE = 'followers_data.csv'

api = twitter.Api(consumer_key=CONSUMER_KEY,
                  	consumer_secret=CONSUMER_SECRET,
                    access_token_key=ACCESS_TOKEN_KEY,
                    access_token_secret=ACCESS_TOKEN_SECRET)

api.VerifyCredentials()
try:
    followers = api.GetFollowers()
except twitter.error.TwitterError:
    print('Rate limit exceeded. Try again in 15 minutes.')
    exit()
followers = [x.screen_name for x in followers]
date = datetime.datetime.today().strftime('%Y-%m-%d')
followers_now = pd.DataFrame(followers, columns=[date])

try:
    followers_before = pd.read_csv(FILE)
except FileNotFoundError:
    print('Followers file not found. Creating new file ...')
    followers_now.to_csv(FILE, index=False)
    print(f'Current followers saved to {FILE}. Check back tomorrow.')
    exit()
except pd.errors.EmptyDataError:
    print(f'{FILE} is corrupted. Check/delete the file.')
    exit()

if followers_before.columns[-1]==date:
    if followers_before.shape[1]==1:
        print('Sorry, it\'s not tomorrow yet, you impatient bastard.')
        exit()
    followers_before.drop(date, axis=1, inplace=True)
final = pd.concat([followers_before,followers_now], axis=1)
final.to_csv(FILE, index=False)

old = set(final.iloc[:,-2])
new = set(final.iloc[:,-1])
unfl = list(old-new-{pd.np.nan})
newfl = list(new-old-{pd.np.nan})

print(f'{len(unfl)} people unfollowed you or deactivated their account:\n' + '\n'.join(unfl))
print(f'\n{len(newfl)} people followed you:\n' + '\n'.join(newfl))