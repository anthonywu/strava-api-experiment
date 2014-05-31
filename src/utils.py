import collections
import datetime
import stravalib.client
import time

class BaseException(Exception):
    pass

class ConfigError(BaseException):
    pass

class MyStravaClient(stravalib.client.Client):

    API_CALL_PAUSE_SECONDS = 1.5  # 40 requests per minute

    def get_all_gears(self):
        all_activities = self.get_activities()
        uniq_gear_ids = filter(None, set(activity.gear_id for activity in all_activities))
        gears = []
        for gear_id in uniq_gear_ids:
            time.sleep(self.API_CALL_PAUSE_SECONDS)
            gears.append(self.get_gear(gear_id))
        return gears

    def get_activities(self, **kwargs):
        return list(stravalib.client.Client.get_activities(self, **kwargs))

    def get_activities_current_month(self, filter_types=['Ride']):
        # get first date of current month
        now = datetime.datetime.now()
        first_of_month = datetime.datetime(now.year, now.month, 1)
        # compile activities since first day of current month
        matches = []
        activities_list = self.get_activities(after=first_of_month)
        for activity in activities_list:
            if activity.type in filter_types:
                matches.append(activity)
        return matches

    def batch_set_privacy(self, activity_ids, private=True):
        updated_ids = []
        for each in activity_ids:
            try:
                self.update_activity(each, private=private)
            except TypeError, e:
                # workaroiund for a bug in stravalib: Rate Limit errors are raised as "TypeError: a float is required"
                time.sleep(15)  # naively cool down for 15 seconds, this works pretty well, implement exponential back-off later
            time.sleep(self.API_CALL_PAUSE_SECONDS)
            updated_ids.append(each)
        return updated_ids


def summarize_gear_usage(activity_list):
    gear_usage_count_lookup = collections.defaultdict(int)
    gear_distance_lookup = collections.defaultdict(float)
    for activity in activity_list:
        gear_usage_count_lookup[activity.gear_id] += 1
        gear_distance_lookup[activity.gear_id] += activity.distance.get_num()
    return dict(gear_usage_count_lookup), dict(gear_distance_lookup)


def summarize(activities_list, short_ride_threshold=5.0):
    summary = {
        'distance': 0.0,
        'count_public': 0,
        'distance_public': 0.0,
        'distance_private': 0.0,
        'private_ids': [],
        'commute_ids': [],
        'short_rides_ids': []
    }
    for activity in activities_list:
        summary['distance'] += activity.distance.get_num()
        activity_distance = activity.distance.get_num()
        if activity.private:
            summary['distance_private'] += activity_distance
            summary['private_ids'].append(activity.id)
        else:
            summary['count_public'] += 1
            summary['distance_public'] += activity_distance

        if (activity_distance / 1000.0) < short_ride_threshold:
            summary['short_rides_ids'].append(activity.id)

        if activity.commute:
            summary['commute_ids'].append(activity.id)
    # convert to kms
    for k in summary:
        if k.startswith('distance'):
            summary[k] = round(summary[k] / 1000.0, 1)
    summary['count_private'] = len(summary['private_ids'])
    summary['count_commute'] = len(summary['commute_ids'])
    return summary

