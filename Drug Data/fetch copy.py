import praw
import pandas as pd
import datetime
import time


## OAUth
USER = 'smartypantsgc9'
CLIENT_ID = 'r3kQmrl358DZAw'
CLIENT_SECRET = 'vwSt2kzzOJqSziRZzCoQz_oKFAY'
REDIR = 'http://127.0.0.1:8080'



## Subreddits to search through
SUBREDDITS = ['drugs', 'researchchemicals']

## Query
QUERIES = ['xanax', 'opiate', 'opioid', 'best', 'fentanyl', 'heroin', 'adderall', 'amps', 'speed', 'amphetamine', 'stims', 'stimulant', 'hydro', 'oxy', 'hydrocodone', 'oxycodone', 'subs', 'suboxone', 'xannies']



## Search Params
SORT='comments'
SYNTAX='lucene'
TIME='year'



## sign in
r = praw.Reddit(user_agent=USER,client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET, redirect_uri=REDIR)





for SUBREDDIT in SUBREDDITS:

    subreddit = r.subreddit(SUBREDDIT)
    
    for QUERY in QUERIES:
        print(SUBREDDIT, QUERY)

        submissions = {}

        ## fetch all of the self posts relating to query
        for submission in subreddit.search(QUERY,sort=SORT, syntax=SYNTAX, time_filter=TIME ):

            comment_corpus = ''
            
            ## loop thru comments for thread
            for i in submission.comments:
                try:
                    ## add comment text
                    comment_corpus += i.body
                except:

                    ## figure out how to get all comments, even the most nested
                    print(i.comments)




            ## collect relevent info
            submission_info = {'text': submission.selftext,
                               'author': submission.author.name,
                               'score':submission.score,
                               'flair': submission.link_flair_text,
                               'created':submission.created,
                               'url':submission.url,
                               'num_comments':submission.num_comments,
                               'comment_corpus': comment_corpus}


            ## add to dat
            submissions[submission.id] = submission_info



        pd.DataFrame(submissions).transpose().to_json( SUBREDDIT + '_' + QUERY + '_' + TIME + '.json')
        time.sleep(1)
