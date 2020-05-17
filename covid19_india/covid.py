from flask import Flask, render_template, redirect, url_for
import plotly.graph_objects as go
import plotly
import requests
import json
requests.packages.urllib3.disable_warnings()

app = Flask(__name__)

@app.route("/covid19")
def covid_home():
  url = 'https://api.covid19india.org/data.json'
  url_world = 'https://corona.lmao.ninja/v2/all'
  data = requests.get(url, verify=False)
  covid = data.json()
  covid19 = covid['statewise']
  covidstate = sorted(covid19, key=lambda k: int(k['confirmed']),reverse=True)

  data_total = requests.get(url_world, verify=False)
  total_data = data_total.json()
  world = total_data['cases']
  ids, daily_plot = get_daily_case_data(covid['cases_time_series'])
  return render_template('covid19_home.html', covid=covidstate, plot = daily_plot, ids = ids, page='covid', world = world)


@app.route("/covid19/helpline")
def covid_helpline():
  url = 'https://covid-19india-api.herokuapp.com/v2.0/helpline_numbers'
  data = requests.get(url, verify=False)
  covid = data.json()
  help_data = covid[1]['contact_details']
  return render_template('covid_helpline.html', help_data=help_data, page='covid_helpline')

def get_daily_case_data(detail):
  date, dailyconfirmed, dailydeceased, dailyrecovered, totalconfirmed, totaldeceased, totalrecovered = [], [], [], [], [], [], []
  for d in detail[31:]:
    date.append(d['date'])
    dailyconfirmed.append(d['dailyconfirmed'])
    dailydeceased.append(d['dailydeceased'])
    dailyrecovered.append(d['dailyrecovered'])
    totalconfirmed.append(d['totalconfirmed'])
    totaldeceased.append(d['totaldeceased'])
    totalrecovered.append(d['totalrecovered'])

  data1=[
    go.Scatter(
        x=date,
        y=dailyconfirmed,
        mode='lines+markers',
        name = 'Confirmed',
        line = dict(color = 'royalblue')
    ),
    go.Scatter(
        x=date,
        y=dailyrecovered,
        mode='lines+markers',
        name = 'Recovered',
        line = dict(color = '#34a227')
    ),
    go.Scatter(
        x=date,
        y=dailydeceased,
        mode='lines+markers',
        name = 'Deceased',
        line = dict(color = '#e64950')
    )
  ]

  layout1 = go.Layout(
    title = "Daily Cases",
    yaxis_title="Number of cases",
    font=dict(
        family="Courier New",
        size=14,
        color="#7f7f7f"
    )
  )

  data2=[
    go.Scatter(
        x=date,
        y=totalconfirmed,
        mode='lines+markers',
        name = 'Confirmed',
        line = dict(color = 'royalblue')
    ),
    go.Scatter(
        x=date,
        y=totalrecovered,
        mode='lines+markers',
        name = 'Recovered',
        line = dict(color = '#34a227')
    ),
    go.Scatter(
        x=date,
        y=totaldeceased,
        mode='lines+markers',
        name = 'Deceased',
        line = dict(color = '#e64950')
    )
  ]

  layout2 = go.Layout(
    title = "Total Cases",
    yaxis_title="Number of cases",
    font=dict(
        family="Courier New",
        size=14,
        color="#7f7f7f"
    )
  )

  graphs = [
    dict(
        data=data1,
        layout=layout1
    ),
    dict(
        data=data2,
        layout=layout2
    ),
  ]

  ids = ['graph-{}'.format(i) for i, _ in enumerate(graphs)]
  graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)
  return ids, graphJSON

if __name__ == "__main__":
  app.run()

#305621
