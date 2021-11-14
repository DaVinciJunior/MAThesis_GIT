import re
from praw.models.reddit import comment


def demojize(text):
    if isinstance(text, comment.Comment):
        for key in NON_UNICODE_EMOJIS.keys():
            text.body = re.sub(REGEX_BEGIN + re.escape(key) + REGEX_END, " " + NON_UNICODE_EMOJIS[key] + " ", text.body)
    elif isinstance(text, str):
        for key in NON_UNICODE_EMOJIS.keys():
            text = re.sub(REGEX_BEGIN + re.escape(key) + REGEX_END, " " + NON_UNICODE_EMOJIS[key] + " ", text)
    return text

# some emojis were taken from https://emoticoncentral.com/category/classic
# others were taken from the data obtained
# others are just variations of existing smileys
HEART = ":heart:"
WINK = ":wink:"
GREAT_SADNESS = ":great_sadness:"
SICK = ":sick:"
ANGRY = ":angry:"
CLOWN = ":clown:"
DISMAY = ":dismay:"
PIRATE = ":pirate:"
TONGUE_OUT = ":tongue_out:"
OH_NO = ":oh_no:"
SHOCKED = ":shocked:"
THE_HORROR = ":the_horror:"
TEARS_OF_HAPPINESS = ":tears_of_happiness:"
TIRED_AND_DISAPPOINTED = ":tired_and_disappointed:"
LAUGHING = ":laughing:"
LAUGHING_OUT_LOUD = ":laughing_out_loud:"
DEAD_WITH_TONGUE_OUT = ":dead_with_tongue_out:"
DORITO_FACE = ":dorito_face:"
SMILEY = ":smiley:"
SLEEPY_EYES = ":sleepy_eyes:"
CALM = ":calm:"
SAD = ":sad:"
CRYING = ":crying:"
ANGRY_PUNK = ":angry_punk:"
KISS = ":kiss:"
EVIL_GRIN = ":evil_grin:"
RAWR_I_AM_A_LION = ":rawr_I_am_a_lion:"
DEEP_FROWN = ":deep_frown:"
CAT_FACE = ":cat_face:"
FUNNY = ":funny:"
SHRUG = ":shrug:"
LITTLE_PIG = ":little_pig:"
HIGH_FIVE = ":high_five:"
LITTLE_FISH = ":little_fish:"
FISH = ":fish:"
VW_BUG = ":vw_bug:"
PAC_MAN = ":pac_man:"
PIKACHU = ":pikachu:"
COUPLE_KISSING = ":couple_kissing:"
PIKACHU_FACE = ":pikachu_face:"
KYRBI = ":kyrbi:"
FACEPALM = ":facepalm:"

NON_UNICODE_EMOJIS = {
    # Creative Emojis
    "⊂(◉‿◉)": KYRBI,
    "⊂(◉‿◉)⊃": KYRBI,
    "(◉‿◉)⊃": KYRBI,
    "⊆(◉‿◉)": KYRBI,
    "⊆(◉‿◉)⊇": KYRBI,
    "(◉‿◉)⊇": KYRBI,
    "c(O_O)": KYRBI,
    "(o^-^o)": PIKACHU_FACE,
    "( '}{' )": COUPLE_KISSING,
    "^_^\'\'": PIKACHU,
    "^_^\"": PIKACHU,
    "\'\'^_^": PIKACHU,
    "\"^_^": PIKACHU,
    "*~●＞^": PAC_MAN,
    "(o\\_!_/o)": VW_BUG,
    "<*)))‑{": FISH,
    "><(((*>": FISH,
    "<><": LITTLE_FISH,
    "><>": LITTLE_FISH,
    "o/\\o": HIGH_FIVE,
    "O/\\O": HIGH_FIVE,
    "o()~": LITTLE_PIG,
    "¯\\_(ツ)_/¯": SHRUG,
    "<3": HEART,
    # "Standard faces"
    "^^": FUNNY,
    "^-^": FUNNY,
    "^_^": FUNNY,
    ":3": CAT_FACE,
    ":-3": CAT_FACE,
    "=3": CAT_FACE,
    "=-3": CAT_FACE,
    ":c": DEEP_FROWN,
    ":-c": DEEP_FROWN,
    "=c": DEEP_FROWN,
    "=-c": DEEP_FROWN,
    ">:3": RAWR_I_AM_A_LION,
    ">:-3": RAWR_I_AM_A_LION,
    ">=3": RAWR_I_AM_A_LION,
    ">=-3": RAWR_I_AM_A_LION,
    ":>": EVIL_GRIN,
    ":->": EVIL_GRIN,
    "<:": EVIL_GRIN,
    "<-:": EVIL_GRIN,
    "=>": EVIL_GRIN,
    "=->": EVIL_GRIN,
    "<=": EVIL_GRIN,
    "<-=": EVIL_GRIN,
    ":*": KISS,
    ":-*": KISS,
    "*:": KISS,
    "*-:": KISS,
    "=*": KISS,
    "=-*": KISS,
    "*=": KISS,
    "*-=": KISS,
    ">:(": ANGRY_PUNK,
    ">:-(": ANGRY_PUNK,
    "):<": ANGRY_PUNK,
    ")-:<": ANGRY_PUNK,
    ">=(": ANGRY_PUNK,
    ">=-(": ANGRY_PUNK,
    ")=<": ANGRY_PUNK,
    ")-=<": ANGRY_PUNK,
    ">:[": ANGRY_PUNK,
    ">:-[": ANGRY_PUNK,
    "]:<": ANGRY_PUNK,
    "]-:<": ANGRY_PUNK,
    ">=[": ANGRY_PUNK,
    ">=-[": ANGRY_PUNK,
    "]=<": ANGRY_PUNK,
    "]-=<": ANGRY_PUNK,
    ":'‑(": CRYING,
    ":'(": CRYING,
    ":,‑(": CRYING,
    ":,(": CRYING,
    ")':": CRYING,
    ")-':": CRYING,
    ")-,:": CRYING,
    "),:": CRYING,
    ";‑(": CRYING,
    ";(": CRYING,
    ");": CRYING,
    ")-;": CRYING,
    "='‑(": CRYING,
    "='(": CRYING,
    "=,‑(": CRYING,
    "=,(": CRYING,
    ")'=": CRYING,
    ")-'=": CRYING,
    ")-,=": CRYING,
    "),=": CRYING,
    ":'‑[": CRYING,
    ":'[": CRYING,
    ":,‑[": CRYING,
    ":,[": CRYING,
    ";‑[": CRYING,
    ";[": CRYING,
    "]':": CRYING,
    "]-':": CRYING,
    "]-,:": CRYING,
    "],:": CRYING,
    "];": CRYING,
    "]-;": CRYING,
    "='‑[": CRYING,
    "='[": CRYING,
    "=,‑[": CRYING,
    "=,[": CRYING,
    "]'=": CRYING,
    "]-'=": CRYING,
    "]-,=": CRYING,
    "],=": CRYING,
    ":っ(": SAD,
    ":-(": SAD,
    ":(": SAD,
    "):": SAD,
    ")-:": SAD,
    ")-=": SAD,
    ")=": SAD,
    "=-(": SAD,
    "=(": SAD,
    "=っ(": SAD,
    ":っ[": SAD,
    ":-[": SAD,
    ":[": SAD,
    "]:": SAD,
    "]-:": SAD,
    "]-=": SAD,
    "]=": SAD,
    "=-[": SAD,
    "=[": SAD,
    "=っ[": SAD,
    ":/": SAD,
    ":-/": SAD,
    "=/": SAD,
    "=-/": SAD,
    "/:": SAD,
    "/-:": SAD,
    "/=": SAD,
    "/-=": SAD,
    ":\\": SAD,
    ":-\\": SAD,
    "=\\": SAD,
    "=-\\": SAD,
    "\\:": SAD,
    "\\-:": SAD,
    "\\=": SAD,
    "\\-=": SAD,
    "ˊ＿>ˋ": CALM,
    "Z_Z": SLEEPY_EYES,
    "Z-Z": SLEEPY_EYES,
    ":)": SMILEY,
    ":-)": SMILEY,
    "(:": SMILEY,
    "(-:": SMILEY,
    "=)": SMILEY,
    "=-)": SMILEY,
    "(=": SMILEY,
    "(-=": SMILEY,
    ":]": SMILEY,
    ":-]": SMILEY,
    "[:": SMILEY,
    "[-:": SMILEY,
    "=]": SMILEY,
    "=-]": SMILEY,
    "[=": SMILEY,
    "[-=": SMILEY,
    "8)": SMILEY,
    "8-)": SMILEY,
    "(8": SMILEY,
    "(-8": SMILEY,
    ":^)": DORITO_FACE,
    "=^)": DORITO_FACE,
    "(^:": DORITO_FACE,
    "(^=": DORITO_FACE,
    ":^]": DORITO_FACE,
    "=^]": DORITO_FACE,
    "[^:": DORITO_FACE,
    "[^=": DORITO_FACE,
    "XP": DEAD_WITH_TONGUE_OUT,
    "Xb": DEAD_WITH_TONGUE_OUT,
    "xP": DEAD_WITH_TONGUE_OUT,
    "xb": DEAD_WITH_TONGUE_OUT,
    "Xp": DEAD_WITH_TONGUE_OUT,
    "xp": DEAD_WITH_TONGUE_OUT,
    "dX": DEAD_WITH_TONGUE_OUT,
    "dx": DEAD_WITH_TONGUE_OUT,
    "XD": LAUGHING_OUT_LOUD,
    "xD": LAUGHING_OUT_LOUD,
    "X-D": LAUGHING_OUT_LOUD,
    "x-D": LAUGHING_OUT_LOUD,
    "X^D": LAUGHING_OUT_LOUD,
    "x^D": LAUGHING_OUT_LOUD,
    ":D": LAUGHING,
    ":-D": LAUGHING,
    ":^D": LAUGHING,
    "=D": LAUGHING,
    "=-D": LAUGHING,
    "=^D": LAUGHING,
    "BD": LAUGHING,
    "B^D": LAUGHING,
    "v.v": TIRED_AND_DISAPPOINTED,
    "v_v": TIRED_AND_DISAPPOINTED,
    "V.V": TIRED_AND_DISAPPOINTED,
    "V_V": TIRED_AND_DISAPPOINTED,
    "v-v": TIRED_AND_DISAPPOINTED,
    "V-V": TIRED_AND_DISAPPOINTED,
    ":')": TEARS_OF_HAPPINESS,
    ":'-)": TEARS_OF_HAPPINESS,
    "='-)": TEARS_OF_HAPPINESS,
    "=')": TEARS_OF_HAPPINESS,
    ":,)": TEARS_OF_HAPPINESS,
    ":,-)": TEARS_OF_HAPPINESS,
    "=,-)": TEARS_OF_HAPPINESS,
    "=,)": TEARS_OF_HAPPINESS,
    "(':": TEARS_OF_HAPPINESS,
    "(-':": TEARS_OF_HAPPINESS,
    "(-'=": TEARS_OF_HAPPINESS,
    "('=": TEARS_OF_HAPPINESS,
    "(,:": TEARS_OF_HAPPINESS,
    "(-,:": TEARS_OF_HAPPINESS,
    "(-,=": TEARS_OF_HAPPINESS,
    "(,=": TEARS_OF_HAPPINESS,
    ":']": TEARS_OF_HAPPINESS,
    ":'-]": TEARS_OF_HAPPINESS,
    "='-]": TEARS_OF_HAPPINESS,
    "=']": TEARS_OF_HAPPINESS,
    ":,]": TEARS_OF_HAPPINESS,
    ":,-]": TEARS_OF_HAPPINESS,
    "=,-]": TEARS_OF_HAPPINESS,
    "=,]": TEARS_OF_HAPPINESS,
    "[':": TEARS_OF_HAPPINESS,
    "[-':": TEARS_OF_HAPPINESS,
    "[-'=": TEARS_OF_HAPPINESS,
    "['=": TEARS_OF_HAPPINESS,
    "[,:": TEARS_OF_HAPPINESS,
    "[-,:": TEARS_OF_HAPPINESS,
    "[-,=": TEARS_OF_HAPPINESS,
    "[,=": TEARS_OF_HAPPINESS,
    "D:": THE_HORROR,
    "D-:": THE_HORROR,
    "D=": THE_HORROR,
    "D-=": THE_HORROR,
    ">:O": SHOCKED,
    ">:-O": SHOCKED,
    ">:o": SHOCKED,
    ">:-o": SHOCKED,
    ">:0": SHOCKED,
    ">:-0": SHOCKED,
    ">=O": SHOCKED,
    ">=-O": SHOCKED,
    ">=o": SHOCKED,
    ">=-o": SHOCKED,
    ">=0": SHOCKED,
    ">=-0": SHOCKED,
    "O:<": SHOCKED,
    "O-:<": SHOCKED,
    "o:<": SHOCKED,
    "o-:<": SHOCKED,
    "0:<": SHOCKED,
    "0-:<": SHOCKED,
    "O=<": SHOCKED,
    "O-=<": SHOCKED,
    "o=<": SHOCKED,
    "o-=<": SHOCKED,
    "0=<": SHOCKED,
    "0-=<": SHOCKED,
    ":o": OH_NO,
    ":O": OH_NO,
    ":0": OH_NO,
    "=o": OH_NO,
    "=O": OH_NO,
    "=0": OH_NO,
    ":-o": OH_NO,
    ":-O": OH_NO,
    ":-0": OH_NO,
    "=-o": OH_NO,
    "=-O": OH_NO,
    "=-0": OH_NO,
    "o:": OH_NO,
    "O:": OH_NO,
    "0:": OH_NO,
    "o=": OH_NO,
    "O=": OH_NO,
    "0=": OH_NO,
    "o-:": OH_NO,
    "O-:": OH_NO,
    "0-:": OH_NO,
    "o-=": OH_NO,
    "O-=": OH_NO,
    "0-=": OH_NO,
    ":P": TONGUE_OUT,
    ":p": TONGUE_OUT,
    ":b": TONGUE_OUT,
    "d:": TONGUE_OUT,
    "=P": TONGUE_OUT,
    "=p": TONGUE_OUT,
    "=b": TONGUE_OUT,
    "d=": TONGUE_OUT,
    ":-P": TONGUE_OUT,
    ":-p": TONGUE_OUT,
    ":-b": TONGUE_OUT,
    "d-:": TONGUE_OUT,
    "=-P": TONGUE_OUT,
    "=-p": TONGUE_OUT,
    "=-b": TONGUE_OUT,
    "d-=": TONGUE_OUT,
    "?)": PIRATE,
    "?-)": PIRATE,
    "?]": PIRATE,
    "?-]": PIRATE,
    "?D": PIRATE,
    "?-D": PIRATE,
    "D:<": DISMAY,
    "D=<": DISMAY,
    "D-:<": DISMAY,
    "D-=<": DISMAY,
    "Dx": DISMAY,
    "DX": DISMAY,
    "D-x": DISMAY,
    "D-X": DISMAY,
    ":o)": CLOWN,
    "(o:": CLOWN,
    "=o)": CLOWN,
    "(o=": CLOWN,
    ";o)": CLOWN,
    "(o;": CLOWN,
    ":@": ANGRY,
    ":-@": ANGRY,
    "=@": ANGRY,
    "=-@": ANGRY,
    ":&": SICK,
    ":-&": SICK,
    "=&": SICK,
    "=-&": SICK,
    "D':": GREAT_SADNESS,
    "D-':": GREAT_SADNESS,
    "D'=": GREAT_SADNESS,
    "D-'=": GREAT_SADNESS,
    "D,:": GREAT_SADNESS,
    "D-,:": GREAT_SADNESS,
    "D,=": GREAT_SADNESS,
    "D-,=": GREAT_SADNESS,
    "D;": GREAT_SADNESS,
    "D-;": GREAT_SADNESS,
    ";)": WINK,
    ";-)": WINK,
    ";]": WINK,
    ";-]": WINK,
    ";D": WINK,
    ";-D": WINK,
    "(;": WINK,
    "(-;": WINK,
    "[;": WINK,
    "[-;": WINK,
    "(/.-)": FACEPALM,
    "(-.\\)": FACEPALM,
    "(/.\\)": FACEPALM,
    "/.-": FACEPALM,
    "-.\\": FACEPALM,
    "/.\\": FACEPALM,
}

REGEX_BEGIN = r"(\s){0,1}"
REGEX_END = r"((\W\D)+|$)"