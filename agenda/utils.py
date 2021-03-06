from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import Event
from dashboard.models import Irrigation
import datetime as dt


class Calendar(HTMLCalendar):

    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    # formats a day as a td
    # filter events by day
    def formatday(self, day, events, irrigations):
        events_per_day = events.filter(start_time__day=day)
        irrigations_per_day = irrigations.filter(date__day=day)
        today = dt.datetime.today()
        if today.year != self.year or today.month != self.month:
            today = None
        d = ''
        if today and today.day == day:
            d=f'<b style ="position: absolute; margin-top: -20px; margin-left:-20px; color:rgba(160, 197, 141, 1); font-size:18px; background-color:white; line-height: 18px">{day}</b>'
        for event in events_per_day:
            d += f'<li style="background-color:{event.color}; list-style:none;"> {event.get_html_url} </li>'
        for irrigation in irrigations_per_day:
            d += f'<a tabindex="0"  role="button" data-toggle="popover" data-trigger="focus" title="{irrigation.get_irrigation_type_display()}" data-content="durata: {irrigation.get_duration()} minuti" class="event_caption">{irrigation.area}</a><br>'

        if day != 0:
            return f'<td><span class="date">{day}</span><ul> {d} </ul></td>'
        return '<td></td>'

    # formats a week as a tr
    def formatweek(self, theweek, events, irrigations):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events, irrigations)
        return f'<tr> {week} </tr>'

    # formats a month as a table
    # filter events by year and month
    def formatmonth(self, user, withyear=True):
        events = Event.objects.filter(start_time__year=self.year, start_time__month=self.month, user=user)
        irrigations = Irrigation.objects.filter(date__year=self.year, date__month=self.month, area__garden__user=user)
        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events, irrigations)}\n'
        return cal
