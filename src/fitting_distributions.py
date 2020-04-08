exec(open('src/cleaning_data.py').read())

import scipy.stats as stats
import matplotlib.pyplot as plt

plt.style.use('ggplot')
font = {'weight': 'bold', 'size': 10}
plt.rc('font', **font)

def bootstrap_95_ci(drill_name):
    data = joined[joined[drill_name] > 0.1][drill_name]
    bootstrap_sample_means = []
    for i in range(10000):
        bootstrap = np.random.choice(data, size=len(data), replace=True)
        bootstrap_mean = np.mean(bootstrap)
        bootstrap_sample_means.append(bootstrap_mean)
    left_endpoint = np.percentile(bootstrap_sample_means, 2.5)
    right_endpoint = np.percentile(bootstrap_sample_means, 97.5)
    return left_endpoint, right_endpoint

def fit_drill_data(drill_name, ax, ci, skew=None):
    data = joined[joined[drill_name] > 0.1][drill_name]
    n = len(data)
    mu = np.mean(data)
    s = np.std(data, ddof=1)
    x = np.linspace(mu - 4* s, mu + 4*s, 100000)   
    hist = ax.hist(data, bins=50, color='b', density=True, 
        label='original data', alpha=0.5, zorder=5)
    if skew == 'R':        
        fit_mu, fit_s = stats.gumbel_r.fit(data)
        cont_pdf = ax.plot(x, stats.gumbel_r.pdf(x, fit_mu, fit_s),
            color='r', label='fit', zorder=10)
        title = ax.set_title(label=(drill_name + '\n n={}, '.format(n) + 
            r'$\bar X$={:2.2f}, s= {:2.2f}'.format(mu, s) + 
            '\n ~ Gumbel({:2.2f}, {:2.2f})'.format(fit_mu, fit_s)))
        ci_plot = ax.fill_between(x, stats.gumbel_r.pdf(x, fit_mu, fit_s), 0, 
            where=((x >= ci[0]) & (x <= ci[1])), color="g", 
            label=r'$\bar X$ 95% CI', zorder=15)    
    elif skew == 'L':
        fit_mu, fit_s = stats.gumbel_l.fit(data)
        cont_pdf = ax.plot(x, stats.gumbel_l.pdf(x, fit_mu, fit_s), 
            color='r', label='fit', zorder=10)
        title = ax.set_title(label=(drill_name + '\n n={}, '.format(n) + 
            r'$\bar X$={:2.2f}, s= {:2.2f}'.format(mu, s) + 
            '\n ~ Gumbel({:2.2f}, {:2.2f})'.format(fit_mu, fit_s)))
        ci_plot = ax.fill_between(x, stats.gumbel_l.pdf(x, fit_mu, fit_s), 0, 
            where=((x >= ci[0]) & (x <= ci[1])), color="g", 
            label=r'$\bar X$ 95% CI', zorder=15)
    else:
        fit_mu, fit_s = stats.norm.fit(data)
        cont_pdf = ax.plot(x, stats.norm.pdf(x, fit_mu, fit_s), 
            color='r', label='fit', zorder=10)
        title = ax.set_title(label=(drill_name + '\n n={}, '.format(n) + 
            r'$\bar X$={:2.2f}, s= {:2.2f}'.format(mu, s) + 
            '\n ~ Normal({:2.2f}, {:2.2f})'.format(fit_mu, fit_s)))
        ci_plot = ax.fill_between(x, stats.norm.pdf(x, fit_mu, fit_s), 0, 
            where=((x >= ci[0]) & (x <= ci[1])), color="g", 
            label=r'$\bar X$ 95% CI', zorder=15)

# Bootstrapping 10000 samples for each drill
#  and calculating 95% CI
cis = [bootstrap_95_ci(x) for x in drills]

# Recording skew of each distribution in a dictionary
skew = {'40 Yard Dash (sec)': 'R',
    'Bench Press (reps @ 225 lbs)': None,
    'Vertical Leap (in)': None,
    'Broad Jump (in)': None,
    'Shuttle Drill (sec)': 'R',
    '3 Cone Drill (sec)': 'R'}

# Generate and Save the Drills Data Distribution Fits as image
fig, axs = plt.subplots(2, 3, figsize=(15,8))
axs_f = axs.flatten()
for ind, ax in enumerate(axs_f):
    ci = cis[ind]
    fit_drill_data(drills[ind], ax, ci, skew[drills[ind]])
    if ind == 2:
        ax.legend()
fig.tight_layout()
plt.savefig('images/drill_data_dist_fits.png')