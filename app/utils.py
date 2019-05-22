import datetime
import pytz


def now():
    time = datetime.datetime.utcnow()
    return time.replace(tzinfo=pytz.utc)


def as_utc_iso(date):
    return date.astimezone(datetime.timezone.utc).isoformat()