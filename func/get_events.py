from pandas import DataFrame, to_datetime
from base import db
from sqlalchemy import desc
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


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


async def get_events(category_id=1) -> 'DataFrame':
    "Вытаскиваем из базы случаи нужной категории"
    event = await db.select(
            [
                Org.short_name,
                Meddoc.meddoc_biz_key,
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
            MeddocCategory.c_id == category_id
        ).order_by(
            desc(Meddoc.creation_date)
        ).gino.all()

    COLUMNS = [
        "org",
        "meddoc_biz_key",
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

    return df
