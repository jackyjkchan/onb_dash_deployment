# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 12:50:35 2019

@author: Tammi Hawa
"""

import numpy as np
# import math
import pandas as pd
import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
import scipy.stats as stats
import time

# import plotly
import plotly as py
import plotly.graph_objs as go
from dateutil.rrule import *


# begin with methods


def run(args, offline=False):
    # inputs from user
    item_name = args["item_name"] if "item_name" in args else '#1308_Suture'
    # small s for items, reorder level
    min_level = args["min_level"] if "min_level" in args else 150
    # order up to level
    max_level = args["max_level"] if "max_level" in args else 200
    # frequency of review, in days
    frequency = args["frequency"] if "frequency" in args else 2
    # initial inventory level
    current_inventory_level = args["current_inventory_level"] if "current_inventory_level" in args else 110

    # initialize weekend parameters
    # initialize weekday usage parameters
    # minimum amount of inventory used on a typical weekday
    min_weekday_usage = args["min_weekday_usage"] if "min_weekday_usage" in args else 0
    mode_weekday_usage = args["mode_weekday_usage"] if "mode_weekday_usage" in args else 28
    max_weekday_usage = args["max_weekday_usage"] if "max_weekday_usage" in args else 75

    # prop_weekend = 0.22 #proportion of inventory amounts used on weekends
    min_weekend_usage = args["min_weekend_usage"] if "min_weekend_usage" in args else 0
    mode_weekend_usage = args["mode_weekend_usage"] if "mode_weekend_usage" in args else 2
    max_weekend_usage = args["max_weekend_usage"] if "max_weekend_usage" in args else 16

    # initialize leadtime parameters
    min_lt = args["min_lt"] if "min_lt" in args else 1
    mode_lt = args["mode_lt"] if "mode_lt" in args else 2
    max_lt = args["max_lt"] if "max_lt" in args else 3
    
    # include unit of measure
    unit_of_order = args["unit_of_measure"] if "unit_of_measure" in args else 1 #units that orders can be placed in, default is 1


    RunLength = args["RunLength"] if "RunLength" in args else 100  # runlength of sim, the planing horizon inputted by the user
    num_reps = args["num_reps"] if "num_reps" in args else 2000  # number of reps

    # create space to store stats for each rep
    items_in_inventory = []  # quantity of items being held
    stockouts_occur = []  # num of stockouts
    date_of_stockout = []  # date of stockout
    order_is_placed = []  # num of orders
    date_of_order = []  # date order is placed
    order_vol = []  # volume of orders arrived
    fill_rate = []  # record fill rate per period

    # schedule of order volumes and dates of delivery arrival
    delivery_schedule = []
    orderq_schedule = []
    remove_indices = []

    # days of week groups for each item
    week_days = [0, 1, 2, 3, 4]

    # set the seed
    np.random.seed(1)

    start_time = time.time()
    # main simulation loop

    # save stats on all 25 reps
    AllProbStockout = []
    AllMeanInvLevel = []
    # AllNumOrders = []
    AllFillRate = []
    AllMinInvLevel = []
    AllMaxInvLevel = []
    AllDaysInvLevel = []

    AllInvPosition = []

    # generate usage for a particular day of the week for a particular item
    def usage(day_of_week):
        if day_of_week in week_days: #weekday
            if min_weekday_usage == max_weekday_usage: #deterministic
                usage = min_weekday_usage
            else: 
                usage = np.around(np.random.triangular(min_weekday_usage,
                                                   mode_weekday_usage,
                                                   max_weekday_usage,
                                                   size=None))
        else: #weekend
            if min_weekend_usage == max_weekend_usage: #deterministic
                usage = min_weekend_usage
            else:
                usage = np.around(np.random.triangular(min_weekend_usage,
                                                   mode_weekend_usage,
                                                   max_weekend_usage,
                                                   size=None))
        return usage

    # calculate the inventory level at the end of the day and determine if a stock out occurs
    def calc_inventory_level(inventory_level, usage_today,
                             order_arrival):
        c = inventory_level + order_arrival - usage_today
        if usage_today <= inventory_level + order_arrival:  # no stock outs
            fill_rate.append(1)  # meet all demand for the day

        else:
            # a stock out occurred
            stockouts_occur.append(1)
            date_of_stockout.append(clock)
            fill_rate.append((inventory_level + order_arrival) / usage_today)
            if c < 0:
                c = 0
        return c

    # do any orders arrive today?
    def order_arrival_today(_clock):
        order_arrived = 0
        for date in range(len(delivery_schedule)):
            if _clock == delivery_schedule[date]:
                order_arrived = order_arrived + orderq_schedule[date]
                remove_indices.append(date)
        return order_arrived

    def trim_schedules(_remove_indices, _delivery_schedule, _order_q_schedule):
        # now remove events from schedules (orders and deliveries)
        if len(_remove_indices) > 0:
            _delivery_schedule = [i for j, i in enumerate(_delivery_schedule) if j not in _remove_indices]
            _order_q_schedule = [i for j, i in enumerate(_order_q_schedule) if j not in _remove_indices]
        _remove_indices = []
        return _delivery_schedule, _order_q_schedule, _remove_indices

    # assume orders arrive in the morning before surgeries start, optimistic
    def review(_inventory_level, _order_arrival):
        # inventory level today
        count = _inventory_level + _order_arrival
        # place an order, update stats
        if count <= min_level:
            order_is_placed.append(1)
            date_of_order.append(clock)
            if min_lt == max_lt: #deterministic
                order_lt = min_lt
            else: #not deterministic
                order_lt = np.around( np.random.triangular(min_lt, mode_lt, max_lt, size=None))
            
            order_lt = order_lt.astype(int)
            # calculate order date excluding weekends
            date_delivery = rrule(DAILY, byweekday=(MO, TU, WE, TH, FR), dtstart=clock)[order_lt]
            date_delivery = date_delivery.date()

            # calculate order volume based on order position
            order_quantity = max_level - inventory_level - sum(orderq_schedule) #calculate order quantity
            order_quantity = np.ceil(order_quantity/unit_of_order)*unit_of_order #ensure an order is placed in the units required 
            delivery_schedule.append(date_delivery) #add delivery date to schedule
            orderq_schedule.append(order_quantity) # add order quantity to schedule    

    def t_mean_confidence_interval(dat, alpha):
        a = 1.0 * np.array(dat)
        n = len(a)
        m, se = np.mean(a), stats.sem(a)
        h = stats.t.ppf(1 - alpha / 2, n - 1) * se
        return m, m - h, m + h

    def t_mean_error(dat, alpha):
        b = 1.0 * np.array(dat)
        c = len(b)
        se_ub = stats.sem(b)
        h_ub = stats.t.ppf(1 - alpha / 2, c - 1) * se_ub
        return h_ub

    def inv_position(inv_level, _order_q_schedule):
        pos_n = inv_level + sum(_order_q_schedule)
        return pos_n

    for reps in range(0, num_reps, 1):

        # initialize values
        start_date = datetime.date(1994, 12, 19)  # arbirtarily choose a day to start at
        clock = start_date  # assign the day to the start date
        Days = 0  # number of days the sim has run for
        inventory_level = current_inventory_level  # set starting inventory level

        # create space to store stats for each rep
        items_in_inventory = []  # volume of items being held at start of day
        stockouts_occur = []  # num of stockouts
        date_of_stockout = []  # date of stockout
        order_is_placed = []  # num of orders
        date_of_order = []  # date order is placed
        order_vol = []  # volume of each order
        fill_rate = []  # record fill rate per period
        inventory_position_rep = []  # record inventory position

        # schedule of order volumes and dates of delivery arrival
        delivery_schedule = []
        orderq_schedule = []
        remove_indices = []

        while (Days < RunLength):
            day_of_week = clock.weekday()

            if Days % frequency == 0 and day_of_week in week_days:  # conduct a review every 'frequency' mornings that are on weekdays
                order_arrival = order_arrival_today(clock)  # revieve orders
                items_in_inventory.append(inventory_level + order_arrival)
                if order_arrival > 0:
                    order_vol.append(order_arrival)
                review(inventory_level, order_arrival)  # review inventory level
                delivery_schedule, orderq_schedule, remove_indices = trim_schedules(remove_indices, delivery_schedule,
                                                                                    orderq_schedule)
                usage_today = usage(day_of_week)  # create demand for the day
                inventory_level_EoD = calc_inventory_level(inventory_level, usage_today,
                                                           order_arrival)  # calculate the inventory level at the end of the day

            else:  # when not conducting a review
                order_arrival = order_arrival_today(clock)  # check if an order arrives
                items_in_inventory.append(inventory_level + order_arrival)
                if order_arrival > 0:
                    order_vol.append(order_arrival)
                delivery_schedule, orderq_schedule, remove_indices = trim_schedules(remove_indices, delivery_schedule,
                                                                                    orderq_schedule)
                usage_today = usage(day_of_week)
                inventory_level_EoD = calc_inventory_level(inventory_level, usage_today, order_arrival)

            clock = clock + timedelta(days=1)  # progress clock (for date)
            Days = Days + 1  # progress days

            inventory_position = inv_position(inventory_level, orderq_schedule)
            inventory_position_rep.append(inventory_position)
            inventory_level = inventory_level_EoD  # set inventory level

        AllProbStockout.append(np.sum(stockouts_occur)/RunLength)
        AllMeanInvLevel.append(np.mean(items_in_inventory))
        AllMinInvLevel.append(np.min(items_in_inventory))
        AllMaxInvLevel.append(np.max(items_in_inventory))
        # AllNumOrders.append(np.sum(order_is_placed))
        AllFillRate.append(np.mean(fill_rate))
        AllDaysInvLevel.append(items_in_inventory)
        AllInvPosition.append(inventory_position_rep)

    elapsed_time = time.time() - start_time

    print("The expected fill rate and the 95% confidence interval for the given policy is: ",
          t_mean_confidence_interval(AllFillRate, 0.05))
    print("The expected probability of stockout and the 95% confidence interval for the given policy is: ",
          t_mean_confidence_interval(AllProbStockout, 0.05))
    print("\nThe expected daily inventory level and the 95% confidence interval for the given policy is: ",
          t_mean_confidence_interval(AllMeanInvLevel, 0.05))
    print("\nThe expected lowest daily inventory level and the 95% confidence interval for the given policy is: ",
          t_mean_confidence_interval(AllMinInvLevel, 0.05))
    print("\nThe expected highest daily inventory level and the 95% confdence interval for the given policy is:",
          t_mean_confidence_interval(AllMaxInvLevel, 0.05))

    fill_rate_m, fill_rate_l, fill_rate_u = t_mean_confidence_interval(AllFillRate, 0.05)
    prob_stockout_m, prob_stockout_l, prob_stockout_u = t_mean_confidence_interval(AllProbStockout, 0.05)
    inv_lvl_m, inv_lvl_l, inv_lvl_u = t_mean_confidence_interval(AllMeanInvLevel, 0.05)
    min_lvl_m, min_lvl_l, min_lvl_u = t_mean_confidence_interval(AllMinInvLevel, 0.05)
    max_lvl_m, max_lvl_l, max_lvl_u = t_mean_confidence_interval(AllMaxInvLevel, 0.05)


    summary_df = pd.DataFrame({
        "Metric": ["Fill Rate","Probability Stockout", "Inventory Level", "Min Inventory Level", "Max Inventory Level"],
        "Expectation": ["{0:0.3f}".format(x) for x in [fill_rate_m, prob_stockout_m, inv_lvl_m, min_lvl_m, max_lvl_m]],
        "95% CI Lower Bound": ["{0:0.3f}".format(x) for x in [fill_rate_l, prob_stockout_l, inv_lvl_l, min_lvl_l, max_lvl_l]],
        "95% CI Upper Bound": ["{0:0.3f}".format(x) for x in [fill_rate_u, prob_stockout_u, inv_lvl_u, min_lvl_u, max_lvl_u]]
    })
    print(summary_df)

    # sample path building
    # put all inventory levels for each day together
    Daily = []
    Daily_posn = []
    for inv in range(0, RunLength, 1):
        day_inv = []
        day_inv_posn = []
        for day in range(0, num_reps, 1):
            day_inv.append(AllDaysInvLevel[day][inv])
            day_inv_posn.append(AllInvPosition[day][inv])
        Daily.append(day_inv)
        Daily_posn.append(day_inv_posn)

    samplePath_Values_Mean = []
    samplePath_Values_error = []
    samplePath_Values_5 = []
    samplePath_Values_95 = []

    samplePosn_mean = []
    samplePosn_error = []
    samplePosn_5 = []
    samplePosn_95 = []

    for i in range(0, len(Daily), 1):
        samplePath_Values_Mean.append(np.mean(Daily[i]))
        samplePath_Values_error.append(t_mean_error(Daily[i], 0.05))
        samplePath_Values_5.append(np.percentile(Daily[i], 5))
        samplePath_Values_95.append(np.percentile(Daily[i], 95))
        samplePosn_mean.append(np.mean(Daily_posn[i]))
        samplePosn_error.append(t_mean_error(Daily_posn[i], 0.05))
        samplePosn_5.append(np.percentile(Daily_posn[i], 5))
        samplePosn_95.append(np.percentile(Daily_posn[i], 95))
    # build x array
    x = []
    for date in range(0, RunLength, 1):
        x.append(date)

        # put together plot
    fig = plt.figure(figsize=(20, 10))

    yerr = samplePath_Values_error
    yerr2 = samplePosn_error
    text = "Estimated Inventory Level Sample Path for Review every {} Days and ({},{}) Inventory Control Policy".format(
        frequency, min_level, max_level)

    print("Simulation time in seconds: ", elapsed_time)

    trace0 = go.Scatter(
        x=x,
        y=samplePath_Values_Mean,
        error_y=dict(type='data', array=yerr, visible=True, color='#85144B'),
        mode='lines+markers',
        name='Average Inventory Level')
    trace1 = go.Scatter(x=x,
                        y=samplePath_Values_5,
                        mode='lines',
                        name='5th Percentile',
                        line=dict(dash='dash'))
    trace2 = go.Scatter(x=x,
                        y=samplePath_Values_95,
                        mode='lines',
                        name='95th Percentile',
                        line=dict(dash='dash'))
    trace3 = go.Scatter(x=x,
                        y=[max_level] * RunLength,
                        mode='lines',
                        name='Order Up To Point',
                        line=dict(color='rgb(55, 128, 191)')
                        )
    trace4 = go.Scatter(x=x,
                        y=[min_level] * RunLength,
                        mode='lines',
                        name='Reorder Point',
                        line=dict(color='rgb(179,166 ,253 )'))

    data = [trace0, trace1, trace2, trace3, trace4]

    layout = go.Layout(
        title=None,
        hovermode='closest',
        xaxis=dict(
            title='Days'
        ),
        yaxis=dict(
            title='Beginning of Day Inventory Level',
        ),
        height=700
    )

    fig = {
        'data': data,
        'layout': layout,
    }
    if offline:
        py.offline.plot(fig, filename='Est_Inv_Level.html')

    return fig, summary_df


if __name__ == "__main__":
    run({}, offline=True)
