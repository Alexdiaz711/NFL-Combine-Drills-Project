exec(open('src/cleaning_data.py').read())

import scipy.stats as stats
import matplotlib.pyplot as plt

plt.style.use('ggplot')
font = {'weight': 'bold', 'size': 8}
plt.rc('font', **font)


def two_sample_z(drill_name, assumed_diff):
    '''
    Performes a two-sampled z-test between the 40-Yard dash data and the
    passed-in combine drill. Then, plots a visualization of the z-test.
    ----------
    Parameters
    ----------
    drill_name: str
        A string matching one of the six combine drills' names.
    assumed_diff: float
        A float representing the assumed difference in sample frequency to be
        used as the mean/mode of the null hypothesis distribution.
    ----------
    Returns 
    ----------
    None
    '''
    p40, n40 = p[drills[0]], n[drills[0]]
    p2, n2 = p[drill_name], n[drill_name]
    p_shared = (p40*n40 + p2*n2)/(n40 + n2)
    s_shared = np.sqrt((n40 +n2)*p_shared*(1-p_shared)/(n40*n2))
    dist_null = stats.norm(assumed_diff, s_shared)
    sample_diff = p40 - p2
    p_value = 1 - dist_null.cdf(sample_diff)
    x = np.linspace(0-5*s_shared, 0+10*s_shared, 1000)
    plot = ax.plot(x, dist_null.pdf(x), label='$H_0$')
    fill = ax.fill_between(x, dist_null.pdf(x), 
                where=(x >= sample_diff),color="blue", label='p-value region')
    line = ax.axvline(sample_diff, color='b', alpha = 0.5, ls='--')
    legend = ax.legend()
    title = ax.set_title("Distribution of Difference in Sample Frequencies \n {} vs {}, p-value:{:0.2}"
                .format(short_name[drills[0]], short_name[drill_name], p_value))


def max_sample_diff_z(drill_name, alpha):
    '''
    A function to maximize assumed difference in sample frequency while 
    maintaining null-rejection at the passed-in alpha. 
    ----------
    Parameters
    ----------
    drill_name: str
        A string matching one of the six combine drills' names.
    alpha: float
        A float representing the maximum threshold for the p-value where
        the null hypothesis can be rejected.
    ----------
    Returns 
    ----------
    A float: the maximum assumed difference in sample frequency to use for the 
    null hypothesis and still maintain null-rejection.
    '''
    p40, n40 = p[drills[0]], n[drills[0]]
    p2, n2 = p[drill_name], n[drill_name]
    p_shared = (p40*n40 + p2*n2)/(n40 + n2)
    s_shared = np.sqrt((n40 +n2)*p_shared*(1-p_shared)/(n40*n2))
    sample_diff = p40 - p2
    max_diff = 0.0
    for i in np.linspace(0.000, 0.200, 201):        
        dist_comp = stats.norm(i, s_shared)
        p_value_comp = 1 - dist_comp.cdf(sample_diff)
        if p_value_comp <= alpha:
            p_value = p_value_comp
            dist = dist_comp
            max_diff = i
        else:
            break
    return max_diff


# Run two-sampled z-test between 40yd dash and each other test and save
# all plots on the same figure
fig, axs = plt.subplots(2, 3, figsize=(15,8))
axs_f = axs.flatten()
for i, x in enumerate(drills[1:]):
    ax = axs_f[i]
    two_sample_z(x, 0.0)
axs_f[-1].remove()
fig.tight_layout()
plt.savefig('images/z_test_all.png')

# Find out what the maximum assumed difference in sample frequency
# can be while still maintaining null-rejection at alpha=0.01
fig, axs = plt.subplots(2, 3, figsize=(15,8))
axs_f = axs.flatten()
for i, x in enumerate(drills[1:]):
    ax = axs_f[i]
    diff = max_sample_diff_z(x, 0.01)
    two_sample_z(x, diff)
    print('Max Diff for {} is {:2.4f}'.format(x, diff))
axs_f[-1].remove()
fig.tight_layout()
plt.savefig('images/z_test_adjusted_all.png')

