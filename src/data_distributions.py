exec(open('src/cleaning_data.py').read())

import scipy.stats as stats
import matplotlib.pyplot as plt
import numpy as np

plt.style.use('ggplot')
font = {'weight': 'bold', 'size': 10}
plt.rc('font', **font)


def bootstrap_95_ci(drill_name):
    '''
    Takes the name of a combine drill and uses it's sample to
    bootstrap 10,000 samples and compute the sample mean 95% 
    confidence interval
    ----------
    Parameters
    ----------
    drill_name: str
        A string matching one of the six combine drills' names.
    ----------
    Returns 
    ----------
    A tuple of two floats: the endpoints for the 95% CI.
    '''
    data = joined[joined[drill_name] > 0.1][drill_name]
    bootstrap_sample_means = []
    for _ in range(10000):
        bootstrap = np.random.choice(data, size=len(data), replace=True)
        bootstrap_mean = np.mean(bootstrap)
        bootstrap_sample_means.append(bootstrap_mean)
    left_endpoint = np.percentile(bootstrap_sample_means, 2.5)
    right_endpoint = np.percentile(bootstrap_sample_means, 97.5)
    return left_endpoint, right_endpoint


def fit_plot(drill_name, axes, dist, name):
    '''
    Plots the histogram of a combine drill's data and fits a distribution
    using the MLE method, all on the passed-in axes.
    ----------
    Parameters
    ----------
    drill_name: str
        A string matching one of the six combine drills' names.
    axes: matplotlib axes subplot
        A matplotlib axes subplot for the histogram and fit distribution
        to be plotted on.
    dist: scipy.stats distribution (ex: stats.norm)
        A distribution to be used as a model to create a fit for the data.
    name: str
        A string to be used as the plot title
    ----------
    Returns 
    ----------
    None
    '''    
    data = joined[joined[drill_name] > 0.1][drill_name]
    n = len(data)
    mu = np.mean(data)
    s = np.std(data, ddof=1)
    x = np.linspace(mu - 4* s, mu + 4*s, 1000)   
    hist = axes.hist(data, bins=50, color='b', density=True, 
        label='original data', alpha=0.5, zorder=5)            
    fit_mu, fit_s = dist.fit(data)
    cont_pdf = axes.plot(x, dist.pdf(x, fit_mu, fit_s),
            color='r', label='fit', zorder=10)
    axes.set_title(name)


def quartiles(df, category, q_divs):
    '''
    Computes the four quartile DataFrames from the passed-in DF.
    ----------
    Parameters
    ----------
    df: Pandas DataFrame
        A DataFrame to split into 4 quartiles.
    category: str
        A string containing the column name that you wish to use to split
        the DataFrame into 4 quartiles
    q_divs: list
        A list of three floats which are the 25th percentile, Median, and 
        75th percentile of the column's data, which will be used to split
        the Dataframe 
    ----------
    Returns 
    ----------
    A tuple of 4 DataFrames
    ''' 
    w_q1 = df[df[category] <= q_divs[0]]
    w_q2 = df[(df[category] > q_divs[0]) & (df[category] <= q_divs[1])]
    w_q3 = df[(df[category] > q_divs[1]) & (df[category] <= q_divs[2])]
    w_q4 = df[df[category] > q_divs[2]]
    return w_q1, w_q2, w_q3, w_q4


def combined_norm_fits(drill_name, axes, name):
    '''
    Splits the combine drill's data into four DataFrames, the four quartiles
    of the performing players' weights. Next, it fits a normal distribution to
    each quartile's data. Finally, it averages the four fits for each point in
    the x array and plots the combined fit over a histogram of the drill's data.
    ----------
    Parameters
    ----------
    drill_name: str
        A string matching one of the six combine drills' names.
    axes: matplotlib axes subplot
        A matplotlib axes subplot for the histogram and fit distribution
        to be plotted on.
    name: str
        A string to be used as the plot title
    ----------
    Returns 
    ----------
    None
    '''
    temp = joined[joined[drill_name] > 0.1]
    q_divs = [temp['Weight (lbs)'].describe()[j] for j in [4, 5, 6]]
    w_qs = quartiles(temp, 'Weight (lbs)', q_divs)
    q = ['q1', 'q2', 'q3', 'q4']
    mean, std = temp[drill_name].mean(), temp[drill_name].std()
    mu = {}
    s = {}
    for i, w in enumerate(w_qs):
        data = w[w[drill_name] > 0.1][drill_name]
        mu[q[i]], s[q[i]] = stats.norm.fit(data)
    x = np.linspace(mean - 4* std, mean + 4*std, 1000)
    y = (stats.norm.pdf(x, mu[q[0]], s[q[0]]) + stats.norm.pdf(x, mu[q[1]], s[q[1]]) 
         + stats.norm.pdf(x, mu[q[2]], s[q[2]]) + stats.norm.pdf(x, mu[q[3]], s[q[3]]))/4
    hist = axes.hist(temp[drill_name], bins=50, color='b', density=True, 
        label='original data', alpha=0.5, zorder=5)
    cont_pdf = axes.plot(x, y, color='r', label='fit', zorder=10)
    axes.set_title(name)


def plot_hist(drill_name, axes):
    '''
    Plots the data from the combine drill as a histogram on the 
    passed-in axes.
    ----------
    Parameters
    ----------
    drill_name: str
        A string matching one of the six combine drills' names.
    axes: matplotlib axes subplot
        A matplotlib axes subplot for the histogram and fit distribution
        to be plotted on.
    ----------
    Returns 
    ----------
    None
    '''    
    data = joined[joined[drill_name] > 0.1][drill_name]
    hist = axes.hist(data, bins=50, color='b', alpha=0.5, label='original data')
    n, mu, s= len(data), np.mean(data), np.std(data, ddof=1)
    title = axes.set_title(label=(drill_name + '\n n={}, '.format(n) + 
            r'$\bar X$={:2.2f}, s= {:2.2f}'.format(mu, s)))


# Plot the data from each drill as a histogram on it's own subplot.
fig, axs = plt.subplots(2, 3, figsize=(15,8))
axs_f = axs.flatten()
for ind, ax in enumerate(axs_f):
    plot_hist(drills[ind], ax)
fig.tight_layout()
plt.savefig('images/drill_data_dist.png')


# Bootstrapping 10000 samples for each drill and calculating 95% CI
for drill in drills:
    lower, upper = bootstrap_95_ci(drill)
    print('Based on 10,000 bootstrapped samples, the 95% CI for the {} is [{:2.2f}, {:2.2f}]'
          .format(short_name[drill], lower, upper))


# Plotting the three drills which have skewed data as a histogram on a subpllot beside
# the weight of the participants as a histogram, beside a scatter plot highliting any
# correlation between the drill data and the player's weights. Also, plots a fit line 
# to the scatter plot data using the method of least squares.
fig, axs = plt.subplots(3, 3, figsize=(15,10))
index = [0, 4, 5]
for i in [0, 1, 2]:
    data = joined[['Weight (lbs)', drills[index[i]]]].dropna()
    array = data.to_numpy()
    m, b = np.polyfit(array[:,0], array[:,1], 1)
    forty = data.hist(drills[index[i]], bins=50 ,color='b', 
                    ax=axs[i,0], label=drills[index[i]], alpha=0.5)
    w = data.hist('Weight (lbs)', bins=50, color='r', 
                    ax=axs[i,1], label='Weight (lbs)', alpha=0.5)
    fit = axs[i, 2].plot(array[:,0], m*array[:,0]+b)
    scat = joined.plot.scatter('Weight (lbs)', drills[index[i]], alpha=0.75, 
                    color='g', ax=axs[i,2], title= drills[index[i]] + ' vs Weight (lbs)')
fig.tight_layout()
plt.savefig('images/skewed_drills.png')


# Creating a plot with a normal distribution fit for each weight quartile of the
# 40-yard dash participants to highlight the location of each weight class's 
# 40-yard dash times. 
fig, ax = plt.subplots()
x = np.linspace(4, 6.5, 1000)
temp = joined[joined[drills[0]] > 0.1]
q_divs = [temp['Weight (lbs)'].describe()[j] for j in [4, 5, 6]]
w_qs = quartiles(temp, 'Weight (lbs)', q_divs)
q = ['q1', 'q2', 'q3', 'q4']
mu = {}
s = {}
for i, w in enumerate(w_qs):
    data = w[w[drills[0]] > 0.1][drills[0]]
    mu[q[i]], s[q[i]] = stats.norm.fit(data)
    cont_pdf = ax.plot(x, stats.norm.pdf(x, mu[q[i]], s[q[i]]), label=q[i], zorder=10)
plot = ax.set_title('40 Yard Dash: Fit Normal Distributions\n by Weight Quartiles')
leg = ax.legend()
plt.savefig('images/fits_by_wq.png')


# Creating a plot comparing the 40-yard dash data with three different distribution
# fits: Normal, Gumbel, and average of the four quartile's fit distributions.
fig, axs = plt.subplots(1,3, figsize=(18,4))
ax = axs.flatten()
fit_plot(drills[0], ax[0], stats.norm, '40 Yard Dash: Normal Fit')
fit_plot(drills[0], ax[1], stats.gumbel_r, '40 Yard Dash: Gumbel Fit')
combined_norm_fits(drills[0], ax[2], '40 Yard Dash: Avg of Weight Quartile Fits')
plt.savefig('images/fit_comparison.png')


# Generate and Save the Drills Data Distribution Fits as image (using the average fit method)
fig, axs = plt.subplots(2, 3, figsize=(15,8))
axs_f = axs.flatten()
for ind, ax in enumerate(axs_f):
    data = joined[joined[drills[ind]] > 0.1][drills[ind]]
    n, mu, s= len(data), np.mean(data), np.std(data, ddof=1)
    title = (drills[ind] + '\n n={}, '.format(n) + 
            r'$\bar X$={:2.2f}, s= {:2.2f}'.format(mu, s))
    combined_norm_fits(drills[ind], ax, title)
fig.tight_layout()
plt.savefig('images/drill_data_dist_fits.png')
