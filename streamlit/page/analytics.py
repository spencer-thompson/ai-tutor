import datetime
import os

import pandas as pd
import requests

import streamlit as st

st.title("hello")

options = ["pageviews", "visit_duration", "events"]


date_range = st.selectbox("time range", options=["day", "7d", "28d", "30d", "91d", "month", "6mo", "12mo"], index=1)

selection = st.pills("test", selection_mode="multi", options=options, default=options, label_visibility="hidden")

api_key = os.getenv("PLAUSIBLE_API_KEY")

headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

url = "https://analytics.aitutor.live/api/v2/query"


today = datetime.datetime.now()

date_selection = st.date_input(
    "Select Dates to view:",
    (datetime.date(today.year, today.month, today.day - 7), today),
    min_value=datetime.date(2025, 1, 1),
    max_value=today,
    format="MM-DD-YYYY",
)

ds = [d.strftime("%Y-%m-%d") for d in date_selection]

if len(ds) == 2:
    data = st.session_state.backend.get(
        "analytics",
        {
            "timeseries": True,
            "start": ds[0],
            "end": ds[1],
        },
    )

    st.json(data)

# st.json(r.json()["results"])

# data = {x.get("dimensions")[0]: {selection[i]: m for i, m in enumerate(x.get("metrics"))} for x in r.json()["results"]}

# st.json(data)

# df = pd.DataFrame.from_dict(data, orient="index")

# st.line_chart(df)
#
# df = pd.read_json(orient="index")
#
# st.json(data)
#
#
# st.line_chart(data, x="date", y="metric")
