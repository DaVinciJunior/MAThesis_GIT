from datetime import datetime
import praw

import sentHelper


def login():
    # contains your login info comma-separated params: client_id, client_secret, user_agent
    login_data = open("res/login-data.txt", "r")
    my_params = login_data.read().split(',')
    my_client_id = my_params[0]
    my_client_secret = my_params[1]
    my_user_agent = my_params[2]
    return praw.Reddit(
        # insert login info here
        client_id=my_client_id,
        client_secret=my_client_secret,
        user_agent=my_user_agent
    )

def prettyPrinterComments(comment, sentiment, prefix):
    id = ""
    user = ""
    score = ""
    time = ""
    text = ""
    num_replies = ""
    try:
        id = str(comment.id)
    except:
        id = "Faulty-Id"
    try:
        user = comment.author.name
    except:
        user = "Faulty-User-Name"
    try:
        score = str(comment.score)
    except:
        score = "Faulty-Score"
    try:
        time = datetime.utcfromtimestamp(int(comment.created_utc)).strftime("%d.%m.%y %H:%M:%S")
    except:
        time = "Faulty-Time"
    try:
        text = comment.body.replace("\n", "\n" + prefix)
    except:
        text = "Faulty-Textbody"
    try:
        num_replies = str(comment.replies.__len__())
    except:
        num_replies = "Faulty-Num-Replies"

    if user == "BOT":
        print(prefix + "BOT Message ignored...")
        return

    if user == "NON-GERMAN-COMMENT":
        print(prefix + "Non German Message ignored...")
        return

    print(prefix + "<" + id + ">" + user + "[" + score + "]" + "{" + time + "}" + "#" + num_replies + " " + text, end='\n')
    if sentiment != None:
        print(prefix + str(sentiment))

def prettyPrinterSubmissions(submission):
    id = ""
    user = ""
    score = ""
    time = ""
    title = ""
    upvote_ratio = ""
    numberOfComments = ""

    try:
        id = str(submission.id)
    except:
        id = "Faulty-Id"
    try:
        user = submission.author.name
    except:
        user = "Faulty-User-Name"
    try:
        score = str(submission.score)
    except:
        score = "Faulty-Score"
    try:
        upvote_ratio = str(submission.upvote_ratio)
    except:
        upvote_ratio = "Faulty-Upvote-Ratio"
    try:
        time = datetime.utcfromtimestamp(int(submission.created_utc)).strftime("%d.%m.%y %H:%M:%S")
    except:
        time = "Faulty-Time"
    try:
        title = submission.title
    except:
        title = "Faulty-Textbody"
    try:
        numberOfComments = str(submission.num_comments)
    except:
        numberOfComments = "Faulty-Number-of-comments"

    print("<" + id + ">" + user + "[" + score + "-" + upvote_ratio + "]" + "{" + time + "}" + title + " #" + numberOfComments)

def outputAllReplies(comment, func, prefix, preprocess=True):
    for reply in comment.replies:
        if preprocess:
            reply = sentHelper.preprocessComments(reply)
        sentiment = None
        if func != None:
            sentiment = func(comment.body)
        prettyPrinterComments(reply, sentiment, prefix)
        outputAllReplies(reply, func, prefix + "\t")

def outputAllRepliesFeatureFunc(comment, func, prefix, preprocess=True, submission=None):
    for reply in comment.replies:
        if preprocess:
            reply = sentHelper.preprocessComments(reply)
        sentiment = None
        if func != None:
            sentiment = func(reply.body, reply.score, reply.replies.__len__(), str(submission.id), str(reply.id))
        # prettyPrinterComments(reply, sentiment, prefix)
        outputAllRepliesFeatureFunc(reply, func, prefix, preprocess, submission)

# default: n = 100
def get_n_LatestSubmissionsAndComments(n=100):
    get_n_LatestSubmissionsAndCommentsAndExecuteFunction(n=n)


def get_n_LatestSubmissionsAndCommentsAndExecuteFunction(n=100, func=None, preprocess=True):
    reddit = login()
    subreddit = reddit.subreddit("Austria")
    for submission in subreddit.new(limit=n):
        print("--------------------------")
        prettyPrinterSubmissions(submission)
        print("------------------------------")
        submission.comments.replace_more(limit=0)
        for top_level_comment in submission.comments:
            if preprocess:
                top_level_comment = sentHelper.preprocessComments(top_level_comment)
            sentiment = None
            if (func != None):
                sentiment = func(top_level_comment.body)
            prettyPrinterComments(top_level_comment, sentiment, "\t")
            outputAllReplies(top_level_comment, func, "\t\t", preprocess)
        print("\n\n---\n\n")

def get_n_LatestSubmissionsInHotAndCommentsAndExecuteFunction(n=100, func=None, preprocess=True):
    reddit = login()
    subreddit = reddit.subreddit("Austria")
    for submission in subreddit.hot(limit=n):
        print("--------------------------")
        prettyPrinterSubmissions(submission)
        print("------------------------------")
        submission.comments.replace_more(limit=0)
        for top_level_comment in submission.comments:
            if preprocess:
                top_level_comment = sentHelper.preprocessComments(top_level_comment)
            sentiment = None
            if (func != None):
                sentiment = func(top_level_comment.body)
            prettyPrinterComments(top_level_comment, sentiment, "\t")
            outputAllReplies(top_level_comment, func, "\t\t", preprocess)
        print("\n\n---\n\n")

def get_n_LatestSubmissionsAndCommentsAndExecuteFeatureFunction(n=100, func=None, preprocess=True):
    reddit = login()
    subreddit = reddit.subreddit("Austria")
    for submission in subreddit.new(limit=n):
    # for submission in subreddit.hot(limit=n):
        # print("--------------------------")
        # prettyPrinterSubmissions(submission)
        # print("------------------------------")
        submission.comments.replace_more(limit=0)
        for top_level_comment in submission.comments:
            if preprocess:
                top_level_comment = sentHelper.preprocessComments(top_level_comment)
            sentiment = None
            if (func != None):
                sentiment = func(top_level_comment.body, top_level_comment.score, top_level_comment.replies.__len__(), str(submission.id), str(top_level_comment.id))
            # prettyPrinterComments(top_level_comment, sentiment, "\t")
            outputAllRepliesFeatureFunc(top_level_comment, func, "\t\t", preprocess, submission)
        # print("\n\n---\n\n")


    ################### FAILED EXPERIMENTS ###################


# Research Notes: 26.10.2021 Tested over multiple days over multiple times - to no avail
# Tested features: mod_note, mod_reason_by, mod_reason_title, mod_reports, num_reports, removal_reason, removed_by, report_reasons
def findAVariantSubmission():
    reddit = login()
    subreddit = reddit.subreddit("Austria")
    for submission in subreddit.new(limit=None):
        if submission.mod_note != None or submission.mod_reason_by != None or submission.mod_reason_title != None or \
            submission.mod_reports or submission.num_reports != None or submission.removal_reason != None or \
                submission.removed_by != None or submission.report_reasons:
            print("--------------------------")
            prettyPrinterSubmissions(submission)
            print(str(submission.mod_note))
            print(str(submission.mod_reason_by))
            print(str(submission.mod_reason_title))
            print(str(submission.mod_reports))
            print(str(submission.num_reports))
            print(str(submission.removal_reason))
            print(str(submission.removed_by))
            print(str(submission.report_reasons))
            print("------------------------------")
        else:
            print(".", end="")