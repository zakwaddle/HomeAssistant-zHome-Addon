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


def is_day_time(target_time_str, start_time_str='07:30:00', end_time_str='21:30:00'):
    # Extract the time part from the datetime string
    time_part = target_time_str.split('T')[1].split('+')[0]

    # Compare with the start and end times
    return start_time_str <= time_part <= end_time_str
