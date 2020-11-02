from meetingtime import MeetingTime
import json
import pandas
import re
import pprint


class MeetingTimeData:
    """
    This class handles creating objects for Meeting Times
    """

    def __init__(self, file_path):
        meetingTimeData = pandas.read_excel(file_path, sheet_name='Meeting Times')
        json_str = meetingTimeData.to_json()
        data = json.loads(json_str)
        self.meeting_times = []
        self._meeting_times = []

        data_keys = data.keys()
        for each_key in data_keys:
            input_str = each_key.upper().strip()

             # trying to match "M or W or F or MWF or MW or WF or MF, 50 min" patters
            if re.match(r"^([A-Z]{1,4}(\sor\s)?)+,\s\d{1,3}\s?(min|hr)\s*$", input_str) is None:
                print("Unexpected header name: " + input_str +
                      "\nHeader of each column in Meeting Times Sheet should match the following format:"
                      " 'M or W or F or MWF or MW or WF or MF, 50 min'")
                raise Exception

            all_the_days, duration = self._parse_days(each_key)
            for each_day in all_the_days:
                for each_time_slot in data.get(each_key).values():
                    if each_time_slot is None or "Common Break" in each_time_slot:
                        continue
                    else:
                        self.meeting_times.append((MeetingTime(each_day, duration, each_time_slot)))
                        self._meeting_times.append((MeetingTime(each_day, duration, each_time_slot)))

    def _parse_days(self, days_duration_string):
        """
         input: "M or W or F, 2 hr, MW or WF or FM, 2hr'
         output : ['M', 'W', 'F', ..], 2hr

        """
        all_the_days = []
        items = days_duration_string.split(',')
        duration = items[-1].strip()
        for i, item in enumerate(items):
            if i % 2 == 0:
                days = item.split('or')
                for day in days:
                    all_the_days.append(day.strip())

        return all_the_days, duration

    def get_meeting_times_objects_list(self):
        return self._meeting_times
