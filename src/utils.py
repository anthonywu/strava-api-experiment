import os
from datetime import date
from stravalib.client import Client

class BaseException(Exception):
    pass

class ConfigError(BaseException):
    pass

def get_env_token(env_var_name='STRAVA_ACCESS_TOKEN'):
    try:
        return os.environ[env_var_name]
    except KeyError:
        raise ConfigError('Access Token not defined in environment variable %r' % env_var_name)

def get_client(token):
    return Client(access_token=token)

def get_activities_current_month(activities_list, filter_types=['Ride']):
    today = date.today()
    matches = []
    for activity in activities_list:
        if (activity.start_date_local.year, activity.start_date_local.month) == (today.year, today.month):
            if activity.type in filter_types:
                matches.append(activity)
    return matches

def summarize(activities_list):
    summary = {
        'distance': 0.0,
        'count_public': 0.0,
        'distance_public': 0.0,
        'distance_private': 0.0,
        'private_ids': [],
        'commute_ids': []
    }
    for activity in activities_list:
        summary['distance'] += activity.distance.get_num()
        if activity.private:
            summary['distance_private'] += activity.distance.get_num()
            summary['private_ids'].append(activity.id)
        else:
            summary['count_public'] += 1
            summary['distance_public'] += activity.distance.get_num()
        if activity.commute:
            summary['commute_ids'].append(activity.id)
    # convert to kms
    for k in summary:
        if k.startswith('distance'):
            summary[k] = round(summary[k] / 1000.0, 1)
    summary['count_private'] = len(summary['private_ids'])
    summary['count_commute'] = len(summary['commute_ids'])
    return summary
