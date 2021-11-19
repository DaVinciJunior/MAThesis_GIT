import csv
import emoji

####  Adds 736 Emoji sentiments ####

if __name__ == "__main__":
    file = open("Emoji_Sentiment_Data_v1.0.csv", encoding="utf-8")
    csvreader = csv.reader(file)
    header = next(csvreader)
    rows = []
    i = 2
    for row in csvreader:
        raw_emoji = row[0]
        occurrences = int(row[2])
        negative = int(row[4])
        neutral = int(row[5])
        positive = int(row[6])

        base = 0
        if positive > neutral and positive > negative:
            base = 1
        if negative > neutral and negative > positive:
            base = -1

        average = (positive - negative) / occurrences

        score = (base + average) / 2

        parsed_emoji = emoji.demojize(raw_emoji)
        if not raw_emoji == parsed_emoji:
            # print(str(i), emoji.demojize(row[0]), str(base), str(average), str(score))
            print("<word confidence=\"1.0\" form=\"" + str(parsed_emoji) + "\" intensity=\"1.0\" polarity=\"" + str(score) + "\" pos=\"RB\" subjectivity=\"0.0\"/>")
        i = i + 1