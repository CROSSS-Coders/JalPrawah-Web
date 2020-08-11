import numpy as np

from datetime import datetime, timedelta


def make_forecast(highest_flood_level, danger_level, warning_level,  water_values, time):
    '''
    Makes forecast based on water values vs time
    Returns future water levels and forecasted % of water in each section
    '''

    current_window_size = len(time)
    # print(len(water_values), len(time))
    change_value = _calculate_weighted_change(
        current_window_size, water_values)
    if change_value != 0:
        forecast = np.arange(
            water_values[-1], water_values[-1] + change_value, change_value / current_window_size)
    else:
        forecast = np.array(water_values)

    last_reading = datetime.strptime(time[-1], '%Y-%m-%d:%H')
    f_time = [(last_reading + timedelta(hours=i)).strftime('%Y-%m-%d:%H')
              for i in range(len(forecast))]

    percent_normal, percent_warning, percent_danger, percent_hfl = _get_levels(
        forecast, warning_level, danger_level, highest_flood_level)

    return {'values': forecast.tolist(), 'time': f_time}, {'normal': percent_normal, 'warning': percent_warning, 'danger': percent_danger, 'hfl': percent_hfl}


def _get_levels(forecast, warning_level, danger_level, highest_flood_level):

    percent_normal = (forecast < warning_level).sum() / \
        len(forecast) if warning_level is not None else None
    percent_warning = ((warning_level <= forecast) & (forecast < danger_level)).sum(
    ) / len(forecast) if warning_level is not None and danger_level is not None else None
    percent_danger = ((danger_level <= forecast) & (forecast < highest_flood_level)).sum(
    ) / len(forecast) if danger_level is not None and highest_flood_level is not None else None
    percent_hfl = (forecast >= highest_flood_level).sum() / \
        len(forecast) if highest_flood_level is not None else None

    return percent_normal, percent_warning, percent_danger, percent_hfl


def _calculate_weighted_change(current_window_size, water_values):
    change_sum = 0
    for i in range(current_window_size, 1, -1):
        change_sum += (1 / i) * (water_values[-(i - 1)] - water_values[-i])
    return change_sum
