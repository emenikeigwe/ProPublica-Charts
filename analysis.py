import urllib.request, json
import calendar

with urllib.request.urlopen('http://tinyurl.com/propublicasampledata') as url:
    # all entries are from 2022
    data = json.loads(url.read())

all_months = {}
possible_topics = ['Biden Administration', 'Civil Rights', 'Criminal Justice', 'Debt', 'Democracy', 'Education', 'Environment', 'Health Care', 'Immigration', 'Labor', 'Military', 'Other', 'Politics', 'Racial Justice', 'Regulation', 'Sex and Gender', 'Technology', 'Trump Administration']
total_reporters_by_topic = {}
total_articles_by_topic = dict.fromkeys(possible_topics, 0)
for article in data:
    month = calendar.month_name[int(article["postdate"][5:7])]
    # removes teams and ProPublica authorship from being included as individual reporter assignments
    authors = [author.lstrip(' ') for author in article["authors"].split(",") if "ProPublica" not in author.lstrip(' ')]
    topics = article["topics"]

    if month not in all_months:
        all_months[month] = {"Article Counts": dict.fromkeys(possible_topics, 0),
         "Reporter Counts": dict.fromkeys(possible_topics, 0)}
        for key in all_months[month]["Reporter Counts"]:
            all_months[month]["Reporter Counts"][key] = set()
    # all_months["January"] = {"Article Counts": {<January Article Count Dict>}, "Reporter Counts": {<January Unique Reporter Count Dict>}}

    # topic is unknown
    if not topics:
        topics = "Other"

    article_count_single_month = all_months[month]["Article Counts"]
    reporter_count_single_month = all_months[month]["Reporter Counts"]

    topics = [topic.lstrip(' ') for topic in topics.split(",")]
    for topic in topics:
        if topic not in total_reporters_by_topic:
            reporter_count_single_month[topic] = set()
            total_reporters_by_topic[topic] = set()
        article_count_single_month[topic] = article_count_single_month.setdefault(topic, 0) + 1
        total_articles_by_topic[topic] = total_articles_by_topic.setdefault(topic, 0) + 1
        reporter_count_single_month[topic].update(authors)
        total_reporters_by_topic[topic].update(authors)

# from individual reporters to count; easily modified back by commenting out
for month in all_months:
    for topic in all_months[month]["Reporter Counts"]:
        if topic not in total_reporters_by_topic:
            total_reporters_by_topic[topic] = set()
        all_months[month]["Reporter Counts"][topic] = len(all_months[month]["Reporter Counts"][topic])
for topic in total_reporters_by_topic:
    total_reporters_by_topic[topic] = len(total_reporters_by_topic[topic])
