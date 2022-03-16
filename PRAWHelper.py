import random
from datetime import datetime
import praw

import sentHelper


def login():
    # contains your login info comma-separated params: client_id, client_secret, user_agent
    login_data = open("res/login-data_new.txt", "r")
    my_params = login_data.read().split(',')
    my_client_id = my_params[0]
    my_client_secret = my_params[1]
    my_user_agent = my_params[2]
    my_username = my_params[3]
    my_password = my_params[4]
    return praw.Reddit(
        # insert login info here
        client_id=my_client_id,
        client_secret=my_client_secret,
        user_agent=my_user_agent,
        username=my_username,
        password=my_password
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
    # subreddit = reddit.subreddit("Buecher")
    # subreddit = reddit.subreddit("Hoerbuecher")
    # subreddit = reddit.subreddit("FitnessDE")
    # subreddit = reddit.subreddit("de_IAmA")
    # subreddit = reddit.subreddit("deutschland")
    # subreddit = reddit.subreddit("berlin")
    # subreddit = reddit.subreddit("aeiou")
    # subreddit = reddit.subreddit("graz")
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

def get_comment_by_id_and_reply_de_escalation_to_it(id, placebo=True):
    reddit = login()
    comment = reddit.comment(id)
    comment.reply("*Bleep Blop - I am a Bot.* 🤖  \n"
                  "**Dein Kommentar wurde automatisch selektiert und beantwortet. Es kann auch sein, dass ich mich täusche, dann bitte ich um Entschuldigung.**  \n"
                  "___  \n" +
                  str(get_random_de_escalation_phrase()) +
                  "___  \n"
                  "^(Ich versuche aggressive Kommentare auf Reddit zu de-eskalieren.  \n"
                  "Es besteht die Möglichkeit, dass dein Kommentar ein \"False Positive\" sprich einfach falsch als aggressiv erkannt wurde. In dem Fall diesen Kommentar bitte einfach ignorieren, danke.  \n"
                  "War mein De-Eskalationsversuch sinnvoll?  \n"
                  "Dann bitte gib einen Upvote.  \nAnsonsten ein Downvote.  \nVielen Dank für's Feedback.  \nP.s.: Für konstruktives Feedback habe ich immer ein offenes Ohr - Danke.)"
                  )
    if not placebo:
        comment.report("Bleep Blop - I am a Bot.  \nIch glaube, dieser Kommentar war aggressiv.")

def get_random_de_escalation_phrase():
    de_escalation_phrases = [
        "Ich hab den Eindruck, dass du deinen Kommentar weniger aggressiv formulieren könntest. Ich wäre dir sehr dankbar, wenn du deinen Kommentar editieren würdest.  \n",
        "Tut mir leid, dass ich störe, aber ich glaub, dass du irgendwem gegenüber angreifend warst. Ich wär dir dankbar, wenn du deinen Kommentar weniger aggressiv verfassen würdest. Danke dir.  \n",
        "Ich hab das Gefühl, dass du jemanden in ein \"schlechts Licht\" gerückt hast. Vielleicht kannst du deine Meinung auch ausdrücken, ohne dabei angreifend/verletzend zu sein? I wär dir dankbar, wenn du es probieren würdest.  \n",
        "In manchen Situationen ist man einfach grantig und dann will man auch Dampf ablassen. Ich will dich nur daran erinnern, dass das noch immer ein Mensch bzw. mehrere Menschen sind. Vielleicht kannst du das auch sagen, ohne diese(n) zu beleidigen. Danke für's Lesen.  \n",
        # "*Rosen sind rot, Veilchen sind blau*  \n*Dein Kommentar ginge weniger aggressiv, das weiß' ich genau.*  \n",
        # "Egal wie grantig der Mensch ist, essen muss er.  \nJetzt iss mal ein Snickers und vielleicht magst ja danach deinen Kommentar etwas überarbeiten.  \n",
        # "Ein von Zorn getrübtes Auge sieht nicht mehr, was recht oder unrecht ist.  \nWas ich damit sagen will...bitte versuch deinen Kommentar bisschen weniger angreifend zu formulieren.  \n",
        # "Respekt und Achtung verlieren sich am schnellsten in der Wut.  \nVielleicht können wir gemeinsam dazu beitragen, dass dieser Subreddit ein wenig ein schönerer Ort für alle Redditors wird.  \n",
        # "Aggressionen schaden nicht der Person, gegen die du sie richtest, sondern meistens nur dir.  \nIch würde mich freuen, wenn du deinen Kommentar etwas weniger toxisch umschreiben könntest.  \n",
        # "> Das Ärgerliche am Ärger ist, dass man sich schadet, ohne anderen zu nützen.  \n\n-*Kurt Tucholsky*  \nVielleicht können wir aufhören uns selber zu schaden, indem wir weniger grantig in die Welt hinausgehen?  \n",
        # "> Feder und Papier entzünden mehr Feuer als alle Streichhölzer der Welt.  \n\n-*Malcolm Stevenson Forbes*  \nIn unserem Kontext sind's halt digitale Feder und Papier. Wäre cool, wenn du deinem Kommentar bissl \"den Pfeffer\" nehmen könntest.  \n",
        # "> Wut ist wie eine Waffe, die man an der Klinge hält.  \n\n-*J.M. Barrie*  \nLegen wir die Waffen nieder und genießen wir den Subreddit als Chance mit anderen Schnitzel-EnthusiastikerInnen zu interagieren.  \n",
        # "> Wütend zu sein ist wie sich wegen der Fehler anderer an sich selbst zu rächen.  \n\n-*Alexander Pope*  \nMagst du unter Umständen deinen Kommentar versuchen konstruktiver zu verfassen?  \n",
        # "> An Ärger festzuhalten ist wie Gift zu trinken und erwarten, dass der andere dadurch stirbt.  \n\n-*Buddha*  \nMir ist klar, dass du vermutlich verärgert bist, aber hey vielleicht kannst du den Kommentar doch etwas umschreiben, damit er ned ganz so garstig rüberkommt?  \n",
        # "> Zorn. Furcht. Aggressivität. Die dunkle Seite der Macht sind sie. Besitz ergreifen sie leicht von dir.  \n\n-*Meister Yoda* in Star Wars: Episode V - Das Imperium schlägt zurück  \nDeinen Zorn nicht in diesem Subreddit ausleben du musst junger Padawan.  \n",
        # "Hier könnte etwas schlaues stehen, um dich dazu zu motivieren, weniger grantig zu sein, aber irgendwann geht auch mir die Muse aus. Editier bitte deinen Comment zu etwas weniger grantigem, ja?  \n",
        # "1...2...3...  \njetzt is'as mit'n Grant vorbei...  \n29...30...31...  \njetzta editier dein kommentar fleißig  \n",
        # "Hast du gewusst, dass Katzen in Schachteln statistisch viel beliebter sind als aggressive Kommentare?  \n...Nicht?! Wow, ja dann magst du vielleicht deinen Kommentar bisschen überarbeiten.  \n",
        # "> Marvin:\"Ich habe mit dem Bordcomputer gesprochen.\"  \nFord:\"Und?\"  \nMarvin:\"Er hasst mich.\"  \n\n-*Per Anhalter durch die Galaxis*  \nDas hätte der Bordcomputer besser machen können und ich bin mir zu 93% sicher du auch.  \n"
    ]
    alternative = "  \n---  \n**Ein Vorschlag**... Du kannst deine Meinung genauso ausdrücken ohne aggressiv dabei zu sein. Ein exemplarisches Beispiel, wenn ich darf?"
    alternative_variations = [
        "  \n **Aggressiv**:\"Du bist a bleda Beidl.\"  \n**Nicht-aggressiv**:\"I find dei Meinung is unbegründet.\"  \n",
        "  \n **Aggressiv**:\"Hawi bist behindert?\"  \n**Nicht-aggressiv**:\"I find's ned guat, was du da sagst, aber wenn das deine Meinung is, dann soll's so sein.\"  \n",
        "  \n **Aggressiv**:\"Geh scheißn drecks bot.\"  \n**Nicht-aggressiv**:\"I find den Bot unnedig, weil ... (gern auch im Kommentar konstruktives Feedback geben)\"  \n",
        "  \n **Aggressiv**:\"Konnst da a Watschen bei mir obholen kumman.\"  \n**Nicht-aggressiv**:\"I hab dir nix mehr zum sagen, sorry.\"  \n",
        "  \n **Aggressiv**:\"Bist ongrennt oda wos?\"  \n**Nicht-aggressiv**:\"Wennst manst, dass das gscheid is, dann mach's, i bin aba ehrlich gsagt ka Fan von.\"  \n",
        "  \n **Aggressiv**:\"Deppate Funzn!\"  \n**Nicht-aggressiv**:\"De Frau is ma ned sympathisch.\"  \n",
        "  \n **Aggressiv**:\"Hianbliatla.\"  \n**Nicht-aggressiv**:\"Find i ned gscheid, was du da schreibst, aber okay...\"  \n",
        "  \n **Aggressiv**:\"Schaß Kretzn du elendige!\"  \n**Nicht-aggressiv**:\"Du gehst ma ehrlich gsagt auf die Nerven. Sei so guad und lass das bitte.\"  \n",
        "  \n **Aggressiv**:\"Deppads Gsindl.\"  \n**Nicht-aggressiv**:\"Was die Gruppe da macht, find i ned guad.\"  \n"
    ]
    return random.choice(de_escalation_phrases) + alternative + random.choice(alternative_variations)

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