from sense_hat import SenseHat
from readingRanges import ReadingRanges
from climateReading import ClimateReading


# TODO DB class details can go in a seperate py file
# as analytics needs to use the same info.
# Adds reuseability. Just need to import the module

class MonitorAndNotify:
    def __init__(self, range_config):
        self.range_config = range_config
    def run(self):
        sense = SenseHat()
        ReadingRanges.update_defaults_from_json(self.range_config)
        current_reading = ClimateReading.from_sensehat(sense)

        # TODO Change based on DB implementation
        # This goes for all the db function calls
        current_reading.write_to_db("db_info")

        if current_reading.outside_config_range(ReadingRanges):
            if not current_reading.notified_pushbullet_today("db_info"):
                current_reading.notify_pushbullet()
                current_reading.update_notify_today_status("db_info")

monitorAndNotify = MonitorAndNotify("config.json")
monitorAndNotify.run()