import pandas as pd
from datetime import datetime

def pt():
    df = pd.read_csv("~/Developer/hecon23/asset/물류_PT.csv")
    col = {
        'dates': "dates",
        '입원환자수': "total",
        '연령0_9': "age_0_9",
        '연령10_19': "age_10_19",
        '연령20_29': "age_20_29",
        '연령30_39': "age_30_39",
        '연령40_49': "age_40_49",
        '연령50_59': "age_50_59",
        '연령60_69': "age_60_69",
        '연령70_79': "age_70_79",
        '연령80_': "age_80",
        '성별M': "sex_male",
        '성별F': "sex_female",
        '치과': "dep_dentist",
        '정형외과': "dep_orthopedics",
        '그외': "dep_etc"
    }

    insertable = []
    for name in df.columns:
        if name == "dates":
            continue

        # date, id, value
        dts = df["dates"]
        id = col[name]
        vals = df[name]
        for (d, v) in zip(dts, vals):
            insertable.append([d, id, v])
    return ["date", "id", "value"], insertable


def op():
    df = pd.read_csv("~/Developer/hecon23/asset/물류_OP.csv")
    ids = df['수술코드1']
    date = df.columns[1:]

    insertable = []
    for d in date:
        for (v, i) in zip(df[d], ids):
            insertable.append([d, i, v])
    return ["date", "id", "value"], insertable


def dx():
    df = pd.read_csv("~/Developer/hecon23/asset/물류_DX.csv")
    ids = df['상병코드1']
    date = df.columns[1:]

    insertable = []
    for d in date:
        for (v, i) in zip(df[d], ids):
            insertable.append([d, i, v])
    return ["date", "id", "value"], insertable


def dates():
    df1 = pd.read_csv("~/Developer/hecon23/asset/물류_PT.csv")
    df2 = pd.read_csv("~/Developer/hecon23/asset/물류_OP.csv")
    df3 = pd.read_csv("~/Developer/hecon23/asset/물류_DX.csv")

    dt1 = df1["dates"]
    dt2 = df2.columns[1:]
    dt3 = df3.columns[1:]

    result = set()
    for i in range(max(len(dt1), len(dt2), len(dt3))):
        for ls in [dt1, dt2, dt3]:
            try:
                result.add(ls[i])
            except Exception as e:
                continue

    insertable = list()
    for i in result:
        my_date = datetime.strptime(i, "%Y-%m-%d")
        insertable.append(
            [i, my_date.year, my_date.month, my_date.day, my_date.weekday()]
        )

    return ["date", "year", "month", "day", "weekday"], insertable
