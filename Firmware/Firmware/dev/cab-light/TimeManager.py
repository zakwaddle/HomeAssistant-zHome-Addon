import utime
import urequests


def get_current_time(timezone='America/New_York'):
    url = f"http://worldtimeapi.org/api/timezone/{timezone}"
    try:
        response = urequests.get(url)
        if response.status_code == 200:
            time_data = response.json()
            c_time = time_data["datetime"]
            response.close()
            return c_time  # Adjust format as needed
        else:
            print("Failed to get time:", response.status_code)
            response.close()
    except Exception as e:
        print("Error getting time:", e)


class TimeManager:
    def __init__(self):
        self.last_sync_time = None  # Timestamp of the last time we synced with the API
        self.last_sync_system_time = None  # System time at last sync

    def sync_time(self):
        """Syncs the current time with the time API."""
        current_time_str = get_current_time()
        if current_time_str:
            try:
                date_part, time_part = current_time_str.split('T')
                time_part = time_part.split('.')[0]  # Remove fractional seconds
                year, month, day = [int(part) for part in date_part.split('-')]
                hour, minute, second = [int(part) for part in time_part.split(':')]

                self.last_sync_time = utime.mktime((year, month, day, hour, minute, second, 0, 0))
                self.last_sync_system_time = utime.ticks_ms()
            except ValueError as e:
                print("Error parsing time string:", e)

    def get_estimated_current_time(self):
        """Estimates the current time based on the last sync and elapsed system time."""
        if self.last_sync_time is None:
            return None
        elapsed = utime.ticks_diff(utime.ticks_ms(), self.last_sync_system_time)
        elapsed_seconds = elapsed // 1000
        estimated_time = utime.localtime(self.last_sync_time + elapsed_seconds)
        return estimated_time

    def is_day_time(self, start_time_str='07:30:00', end_time_str='21:30:00'):
        """Checks if the current estimated time is within day time hours."""
        current_time = self.get_estimated_current_time()
        if current_time is None:
            return False
        # Convert the time tuple to a time string
        current_time_str = "{:02d}:{:02d}:{:02d}".format(current_time[3], current_time[4], current_time[5])

        return start_time_str <= current_time_str <= end_time_str



