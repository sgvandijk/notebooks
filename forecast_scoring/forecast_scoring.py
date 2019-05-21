import matplotlib.pyplot as plt
from matplotlib import animation
from IPython.display import HTML
import random
import numpy as np
from itertools import groupby
from collections import OrderedDict

def calibration_example(
    forecaster, 
    sort=False, 
    calibration_line=False, 
    calibration_score=False,
    resolution_line=False,
    resolution_score=False,
    skill_area=False,
    skill_score=False,
):
    buckets_green_ratios = np.arange(0.0, 1.1, 0.1)
    n_draws = 1600
    n_points_per_row = 12 if forecaster=="5050" else 10 if "confident" in forecaster else 4

    def predict(bucket):
        if forecaster == "calibrated":
            return buckets_green_ratios[bucket]
        elif forecaster == "random":
            return random.randint(0, 10) / 10
        elif forecaster == "5050":
            return 0.5
        elif forecaster == "inverse":
            return 1.0 - buckets_green_ratios[bucket]
        elif forecaster == "confident":
            return 1 if bucket > 5 else 0
        elif forecaster == "inv_confident":
            return 1 if bucket < 5 else 0
        

    draws = {"predictions": [], "outcomes": []}
    for i in range(n_draws):
        bucket = random.randint(0, 10)
        pred = predict(bucket)
        outc = random.random() < buckets_green_ratios[bucket]
        draws['predictions'].append(pred)
        draws['outcomes'].append(outc)
        
    # plt.grid(axis='x')
    cmap = plt.cm.Set1
        
    def draws_to_points():
        dist_between_points = .09 / n_points_per_row
        x_start = - 0.045 + dist_between_points / 2
        cur_pos = np.zeros((len(buckets_green_ratios), 2))
        
        xs = []
        ys = []
        cs = []
        
        draws_ = zip(draws["predictions"], draws["outcomes"])
        if sort:
            draws_ = sorted(draws_, key=lambda d: d[1], reverse=True)
            
        for pred, outc in draws_:
            bucket = int(round(pred * 10)) - 1
            y_idx, x_idx = cur_pos[bucket]
            x = pred + x_start + x_idx * dist_between_points
            y = y_idx * dist_between_points
            
            jitter = 0.002
            x += jitter * (random.random() * 2 - 1)
            y += jitter * (random.random() * 2 - 1)
            
            xs.append(x)
            ys.append(y)
            cs.append(cmap(2 if outc else 0))
            
            x_idx += 1
            if x_idx >= n_points_per_row:
                y_idx += 1
                x_idx = 0
            cur_pos[bucket] = [y_idx, x_idx]
        return {"x": xs, "y": ys, "c": cs}
    
    def determine_rates():
        draws_ = zip(draws["predictions"], draws["outcomes"])
        draws_ = sorted(draws_, key=lambda d: d[0], reverse=True)
        grouped_draws = groupby(draws_, key=lambda d: d[0])
        
        rates = OrderedDict()
        for g, d in grouped_draws:
            d_ = [i[1] for i in d]
            rates[g] = (len(d_), sum(d_) / len(d_))
        return rates
    
    def plot_calibration_line(rates):
        plt.plot([0, 1], [0, 1], lw=3, c=cmap(4), zorder=4)
        vs = [v[1] for v in rates.values()]
        plt.plot(rates.keys(), vs, c=cmap(1))
        plt.scatter(rates.keys(), vs, c=cmap(1), s=200, zorder=5)
        plt.vlines(rates.keys(), rates.keys(), vs)
        
    def determine_base_rate():
        return sum(draws["outcomes"]) / len(draws["outcomes"])
    
    def plot_resolution_line(rates):
        base_rate = determine_base_rate()
        plt.plot([0, 1], [base_rate, base_rate], lw=3, c=cmap(4), zorder=4)
        vs = [v[1] for v in rates.values()]
        plt.plot(rates.keys(), vs, c=cmap(1))
        plt.scatter(rates.keys(), vs, c=cmap(1), s=200, zorder=5)
        plt.vlines(rates.keys(), base_rate, vs)
    
    def determine_calibration_score(rates):
        N = 0
        cal = 0.0
        for f, n_o in rates.items():
            N += n_o[0]
            cal += n_o[0] * np.square(f - n_o[1])
        return cal / N
    
    def determine_resolution_score(rates):
        base_rate = determine_base_rate()
        N = 0
        res = 0.0
        for f, n_o in rates.items():
            N += n_o[0]
            res += n_o[0] * np.square(base_rate - n_o[1])
        return res / N

    def determine_uncertainty():
        base_rate = determine_base_rate()
        return base_rate * (1 - base_rate)

    # First set up the figure, the axis, and the plot element we want to animate
    if calibration_score:
        figsize = 4
    else:
        figsize = 8
        
    fig, ax = plt.subplots(figsize=(figsize, figsize))
    rates = determine_rates()
    
    if skill_area:
        base_rate = determine_base_rate()
        plt.fill_between([0, base_rate], [.5 * base_rate, base_rate], color=cmap(2), alpha=.5)
        plt.fill_between([base_rate, 1], [base_rate, base_rate + .5 * (1 - base_rate)], [1, 1], color=cmap(2), alpha=.5)
        
    if calibration_score:
        cal = determine_calibration_score(rates)
        plt.title(f"CAL: {cal:.4f}")
    
    if resolution_score:
        res = determine_resolution_score(rates)
        plt.title(f"RES: {res:.4f}")
    
    if skill_score:
        cal = determine_calibration_score(rates)
        res = determine_resolution_score(rates)
        unc = determine_uncertainty()
        ss = (res - cal) / unc
        
        plt.title(f"CAL: {cal:.4f}, RES: {res:.4f}, UNC: {unc:.4f}, SKILL: {ss:.4f}")
        
    for b in np.arange(-0.05, 1.15, 0.1):
        ax.vlines(b, -0.01, 1, 'grey')
    
    ax.scatter(**draws_to_points(), alpha=0.1 if calibration_line or resolution_line else 1.0)
    if calibration_line:
        plot_calibration_line(rates)
    
    if resolution_line:
        plot_resolution_line(rates);
        
    ax.set_aspect('equal')
    plt.xlim((-0.1, 1.1))
    plt.xticks(buckets_green_ratios)
    plt.xlabel("Prediction")
    