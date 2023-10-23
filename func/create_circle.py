import folium


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
              }""" + f"""
            </style>
            <table cellpadding="1" cellspacing="0"  bordercolor="white" border="0" class="table">
              <thead>
                <tr>
                  <th colspan="2" scope="col" class="table__heading">{row['org']}</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td colspan="2" class="table__cell table__cell--highlighted">{row['mkb']} {row['sex']}  Возраст: {row['age']} </td>
                </tr>
                 <tr>
                  <td colspan="2" class="table__cell table__cell--highlighted">{row['diagnoz']}</td>
                </tr>
                <tr>
                  <td colspan="2" class="table__cell table__cell--highlighted"> key: {row['meddoc_biz_key']}</td>
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
