import praw
import pandas as pd
import datetime
import time
import pprint
from praw.models import MoreComments
import json
## OAUth
USER = 'smartypantsgc9'
CLIENT_ID = 'r3kQmrl358DZAw'
CLIENT_SECRET = 'vwSt2kzzOJqSziRZzCoQz_oKFAY'
REDIR = 'http://127.0.0.1:8080'
SYNTAX='lucene'



## Subreddits to search through
SUBREDDITS = ['drugs', 'researchchemicals']

## Query
QUERIES = ['xanax', 'opiate', 'opioid', 'best', 'fentanyl', 'heroin', 'adderall', 'amps', 'speed', 'amphetamine', 'stims', 'stimulant', 'hydro', 'oxy', 'hydrocodone', 'oxycodone', 'subs', 'suboxone', 'xannies']




## Search Params
SORT='comments'
TIME='all'



## sign in
r = praw.Reddit(user_agent=USER,client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET, redirect_uri=REDIR)




def process_comment_forest(commentForest):
    current_level = {}
    for topLevelComment in commentForest:
        try:
            current_level[topLevelComment.id] = {'score': topLevelComment.score, 'link':topLevelComment.permalink, 'is_submitter': topLevelComment.is_submitter, 'created': topLevelComment.created, 'body':topLevelComment.body, 'replies': process_comment_forest(topLevelComment.replies)}
        except:
            try:
                for n in topLevelComment.comments():
                    current_level[n.id] = {'score': n.score, 'link':n.permalink, 'is_submitter': n.is_submitter, 'created': n.created, 'body':n.body, 'replies': process_comment_forest(n.replies)}
            except:
                break
    return current_level




test = []
for SUBREDDIT in SUBREDDITS:
    subreddit = r.subreddit(SUBREDDIT)
    for QUERY in QUERIES:
        submissions = {}
        ## fetch all of the self posts relating to query
        for submission in subreddit.search(QUERY,sort=SORT, syntax=SYNTAX, time_filter=TIME ):
            processed_comments = process_comment_forest(submission.comments)

            ## collect relevent info
            submission_info = {'text': submission.selftext,
                               'author': submission.author.name,
                               'score':submission.score,
                               'flair': submission.link_flair_text,
                               'created':submission.created,
                               'url':submission.url,
                               'num_comments':submission.num_comments,
                               'title': submission.title,
                                'subreddit': SUBREDDIT,
                                'comments': processed_comments}

            ## add to data
            submissions[submission.id] = submission_info



        with open(SUBREDDIT + '_' + QUERY + '_' + TIME + '.json', 'w') as outfile:
            json.dump(submissions, outfile)
        print('done' + SUBREDDIT+QUERY)
        time.sleep(1)
