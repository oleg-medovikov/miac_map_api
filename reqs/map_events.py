from .app import app
from pandas import DataFrame, to_datetime
from base import db
from sqlalchemy import desc
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import folium
from folium.plugins import MarkerCluster
from fastapi.responses import HTMLResponse

# from typing import Optional
# from fastapi import Header, Body

from model import (
    Meddoc,
    MeddocCategory,
    Patient,
    Org,
    Case,
    Doctor,
    Adress,
    Diagnoz,
)


def create_circle(row):
    html = """<style>
              .table {
              font-family: Helvetica, Arial, sans-serif;
                width: 300px;
              }
              .table__heading, .table__cell {
                padding: .5rem 0;
              }
              .table__heading {
                text-align: left;
                font-size: 1.5rem;
                border-bottom: 1px solid #ccc;
              }
              .table__cell {
                line-height: 2rem;
              }
              .table__cell--highlighted {
                font-size: 1.25rem;
                font-weight: 300;
              }
              .table__button {
                display: inline-block;
                padding: .75rem 2rem;
                margin-top: 1rem;
                font-weight: 300;
                text-decoration: none;
                text-transform: uppercase;
                color: #fff;
                background-color: #f82;
                border-radius: .10rem;
              }
              .table__button:hover {
                background-color: #e62;
              }""" + f"""
            </style>
            <table cellpadding="1" cellspacing="1"  bordercolor="white" border="1" class="table">
              <thead>
                <tr>
                  <th colspan="2" scope="col" class="table__heading">{row['org']}</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td colspan="2" class="table__cell table__cell--highlighted">{row['mkb']} {row['sex']}  Возраст: {row['age']}</td>
                </tr>
                 <tr>
                  <td colspan="2" class="table__cell table__cell--highlighted">{row['diagnoz']}</td>
                </tr>
                <tr>
                  <td class="table__cell">Врач установивший диагноз:</td>
                  <td class="table__cell table__cell--highlighted">{row['doctor_fio']}</td>
                </tr>
                <tr>
                  <td class="table__cell">Дата заболевания:</td>
                  <td class="table__cell table__cell--highlighted">{row['date_sickness']}</td>
                </tr>
                <tr>
                  <td class="table__cell">Адрес:</td>
                  <td class="table__cell table__cell--highlighted">{row['adress']}</td>
                </tr>
              </tbody>
            </table>"""
    iframe = folium.Html(html, script=True)
    popup = folium.Popup(iframe)
    return folium.CircleMarker(
            location=[row['point'][1], row['point'][0]],
            radius=13,
            popup=popup,
            color="red",
            fill_opacity=0.8
        )


@app.get("/map_events", tags=["map_events"], response_class=HTMLResponse)
async def return_map_events():
    """возвращает карту со случаями определенной категории"""

    event = await db.select(
            [
                Org.short_name,
                Meddoc.history_number,
                Meddoc.creation_date,
                Patient.sex,
                Patient.birthdate,
                Meddoc.age,
                Patient.birthdate_baby,
                Doctor.fio,
                Doctor.spec,
                Doctor.telefon,
                Case.date_sickness,
                Case.date_first_req,
                Case.date_diagnoz,
                Case.time_SES, 
                Diagnoz.mkb,
                Diagnoz.diagnoz,
                Adress.text,
                Adress.point,
            ]
        ).select_from(
            Meddoc
            .join(MeddocCategory)
            .outerjoin(Patient)
            .outerjoin(Org)
            .join(Case.outerjoin(Doctor).outerjoin(Adress).outerjoin(Diagnoz))
        ).where(
            MeddocCategory.c_id == 1
        ).order_by(
            desc(Meddoc.creation_date)
        ).gino.all()

    COLUMNS = [
        "org",
        "number",
        "data_create",
        "sex",
        "birthdate",
        "age",
        "birthdate_baby",
        "doctor_fio",
        "doctor_cpec",
        "doctor_tel",
        "date_sickness",
        "date_first_req",
        "date_diagnoz",
        "time_SES",
        "mkb",
        "diagnoz",
        "adress",
        "point",
    ]

    df = DataFrame(data=event, columns=COLUMNS)
    now = datetime.now() - timedelta(days=datetime.now().day - 1)
    old = now - relativedelta(month=5)
    MONTH = {
        1: 'Январь',
        2: 'Февраль',
        3: 'Март',
        4: 'Апрель',
        5: 'Май',
        6: 'Июнь',
        7: 'Июль',
        8: 'Август',
        9: 'Сентябрь',
        10: 'Октябрь',
        11: 'Ноябрь',
        12: 'Декабрь',
    }

    df['month'] = to_datetime(df.data_create).dt.month.map(MONTH)

    df.loc[to_datetime(df.data_create) < old, 'month'] = 'Старое'

    dict_sex = {
        True: 'Мужчина',
        False: 'Женщина',
    }
    df.sex = df.sex.map(dict_sex)

    map = folium.Map(
        name='test',
        location=[59.95020, 30.31543],
        zoom_start=11,
        max_zoom=18,
        min_zoom=10,
        min_lat=59.5,
        max_lat=60.5,
        min_lon=29.5,
        max_lon=31,
        max_bounds=True,
        prefer_canvas=True,
        tiles=None,
    )

    folium.TileLayer("CartoDB dark_matter", name='Пневмония').add_to(map)

    for month in df.month.unique():
        marker_cluster = MarkerCluster(
            name=month,
            overlay=True,
            control=True,
        ).add_to(map)

        for row in df.loc[df.month == month].to_dict('records'):
            circle = create_circle(row)
            circle.add_to(marker_cluster)

    folium.LayerControl().add_to(map)
    return map.get_root().render()
