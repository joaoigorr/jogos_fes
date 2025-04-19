from urllib.parse import urlencode

def create_event(title, date, time, duration_minutes, description="", location=""):
    base_url = "https://calendar.google.com/calendar/render?action=TEMPLATE"
    params = {
        "text": title,
        "dates": f"{date}T{time.replace(':', '')}-03:00/{date}T{(int(time[:2]) + duration_minutes // 60):02d}{(int(time[3:]) + duration_minutes % 60):02d}-03:00",
        "details": description,
        "location": location
    }
    url = f"{base_url}&{urlencode(params)}"
    return url