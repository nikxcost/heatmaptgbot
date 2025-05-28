from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from typing import List
from datetime import datetime
import calendar

app = FastAPI()


class DateList(BaseModel):
    dates: List[str]


def build_calendar(dates: List[str]) -> str:
    # Преобразуем входные строки в datetime
    date_objs = [datetime.strptime(d, "%d.%m.%Y").date() for d in dates]

    # Группируем по месяцам
    months = {}
    for date in date_objs:
        key = (date.year, date.month)
        if key not in months:
            months[key] = set()
        months[key].add(date.day)

    # Строим текстовые календари по каждому месяцу
    calendar.setfirstweekday(calendar.MONDAY)
    result = ""
    for (year, month) in sorted(months):
        marked_days = months[(year, month)]
        result += f"Календарь активностей для {year}-{month:02}:\n"
        result += "Пн Вт Ср Чт Пт Сб Вс\n"

        month_cal = calendar.monthcalendar(year, month)
        for week in month_cal:
            line = ""
            for day in week:
                if day == 0:
                    line += "   "
                elif day in marked_days:
                    line += "✅ "
                elif day < 10:
                    line += f"{day}  "
                else:
                    line += f"{day} "
            result += line.rstrip() + "\n"
        result += "\n"

    return result.strip()


@app.post("/generate-calendar/", response_class=PlainTextResponse)
async def generate_calendar(date_list: DateList):
    try:
        calendar_text = build_calendar(date_list.dates)
        return calendar_text  # Возвращаем как обычный текст
    except Exception as e:
        return f"Ошибка: {e}"
