import subprocess
import datetime


class Command:
    def __init__(self):
        self._keywords = None

    def update(self, user_input, dir_loc):
        available_types = {"array":"\[\]"}
        available_options = {"submitted":";S;", "restarted":";R;",\
        "queued": ";Q;", "finished":";E;"}
        self._job_type = find_optype(user_input, available_types)
        self._job_option = find_optype(user_input, available_options)
        self._save = False
        self._date_start = datetime.datetime.now()
        self._date_end = datetime.datetime.now()
        self._dir_loc = dir_loc
        self._command = None

        self.init_date(user_input)
        print("Search Start Date: ",self._date_start)
        print("Search End Date: ",self._date_end)

    def init_date(self, user_input):
        date_keywords = {"today": 0, "yesterday": -1, "days": -1, "week": -7,\
        "weeks":-7,"months":-30, "month": -30, "year": -365}
        time_keywords = ("in", "since")
        for date_key in date_keywords:
            if date_key in user_input:
                modifier = 1
                possible_date_number = user_input.index(date_key)-1
                if user_input[possible_date_number].isnumeric():
                    modifier = int(user_input[possible_date_number])
                self._date_start = self.calc_date(date_keywords[date_key]*modifier)
                for element in time_keywords:
                    if element in user_input:
                        return
                self._date_end = self.calc_date(date_keywords[date_key]*modifier)
    
    def calc_date(self, days):
        return datetime.datetime.now()+\
        datetime.timedelta(days=days+1)

    def keywords(self):
        return self._keywords
    
    def modular_egrep(self, date_start, date_end):
        date = date_start
        command = self._command
        result = []
        while date < date_end + datetime.timedelta(hours=1):
            date_ymd = str(date.year)+str(date.month).zfill(2)+str(date.day).zfill(2)
            data_day = (str(subprocess.run(['egrep', command, str(self._dir_loc+date_ymd)], stdout=subprocess.PIPE)).split("\\n"))
            result.extend(data_day[5:-1])
            date += datetime.timedelta(days=1)
        return result

class Story(Command):
    def __init__(self):
        self._keywords = ["story", "about"]
    
    def process(self, user_input, dir_loc):
        self.update(user_input, dir_loc)
        self.modular_egrep(self._date_start, self._date_end)

class Number(Command):
    def __init__(self):
        self._keywords = ["many", "number"]

    def process(self, user_input, dir_loc):
        self.update(user_input, dir_loc)
        self._command = self._job_option+".*"+self._job_type
        print("Command Executed: egrep", self._command)
        result = self.modular_egrep(self._date_start, self._date_end)
        print(len(result))

class Stats(Command):
    def __init__(self):
        self._keywords = ["stats", "average"]
        self._special_words = {"daily": 1, "weekly":7, "monthly": 30}
    
    def process(self, user_input, dir_loc):
        self.update(user_input, dir_loc)
        self._command = self._job_option+".*"+self._job_type
        print("Command Executed: egrep", self._command)
        date_delta = datetime.timedelta(days=1)
        for key in self._special_words:
            if key in user_input:
                date_delta = datetime.timedelta(days=self._special_words[key])
        date = self._date_start
        date_chunk_end = date + date_delta - datetime.timedelta(days=1)
        total, count = 0, 0
        while date_chunk_end < self._date_end + datetime.timedelta(hours=1):
            result = len(self.modular_egrep(date,date_chunk_end))
            total += result
            date += date_delta
            date_chunk_end += date_delta
            count += 1
        avg = total/(count)
        print(avg)

def find_optype(user_input, available):
    for entry in available:
        if entry in user_input:
            return available[entry]
    return ""