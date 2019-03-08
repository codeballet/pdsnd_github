import time
import pandas as pd
import numpy as np
import re

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington).
    # HINT: Use a while loop to handle invalid inputs
    city = ''
    month = ''
    day = ''

    while True:
        city_input = input\
                ('Which city would you like to see data for: Chicago, New York City, or Washington? ').lower()

        if re.match('^c.*', city_input):
            city = 'chicago'
            print('You chose Chicago')
            break
        
        elif re.match('^n.*', city_input):
            city = 'new york city'
            print('You chose New York City')
            break

        elif re.match('^w.*', city_input):
            city = 'washington'
            print('You chose Washington')
            break

        else:
            print('I did not recognize that city, please try again.')
        
    loop_test = True

    while loop_test:
        filter_input = input('Would you like to filter the data by month, day, or applying no time filter? ')

        if re.match('^m.*', filter_input):
            day = 'all'
            print('You chose to filter by month.')
            # get user input for month (all, january, february, ... , june)
            # testing the raw input for month
            while True:
                month_input = input('Which month (Jan, Feb, Mar, Apr, May, Jun, or all months)? ').lower()

                if re.match('^jan.*', month_input):
                    month = months[0]
                    print('You chose {}'.format(months[0]))
                    loop_test = False
                    break
                
                elif re.match('^feb.*', month_input):
                    month = months[1]
                    print('You chose {}'.format(months[1]))
                    loop_test = False
                    break
                
                elif re.match('^mar.*', month_input):
                    month = months[2]
                    print('You chose {}'.format(months[2]))
                    loop_test = False
                    break
                
                elif re.match('^apr.*', month_input):
                    month = months[3]
                    print('You chose {}'.format(months[3]))
                    loop_test = False
                    break
                
                elif re.match('^may.*', month_input):
                    month = months[4]
                    print('You chose {}'.format(months[4]))
                    loop_test = False
                    break
                
                elif re.match('^jun.*', month_input):
                    month = months[5]
                    print('You chose {}'.format(months[5]))
                    loop_test = False
                    break
                
                elif re.match('^a.*', month_input):
                    month = months[6]
                    print('You chose {} months'.format(months[6]))
                    loop_test = False
                    break
                
                else:
                    print('I did not recognize that month, please try again.')

        elif re.match('^d.*', filter_input):
            month = 'all'
            print('You chose to filter by day.')
            # get user input for day of week (all, monday, tuesday, ... sunday)
            # testing the raw input for day
            while True:
                day_input = input('Which day (Mo, Tu, We, Th, Fr, Sa, Su, or all days)? ').lower()

                if re.match('^mo.*', day_input):
                    day = 1 
                    print('You chose Monday')
                    loop_test = False
                    break

                elif re.match('^tu.*', day_input):
                    day = 2
                    print('You chose Tuesday')
                    loop_test = False
                    break

                elif re.match('^we.*', day_input):
                    day = 3
                    print('You chose Wednesday')
                    loop_test = False
                    break

                elif re.match('^th.*', day_input):
                    day = 4
                    print('You chose Thursday')
                    loop_test = False
                    break

                elif re.match('^fr.*', day_input):
                    day = 5
                    print('You chose Friday')
                    loop_test = False
                    break

                elif re.match('^sa.*', day_input):
                    day = 6
                    print('You chose Saturday')
                    loop_test = False
                    break

                elif re.match('^su.*', day_input):
                    day = 0
                    print('You chose Sunday')
                    loop_test = False
                    break

                elif re.match('^a.*', day_input):
                    day = 'all'
                    print('You chose all days')
                    loop_test = False
                    break

                else:
                    print('I did not recognize that day, please try again.')

        elif re.match('^n.*', filter_input):
            month = 'all'
            day = 'all'
            print('No time filters will be applied.')
            loop_test = False
            break

        else:
            print('Apologies, I did not understand your choice, please try again.')

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
    # give summary of the user choices
    if day == 'all':
        print('You have chosen to filter by:\ncity: ', city, '\nmonth: ', month, '\nday: all')

    else:
        print('You have chosen to filter by:\ncity: ', city, '\nmonth: ', month, '\nday: ', days[day])

    # load the dataframe
    df = pd.read_csv(CITY_DATA[city])
    
    # convert time columns to datetime and create new month and day_of_week columns
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list at the top to get the corresponding int
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day_of_week if applicable
    if day != 'all':
        # filter by day_of_week, remember my day is already an int
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]

    if month != 'all':
        print('Your chosen month, {}, is obviously also the most popular month, {}, in this particular analysis.'\
                .format(month, months[popular_month - 1]))

    else:
        print('The most popular month is {}'.format(months[popular_month - 1]))

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]

    if day != 'all':
        print("Your chosen day, {}, is obviously also the most popular day, {}, in this particular analysis."\
        .format(days[day], days[popular_day]))

    else:
        print('The most popular day is {}'.format(days[popular_day]))

    # display the most common start hour
    df['start_hour'] = df['Start Time'].dt.hour
    popular_hour = df['start_hour'].mode()[0]
    print('The most popular start hour is {}:00'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_startpoint = df['Start Station'].mode()[0]
    print('The most popular station to start from is {}'.format(popular_startpoint))

    # display most commonly used end station
    popular_endpoint = df['End Station'].mode()[0]
    print('The most popular station to end at is {}'.format(popular_endpoint))


    # display most frequent combination of start station and end station trip
    # create a new dataframe of popular routes, sorted in descending order
    df_popular_route = df.groupby(['Start Station', 'End Station']).size().sort_values(ascending = False).reset_index()

    # print the route on the top row of the df_popular_route dataframe
    print('The most popular route is from "{}" to "{}".'\
            .format(df_popular_route['Start Station'][0], df_popular_route['End Station'][0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    # calculate the hours, minutes, and seconds of the total travel time
    h = int(total_time // 3600)
    m = int((total_time % 3600) // 60)
    s = int((total_time % 3600) % 60)

    print('Total travel time is {} hours, {} minutes, and {} seconds'.format(h, m, s))

    # display mean travel time
    mean_time = df['Trip Duration'].mean()
    # calculate the hours, minues, and seconds of the mean travel time
    h = int(mean_time // 3600)
    m = int((mean_time % 3600) // 60)
    s = int((mean_time % 3600) % 60)

    print('Mean travel time is {} hours, {} minutes, and {} seconds'.format(h, m, s))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('The amount of subscribers are {}'.format(user_types['Subscriber']))
    print('The amount of customers are {}'.format(user_types['Customer']))

    # Display counts of gender
    # Check if gender data is available
    if df.columns.isin(['Gender']).any():
        gender_types = df['Gender'].value_counts()
        print('\nThe number of male subscibers is {}'.format(gender_types['Male']))
        print('The number of female subscibers is {}'.format(gender_types['Female']))

    else:
        print('\nNo gender recorded.')

    # Display earliest, most recent, and most common year of birth
    # Check if birth data is available
    if df.columns.isin(['Birth Year']).any():
        birth_year = df['Birth Year']
        print('\nThe earliest year of birth is {}'.format(int(birth_year.min())))
        print('The most recent year of birth is {}'.format(int(birth_year.max())))
        print('The most common year of birth is {}'.format(int(birth_year.mode()[0])))

    else:
        print('\nNo year of birth recorded.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    # ask the user if the raw data should be presented or not
    more_data = input('Would you like to see the raw data (yes or no)? ').lower()

    # check the user's response
    if re.match('^y.*', more_data):
        # use a generator to present chunks of the raw data
        index = df.index.values

        def chunker(df):
            i = 0
            interrupt = 'yes'

            for i in range(0, index[-1], 5):
                yield df[i:i + 5]

        for chunk in chunker(df):
            print(chunk)
            interrupt = input("To see more data, just keep pressing that 'return' key. When you had enough, type 'stop'").lower()

            if re.match('^s.*', interrupt):
                print("I'm done, thank you for your enquiry.") 
                break

    else:
        print("Well, since you're not interested, I'm done. Thank you for your enquiry.") 

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
