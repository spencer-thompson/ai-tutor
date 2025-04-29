import datetime
import json
import os

import pandas as pd
import requests

import streamlit as st

st.title("Analytics")


tab1, tab2, tab3, tab4 = st.tabs(["Timeseries", "Breakdown", "Courses", "Duration"])


options = ["pageviews", "visit_duration", "events"]

all_data = st.session_state.backend.get("analytics_data")
# with open("../../mongo/snapshots/mongo_snapshot_users_04-23-2025.json", "r") as f:
#     content = json.load()

# all_data = content
# all_data = json.load("../mongo/snapshots/mongo_snapshot_users_04-23-2025.json")
# all_data =


# date_range = st.selectbox("time range", options=["day", "7d", "28d", "30d", "91d", "month", "6mo", "12mo"], index=1)

# selection = st.pills("test", selection_mode="multi", options=options, default=options, label_visibility="hidden")

api_key = os.getenv("PLAUSIBLE_API_KEY")

headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

# url = "https://analytics.aitutor.live/api/v2/query"


def query_v1_api(endpoint, period, prop, filters):
    if filters:
        url = f"https://analytics.aitutor.live/api/v1/stats/{endpoint}?period=custom&date={period[0]},{period[1]}&site_id=aitutor.live&property=event:{prop}&filters=event:{filters[0]}%3D%3D{filters[1]}"
    else:
        url = f"https://analytics.aitutor.live/api/v1/stats/{endpoint}?period=custom&date={period[0]},{period[1]}&site_id=aitutor.live&property=event:{prop}"  # &filters=event:{filters[0]}%3D%3D{filters[1]}"

    r = requests.get(url, headers=headers)

    return r.json()["results"]


def duration_data(period):
    url = "https://analytics.aitutor.live/api/v2/query"

    filters = [["is_not", "event:props:canvas_id", ["(none)"]]]
    if len(ds) == 2:
        data = {
            "site_id": "aitutor.live",
            "metrics": [
                "visit_duration",
                # "bounce_rate",
                # "events",
                # "time_on_page",
            ],
            # "filters": filters,
            # "filters": [["is_not", "visit:city_name", [""]]],
            "dimensions": [
                "time:hour",
                # "event:page",
                # "visit:city_name",
                # "event:goal",
                # "event:props:canvas_id",
                # "event:props:length",
            ],
            "date_range": period,
        }

        r = requests.post(url, json=data, headers=headers)

        results = r.json()["results"]

        data = [{"Minutes": int(r.get("metrics")[0]) / 60, "Time": r.get("dimensions")[0]} for r in results]

        return data


today = datetime.datetime.now()

date_selection = st.date_input(
    "Select Dates to view:",
    (datetime.date(today.year, today.month - 1, today.day), today),
    min_value=datetime.date(2025, 1, 1),
    max_value=today,
    format="MM-DD-YYYY",
)

ds = [d.strftime("%Y-%m-%d") for d in date_selection]

if len(ds) == 2:
    data = query_v1_api("timeseries", ds, "goal", ["goal", "simple_chat"])


with tab1:
    if len(ds) == 2:
        data = query_v1_api("timeseries", ds, "goal", ["goal", "simple_chat"])

        st.line_chart(data, x="date", y="visitors", x_label="Date", y_label="Students")
    # st.json(data)

with tab2:
    # if len(ds) == 2:
    #     data = query_v1_api("breakdown", ds, "goal", ["goal", "simple_chat"])
    if len(ds) == 2:
        data = query_v1_api("breakdown", ds, "props:length", [])

        data = [
            {"visitors": d.get("visitors"), "length": int(d.get("length"))}
            for d in data
            if not d.get("length") == "(none)"
        ]

        data.sort(key=lambda x: x.get("length"))

        # st.json(data)
        st.bar_chart(
            data,
            x="length",
            y="visitors",
            x_label="Number of Messages",
            y_label="Number of Users",
        )

with tab3:
    url = "https://analytics.aitutor.live/api/v2/query"

    filters = [["is_not", "event:props:canvas_id", ["(none)"]], ["is", "event:goal", ["session"]]]
    if len(ds) == 2:
        data = {
            "site_id": "aitutor.live",
            "metrics": ["events"],
            "filters": filters,
            "dimensions": [
                "event:props:canvas_id",
                "time:day",
                "event:goal",
                # "event:page",
            ],
            "date_range": ds,
        }

        r = requests.post(url, json=data, headers=headers)

        results = r.json()["results"]
        # st.json(results)

        # data = json.loads(results)
        df = pd.DataFrame(results)

        # Flattening the lists into columns
        df["Sessions"] = df["metrics"].apply(lambda x: x[0])
        df["canvas_id"] = df["dimensions"].apply(lambda x: x[0])
        df["Date"] = df["dimensions"].apply(lambda x: x[1])
        # df["type"] = df["dimensions"].apply(lambda x: x[2])

        # Optional: drop the old columns
        df = df.drop(["metrics", "dimensions"], axis=1)

        courses = {u.get("canvas_id"): u.get("courses") for u in all_data}

        records = []
        for canvas_id, course_list in courses.items():
            for course in course_list:
                record = {
                    "id": course.get("id"),
                    "canvas_id": str(canvas_id),
                    "Course Code": course.get("course_code"),
                    "Name": course.get("name"),
                    "Score": course.get("current_score"),
                    # "Sessions": df["Sessions"]
                }
                # record.update(course)
                records.append(record)

        courses_df = pd.DataFrame(records)

        big_df = df.groupby("canvas_id")["Sessions"].sum().reset_index()

        # big_df
        # courses_df

        final_df = pd.merge(courses_df, big_df, on="canvas_id", how="left")
        #
        # final_df
        # final_df
        df = final_df[final_df["Name"] != "DEV_AI-Tutor-Development-Alsharif"]
        df["Department"] = df["Name"].str.split("-").str[0]

        dept_df = df.groupby("Department")["Sessions"].sum().reset_index()

        department_df = dept_df[dept_df["Sessions"] > 1].sort_values(by="Sessions", ascending=False)
        # department_df = department_df.sort_values(by="Sessions", ascending=True)

        # st.bar_chart(final_df, x="Name", y=["Sessions"], x_label="Course Name") # hide dev ai tutor
        st.bar_chart(df, x="Name", y=["Sessions"], x_label="Course Name")

        st.subheader("By Department")

        st.bar_chart(department_df, x="Department", y=["Sessions"], x_label="Course Name")

        # st.json(results)
        # st.json(st.session_state.backend.get("analytics_data"))

with tab4:
    if len(ds) == 2:
        data = duration_data(ds)

        st.area_chart(data, x="Time", y="Minutes")
        # st.json(data)

# with tab5:
#     if len(ds) == 2:
#         data = query_v1_api("breakdown", ds, "props:canvas_id", [])
#         st.json(data)
#         # url = f"https://analytics.aitutor.live/api/v1/stats/breakdown?period=custom&date={ds[0]},{ds[1]}&site_id=aitutor.live&property=event:props:canvas_id"
#         # r = requests.get(url, headers=headers)
#         #
#         # st.json(r.json())
#         # results = r.json()["results"]
#
#         # canvas_ids = [i.get("canvas_id") for i in results]
#         courses = [{u.get("canvas_id"): u.get("courses")} for u in all_data]
#
#         canvas_ids = list(courses[0].keys())
#
#         st.json(courses)

# courses_messages = [{}]

# for id in canvas_ids:
#     # print(id)
#     st.json(query_v1_api("breakdown", ds, "props:length", ["props:canvas_id", id]))
#     # print()


# today = datetime.datetime.now()
#
# date_selection = st.date_input(
#     "Select Dates to view:",
#     (datetime.date(today.year, today.month, today.day - 7), today),
#     min_value=datetime.date(2025, 1, 1),
#     max_value=today,
#     format="MM-DD-YYYY",
# )
#
# ds = [d.strftime("%Y-%m-%d") for d in date_selection]
#
# if len(ds) == 2:
#     data = st.session_state.backend.get(
#         "analytics",
#         {
#             "timeseries": True,
#             "start": ds[0],
#             "end": ds[1],
#         },
#     )
#
#     st.json(data)
#
# # st.json(r.json()["results"])
#
# # data = {x.get("dimensions")[0]: {selection[i]: m for i, m in enumerate(x.get("metrics"))} for x in r.json()["results"]}
#
# # st.json(data)
#
# # df = pd.DataFrame.from_dict(data, orient="index")
#
# # st.line_chart(df)
# #
# # df = pd.read_json(orient="index")
# #
# # st.json(data)
# #
# #
# # st.line_chart(data, x="date", y="metric")
