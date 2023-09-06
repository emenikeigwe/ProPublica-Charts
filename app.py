import io
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from base64 import b64encode
from analysis import possible_topics
from analysis import all_months
from analysis import total_articles_by_topic
from analysis import total_reporters_by_topic
from dash import Dash, dcc, html, dash_table

app = Dash(__name__)

buffer = io.StringIO()
server = app.server


article_topic_df = pd.DataFrame(total_articles_by_topic.items(), columns=['Topic', 'num. of articles']).sort_values(by=['Topic'])
reporter_topic_df = pd.DataFrame(total_reporters_by_topic.items(), columns=["Topic", "num. of reporters"]).sort_values(by=['Topic'])

topic_table_data = [{"Topic": i, "Total Articles": total_articles_by_topic[i], "Total Reporters": total_reporters_by_topic[i]} for i in possible_topics]
article_topic_fig = px.bar(article_topic_df.drop(article_topic_df[article_topic_df.Topic == "Other"].index), x='Topic', y='num. of articles', title="Article Count by Topic")
reporter_topic_fig = px.bar(reporter_topic_df.drop(reporter_topic_df[reporter_topic_df.Topic == "Other"].index), x='Topic', y='num. of reporters', title="Reporter Count by Topic")

article_topic_fig.write_html(buffer)
reporter_topic_fig.update_traces(marker_color='lightskyblue')
reporter_topic_fig.write_html(buffer)

article_month_df = {"Month": [], "Topic": [], "Article Count": []}
reporter_month_df = {"Month": [], "Topic": [], "Reporter Count": []}

for month in all_months:
    for topic in all_months[month]["Article Counts"]:
        article_month_df["Month"].append(month)
        article_month_df["Topic"].append(topic)
        article_month_df["Article Count"].append(all_months[month]["Article Counts"][topic])
    for topic in all_months[month]["Reporter Counts"]:
        reporter_month_df["Month"].append(month)
        reporter_month_df["Topic"].append(topic)
        reporter_month_df["Reporter Count"].append(all_months[month]["Reporter Counts"][topic])

article_month_df = pd.DataFrame.from_dict(article_month_df)
reporter_month_df = pd.DataFrame.from_dict(reporter_month_df)

# diff month for each row; topics in columns; separate into two tables
article_month_table_data = [dict([("Month", month)]+[(topic, all_months[month]["Article Counts"][topic]) for topic in possible_topics if topic != "Other"]) for month in all_months]
reporter_month_table_data = [dict([("Month", month)]+[(topic, all_months[month]["Reporter Counts"][topic]) for topic in possible_topics if topic != "Other"]) for month in all_months]

article_month_fig = px.bar(article_month_df.drop(article_month_df[article_month_df.Topic == "Other"].index), x="Month", y="Article Count", color="Topic", title="Total Articles per Month w/ Breakdown by Topic")
reporter_month_fig = px.bar(reporter_month_df.drop(reporter_month_df[reporter_month_df.Topic == "Other"].index), x="Month", y="Reporter Count", color="Topic", title="Total Reporters per Month w/ Breakdown by Topic")

article_month_fig.write_html(buffer)
reporter_month_fig.write_html(buffer)

html_bytes = buffer.getvalue().encode()
encoded = b64encode(html_bytes).decode()

app.layout = html.Div([
    dcc.Graph(id="art_top", figure=article_topic_fig),
    dcc.Graph(id="rep_top", figure=reporter_topic_fig),
    dcc.Graph(id="art_month", figure=article_month_fig),
    dcc.Graph(id="rep_month", figure=reporter_month_fig),
    html.Br(),
    html.H1('Article and Reporter Count By Topic'),
    dash_table.DataTable(id="topic_table", data=topic_table_data),
    html.Br(),
    html.H1('Article Count By Month (Breakdown by Topic)'),
    dash_table.DataTable(id="article_month_table", data=article_month_table_data),
    html.H1('Reporter Count By Month (Breakdown by Topic)'),
    dash_table.DataTable(id="reporter_month_table", data=reporter_month_table_data)
])

if 'ON_HEROKU' not in os.environ:
    app.run_server(debug=True)
