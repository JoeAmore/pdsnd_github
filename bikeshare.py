import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    cities = ['chicago', 'new york city', 'washington']
    print('We can analyse data from Chicago, New York City or Washington.')
    city = input('Please type in the city you would like to analyse: ').lower()
    while city not in cities:
        print('Looks like you entered an invalid city. You can select from Chicago, New York City or Washington.')
        city = input('Which city would you like to analyse? ').lower()
    
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    print("We can look at data from all months or any month from January to June.")
    month = input("Please type in the month you would like to analyse or type 'all' for all months: ").lower()
    while month not in months:
        print("Looks like you typed in an invalid option. Please type 'all' or the full name of any month from January to June.")
        month = input("Please type in the month or 'all': ").lower()

    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    print("We can look at data from a particular day of the week or all days.")
    day = input("Please type in the days of the week you would like to analyse or type 'all' for all days: ").lower()
    while day not in days:
        print("Looks like you typed in an invalid option. Please type 'all' or the full name of any day of the week.")
        day = input("Please type in the day of the week or 'all': ").lower()

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) +1
        df = df[df['month'] == month]
    
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    most_common_month = df['month'].mode()[0]
    print("The most common month is : {}".format(most_common_month))    

    most_common_day_of_week = df['day_of_week'].mode()[0]
    print("The most common day of the week is : {}".format(most_common_day_of_week))
    
    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]
    print("The most common start hour is : {}".format(most_common_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    most_common_start_station = df['Start Station'].mode()[0]
    print("The most common start station is : {}".format(most_common_start_station))

    most_common_end_station = df['End Station'].mode()[0]
    print("The most common end station is : {}".format(most_common_end_station))

    df['trip_combination'] = df['Start Station'] + ' to ' + df['End Station']
    most_common_trip_combination = df['trip_combination'].mode()[0]
    print("The most frequent station combination is : {}".format(most_common_trip_combination))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel_time = df['Trip Duration'].sum()
    print("Total travel time is : {}".format(total_travel_time))

    mean_travel_time = df['Trip Duration'].mean()
    print("Mean travel time is : {}".format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_types = df['User Type'].fillna("No data given").value_counts()
    print("Counts of user types : {}".format(user_types))

    if 'Gender' in df:
        user_genders = df['Gender'].fillna("No data given").value_counts()
        print("Counts of user genders : {}".format(user_genders))
    else:
        print('Gender stats cannot be calculated because this data is not available.')

    if 'Birth Year' in df:
        user_birthdays = df['Birth Year']
        print("The earliest user birth year is : {}".format(int(min(user_birthdays.dropna()))))
        print("The most recent user birth year is : {}".format(int(max(user_birthdays.dropna()))))
        print("The most common user birth year is : {}".format(int(user_birthdays.dropna().mode()[0])))
    else:
        print('Birth year stats cannot be calculated because this data is not available.')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
def display_raw_data(df):

    print('Would you like to see the raw data?')
    display_input = input("Please enter 'yes' or 'no' : ").lower()
    display_input_answer = ['yes', 'no']
    
    while display_input not in display_input_answer:
        display_input = input("Please enter 'yes' or 'no' : ").lower()

        
    start_loc = 0
    
    while True:
        if display_input == 'yes':
            start_loc += 5
            print(df.iloc[start_loc : start_loc + 5])
            print("Do you want to see more data?")
            display_again = input("Please type 'yes' or 'no': ").lower()
            while display_again not in display_input_answer:
                display_again = input("Please type 'yes' or 'no'. ").lower()
            if display_again == 'no':
                break
        else:
            break

        
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
