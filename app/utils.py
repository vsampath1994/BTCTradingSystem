from datetime import datetime,timedelta
from dateutil import rrule

def dateCount(rule, startDate, endDate):
    x = rrule.rrule(rule, dtstart=startDate, until=endDate)
    return x.count()

def numberOfWeeks(startDate, endDate):
    return dateCount(rrule.WEEKLY, startDate, endDate)

def numberOfMonths(startDate, endDate):
    return dateCount(rrule.MONTHLY, startDate, endDate)

def numberOfDays(startDate, endDate):
    return dateCount(rrule.DAILY, startDate, endDate)

def dateFromString(sdate):
    date = datetime.strptime(sdate, '%Y-%m-%d %H:%M:%S')
    return date

def calculateAverage(startDate, endDate, count):
    avgDict = {}

    days = numberOfDays(dateFromString(startDate), dateFromString(endDate))
    weeks = numberOfWeeks(dateFromString(startDate), dateFromString(endDate))
    months = numberOfMonths(dateFromString(startDate), dateFromString(endDate))

    if days == 0:
        days = 1
    if weeks == 0:
        weeks = 1
    if months == 0:
        months = 1

    print "Total Count: " + str(count)
    print "Total days: "  + str(days)
    print "Total weeks: " + str(weeks)
    print "Total months: "+ str(months)
    avgDict['daily'] = count/days
    avgDict['monthly'] = count/months
    avgDict['weekly'] = count/weeks
    return avgDict

def convertToMonthlyHistogramData(startDate, weeklyVolume):
    start = dateFromString(startDate)
    week = 1

    monthlyData = []
    monthTotal = 0

    month = start.month

    for data in weeklyVolume:
        if start.month != month:
            monthlyData.append(monthTotal)
            monthTotal = 0
            month = start.month
        start = start + timedelta(7)
        print start
        monthTotal += data

    if monthTotal != 0:
        monthlyData.append(monthTotal)
    print monthlyData
    return monthlyData

def convertToWeeklyHistogramData(startDate, dailyVolume):
    start = dateFromString(startDate)
    day = 1

    weeklyData = []
    weekTotal = 0
    for data in dailyVolume:
        if start.weekday() == 6:
            print start
            weeklyData.append(weekTotal)
            weekTotal = 0
        start = start + timedelta(day)
        weekTotal += data

    if weekTotal != 0:
        weeklyData.append(weekTotal)
    print weeklyData
    return weeklyData

def convertToDailyHistogramData(endDate, startDate, orderTransactions, paymentTransactions):
    end = dateFromString(endDate)
    start = dateFromString(startDate)

    count = {}
    for order in orderTransactions:
        date = order.timestamp
        if (date - start).days in count:
            v = count[(date-start).days]
        else:
            v = 0

        count[(date-start).days] = (v+1)

    for payment in paymentTransactions:
        date = payment.timestamp
        if (date - start).days in count:
            v = count[(date-start).days]
        else:
            v = 0

        count[(date-start).days] = (v+1)

    histogram = []
    for i in range(0,(end-start).days+1):
        if not i in count:
            histogram.append(0)
        else:
            histogram.append(count[i])


    print histogram
    return histogram
