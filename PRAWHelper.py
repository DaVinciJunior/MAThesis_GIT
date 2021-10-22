from datetime import datetime
import praw

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

def prettyPrinterComments(comment, prefix):
    id = ""
    user = ""
    score = ""
    time = ""
    text = ""
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

    print(prefix + "<" + id + ">" + user + "[" + score + "]" + "{" + time + "}" + text)

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

def outputAllReplies(comment, prefix):
    for reply in comment.replies:
        prettyPrinterComments(reply, prefix)
        outputAllReplies(reply, prefix + "\t")

def test():
    reddit = login()
    #submission = reddit.submission(id="pyia16")
    submission = reddit.submission(id="q1ycfb")
    # replace "Show more" with limit = 0 (inifinte)
    submission.comments.replace_more(limit=0)
    for top_level_comment in submission.comments:
        prettyPrinterComments(top_level_comment, "")
        outputAllReplies(top_level_comment, "\t")
        print("\n\n---\n\n")

def test2():
    reddit = login()
    subreddit = reddit.subreddit("Austria")
    for submission in subreddit.stream.submissions():
        print("------------------------------")
        prettyPrinterSubmissions(submission)
        print("------------------------------")
        submission.comments.replace_more(limit=0)
        for top_level_comment in submission.comments:
            prettyPrinterComments(top_level_comment, "\t")
            outputAllReplies(top_level_comment, "\t\t")
        print("\n\n---\n\n")
    print("We're done!!")

# default: n = 100
def get_n_LatestSubmissionsAndComments(n=100):
    get_n_LatestSubmissionsAndCommentsAndExecuteFunction(n=n)


def get_n_LatestSubmissionsAndCommentsAndExecuteFunction(n=100, func=None):
    reddit = login()
    subreddit = reddit.subreddit("Austria")
    for submission in subreddit.new(limit=n):
        print("--------------------------")
        prettyPrinterSubmissions(submission)
        print("------------------------------")
        submission.comments.replace_more(limit=0)
        for top_level_comment in submission.comments:
            prettyPrinterComments(top_level_comment, "\t")
            if (func != None):
                func(top_level_comment.body)
            outputAllReplies(top_level_comment, "\t\t")
        print("\n\n---\n\n")
    # print("We're done!!")