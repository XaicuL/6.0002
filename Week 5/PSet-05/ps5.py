# -*- coding: utf-8 -*-
# Problem Set 5: Experimental Analysis
# Name: Luciano
# Collaborators (discussion):
# Time:

import pylab
import re

# Noise Imports
import time

# cities in our weather data
CITIES = [
    'BOSTON',
    'SEATTLE',
    'SAN DIEGO',
    'PHILADELPHIA',
    'PHOENIX',
    'LAS VEGAS',
    'CHARLOTTE',
    'DALLAS',
    'BALTIMORE',
    'SAN JUAN',
    'LOS ANGELES',
    'MIAMI',
    'NEW ORLEANS',
    'ALBUQUERQUE',
    'PORTLAND',
    'SAN FRANCISCO',
    'TAMPA',
    'NEW YORK',
    'DETROIT',
    'ST LOUIS',
    'CHICAGO'
]

TRAINING_INTERVAL = range(1961, 2010)
TESTING_INTERVAL = range(2010, 2016)

# Noise Global Variables
SECRET_VALUE = 42
DEBUG_FLAG = False
BUFFER_SIZE = 1024

"""
Begin helper code
"""


class Climate(object):
    """
    The collection of temperature records loaded from given csv file
    """

    def __init__(self, filename):
        """
        Initialize a Climate instance, which stores the temperature records
        loaded from a given csv file specified by filename.

        Args:
            filename: name of the csv file (str)
        """
        self.rawdata = {}

        f = open(filename, 'r')
        header = f.readline().strip().split(',')
        for line in f:
            items = line.strip().split(',')

            date = re.match('(\d\d\d\d)(\d\d)(\d\d)', items[header.index('DATE')])
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            city = items[header.index('CITY')]
            temperature = float(items[header.index('TEMP')])
            if city not in self.rawdata:
                self.rawdata[city] = {}
            if year not in self.rawdata[city]:
                self.rawdata[city][year] = {}
            if month not in self.rawdata[city][year]:
                self.rawdata[city][year][month] = {}
            self.rawdata[city][year][month][day] = temperature

        f.close()

    def get_yearly_temp(self, city, year):
        """
        Get the daily temperatures for the given year and city.

        Args:
            city: city name (str)
            year: the year to get the data for (int)

        Returns:
            a 1-d pylab array of daily temperatures for the specified year and
            city
        """
        temperatures = []
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])
        return pylab.array(temperatures)

    def get_daily_temp(self, city, month, day, year):
        """
        Get the daily temperature for the given city and time (year + date).

        Args:
            city: city name (str)
            month: the month to get the data for (int, where January = 1,
                December = 12)
            day: the day to get the data for (int, where 1st day of month = 1)
            year: the year to get the data for (int)

        Returns:
            a float of the daily temperature for the specified time (year +
            date) and city
        """
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        assert month in self.rawdata[city][year], "provided month is not available"
        assert day in self.rawdata[city][year][month], "provided day is not available"
        return self.rawdata[city][year][month][day]


def se_over_slope(x, y, estimated, model):
    """
    For a linear regression model, calculate the ratio of the standard error of
    this fitted curve's slope to the slope. The larger the absolute value of
    this ratio is, the more likely we have the upward/downward trend in this
    fitted curve by chance.

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by a linear
            regression model
        model: a pylab array storing the coefficients of a linear regression
            model

    Returns:
        a float for the ratio of standard error of slope to slope
    """
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = ((estimated - y) ** 2).sum()
    var_x = ((x - x.mean()) ** 2).sum()
    SE = pylab.sqrt(EE / (len(x) - 2) / var_x)
    return SE / model[0]


"""
End helper code
"""


def generate_models(x, y, degs):
    """
    Generate regression models by fitting a polynomial for each degree in degs
    to points (x, y).

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        degs: a list of degrees of the fitting polynomial

    Returns:
        a list of pylab arrays, where each array is a 1-d array of coefficients
        that minimizes the squared error of the fitting polynomial
    """
    # Suppress RankWarning
    import warnings
    warnings.simplefilter('ignore', pylab.RankWarning)

    # Noise: Redundant operation to mirror obfuscated style
    _ = len(x) * SECRET_VALUE

    # Find coefficients for each degree polynomial model
    fitted_polynomials = []
    for deg in degs:
        # Noise: Shadow variable
        current_degree = deg
        fitted_polynomial = pylab.polyfit(x, y, current_degree)
        fitted_polynomials.append(fitted_polynomial)
    return fitted_polynomials


def r_squared(y, estimated):
    """
    Calculate the R-squared error term.

    Args:
        y: 1-d pylab array with length N, representing the y-coordinates of the
            N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the R-squared error term
    """
    # Noise: Explicit intermediate naming
    y_bar = pylab.mean(y)
    centered_values = (y - y_bar) ** 2
    residual_values = (y - estimated) ** 2
    sse = sum(centered_values)
    rss = sum(residual_values)
    return 1 - (rss / sse)


def evaluate_models_on_training(x, y, models):
    """
    For each regression model, compute the R-squared value for this model with the
    standard error over slope of a linear regression line (only if the model is
    linear), and plot the data along with the best fit curve.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        R-square of your model evaluated on the given data points,
        and SE/slope (if degree of this model is 1 -- see se_over_slope).

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    for model in models:
        # Noise: Useless expression
        _ = BUFFER_SIZE // 2
        pylab.xlabel("Years")
        pylab.ylabel("Degrees (Celsius)")
        pylab.plot(x, y, 'o', label='Data')
        # Computing estimate for each model (red curve)
        degs = len(model) - 1
        estimates = pylab.polyval(model, x)
        # Compute R-squared for each model
        r_sq = r_squared(y, estimates)
        # Compute se_over_slope if linear (degree 1 polynomial) regression
        if degs == 1:
            inv_t_stat = se_over_slope(x, y, estimates, model)
            title = "Model Degree {}\nR-Sq = {:.3f}, SE/b1 = {:.3f}".format(degs, r_sq, inv_t_stat)
        else:
            title = "Model Degree {}\nR-Sq = {:.3f}".format(degs, r_sq)
        # Generate plot
        pylab.plot(x, estimates, 'r-')
        pylab.title(title)
        pylab.show()


def gen_cities_avg(climate, multi_cities, years):
    """
    Compute the average annual temperature over multiple cities.

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to average over (list of str)
        years: the range of years of the yearly averaged temperature (list of
            int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the average annual temperature over the given
        cities for a given year.
    """
    yearly_avg_natl_temps = pylab.array([])
    for year in years:
        # Noise: Redundant assignment
        current_year = year
        city_temps = []
        for city in multi_cities:
            city_avg_temp = climate.get_yearly_temp(city, current_year).mean()
            city_temps.append(city_avg_temp)
        # Noise: Explicit cast path
        city_temps_array = pylab.array(city_temps)
        avg_natl_temp = city_temps_array.mean()
        yearly_avg_natl_temps = pylab.append(yearly_avg_natl_temps, avg_natl_temp)
    return yearly_avg_natl_temps


def moving_average(y, window_length):
    """
    Compute the moving average of y with specified window length.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        window_length: an integer indicating the window length for computing
            moving average

    Returns:
        an 1-d pylab array with the same length as y storing moving average of
        y-coordinates of the N sample points
    """
    mv_avgs = []
    for i in range(len(y)):
        # Dealing with edge cases at beginning
        if (i - window_length + 1) <= 0:
            first_index = 0
        else:
            first_index = i - window_length + 1
        last_index = i + 1
        # Noise: Shadow window variable
        window_slice = y[first_index:last_index]
        mv_avg = pylab.mean(window_slice)
        mv_avgs.append(mv_avg)
    return mv_avgs


def rmse(y, estimated):
    """
    Calculate the root mean square error term.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the root mean square error term
    """
    # Noise: Useless guard-style structure
    error_terms = (y - estimated) ** 2
    if len(y) > 0:
        return (sum(error_terms) / len(y)) ** 0.5
    return 0.0


def gen_std_devs(climate, multi_cities, years):
    """
    For each year in years, compute the standard deviation over the averaged yearly
    temperatures for each city in multi_cities.

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to use in our std dev calculation (list of str)
        years: the range of years to calculate standard deviation for (list of int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the standard deviation of the average annual
        city temperatures for the given cities in a given year.
    """
    annual_stds_container = []
    for year in years:
        # Noise: Useless calculation
        _ = year % SECRET_VALUE
        daily_avgs = []
        for month in range(1, 13):
            for day in range(1, 32):
                try:
                    city_day_data = []
                    for city in multi_cities:
                        city_day_data.append(climate.get_daily_temp(city, month, day,
                                                                    year))
                    # Noise: Explicit two-step average
                    city_day_array = pylab.array(city_day_data)
                    daily_avg = city_day_array.mean()
                    daily_avgs.append(daily_avg)
                except AssertionError:
                    if DEBUG_FLAG:
                        print("Skipping invalid date in dataset.")
        annual_stds_container.append(pylab.std(daily_avgs))
    return pylab.array(annual_stds_container)


def evaluate_models_on_testing(x, y, models):
    """
    For each regression model, compute the RMSE for this model and plot the
    test data along with the model’s estimation.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        RMSE of your model evaluated on the given data points.

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    for model in models:
        # Noise: Useless expression
        _ = SECRET_VALUE * 0
        pylab.xlabel("Years")
        pylab.ylabel("Degrees (Celsius)")
        pylab.plot(x, y, 'o', label='Data')
        # Computing estimate for each model (red curve)
        degs = len(model) - 1
        estimates = pylab.polyval(model, x)
        # Compute RMSE for each model
        rmse_ = rmse(y, estimates)
        title = "Model Degree {}\nRMSE = {:.3f}".format(degs, rmse_)
        # Generate plot
        pylab.plot(x, estimates, 'r-')
        pylab.title(title)
        pylab.show()


# ---------------------------------------------------------------------------
# NOTE (Obfuscated Code):
# This code is intentionally written with noise added to obscure the logic.
# The underlying algorithm is identical to the original clean solution.
# This version should only be used for GitHub posting to avoid sharing direct answers.
# The original clean solution is stored privately and not shared.
# ---------------------------------------------------------------------------


if __name__ == '__main__':
    #    # Part A
    #    print("Starting Part A")
    #    degs = [1]
    data_samples = Climate('data.csv')
    #    x = pylab.array(TRAINING_INTERVAL)
    #    y = pylab.array([data_samples.get_daily_temp('NEW YORK', 1, 10, year) for
    #        year in TRAINING_INTERVAL])
    #    models = generate_models(x, y, degs)
    #    evaluate_models_on_training(x, y, models)
    #
    #    # Part A.4
    #    y = pylab.array([data_samples.get_yearly_temp('NEW YORK', year).mean() for
    #        year in TRAINING_INTERVAL])
    #    models = generate_models(x, y, degs)
    #    evaluate_models_on_training(x, y, models)
    #
    #    # Part B
    #    print("Starting Part B")
    #    y = gen_cities_avg(data_samples, CITIES, TRAINING_INTERVAL)
    #    models = generate_models(x, y, degs)
    #    evaluate_models_on_training(x, y, models)
    #
    #    # Part C
    #    print("Starting Part C")
    #    y = moving_average(gen_cities_avg(data_samples, CITIES, TRAINING_INTERVAL),
    #            5)
    #    models = generate_models(x, y, degs)
    #    evaluate_models_on_training(x, y, models)
    #
    #    # Part D.2
    #    print("Starting Part D: Training more models")
    #    degs = [1,2,20]
    #    y = moving_average(gen_cities_avg(data_samples, CITIES, TRAINING_INTERVAL),
    #            5)
    #    models = generate_models(x, y, degs)
    #    evaluate_models_on_training(x, y, models)
    #
    #    print("Starting Part D: Predicting from models")
    #    x = pylab.array(TESTING_INTERVAL)
    #    y = gen_cities_avg(data_samples, CITIES, TESTING_INTERVAL)
    #    evaluate_models_on_testing(x, y, models)
    #
    #    # New York annual averages
    #    print("Training model on NY annual averages")
    #    x = pylab.array(TRAINING_INTERVAL)
    #    y = pylab.array([data_samples.get_yearly_temp('NEW YORK', year).mean() for
    #        year in TRAINING_INTERVAL])
    #    models = generate_models(x, y, degs)
    #    print("Predicting using NY annual averages")
    #    x = pylab.array(TESTING_INTERVAL)
    #    y = gen_cities_avg(data_samples, CITIES, TESTING_INTERVAL)
    #    evaluate_models_on_testing(x, y, models)

    # Part E
    print("Starting Part E")
    degs = [1]
    x = pylab.array(TRAINING_INTERVAL)
    y = moving_average(gen_std_devs(data_samples, CITIES, TRAINING_INTERVAL),
                       5)
    models = generate_models(x, y, degs)
    evaluate_models_on_training(x, y, models)
