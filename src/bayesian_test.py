exec(open('src/cleaning_data.py').read())

import scipy.stats as stats
import matplotlib.pyplot as plt

plt.style.use('ggplot')
font = {'weight': 'bold', 'size': 9}
plt.rc('font', **font)



def get_beta_params(drill_name):
    '''
    Generates parameters for a beta distribution for using the binomial
    data from the passed-in combine drill(alpha=successes, beta=failures).
    ----------
    Parameters
    ----------
    drill_name: str
        A string matching one of the six combine drills' names.
    ----------
    Returns 
    ----------
    A tuple of the alpha, beta
    '''
    return mean[drill_name]+1, n[drill_name] - mean[drill_name]+1



def bayes_AB_plot(drill_name):
    '''
    Prepares a Bayesian AB test between the 40-Yard dash data and the
    passed-in combine drill. Calculates and prints the 95% High density
    Interval for the 40-yard and the passed-in drill data. Then, plots a 
    visualization of the beta distributions to be sampled for the AB test.
    ----------
    Parameters
    ----------
    drill_name: str
        A string matching one of the six combine drills' names.
    ----------
    Returns 
    ----------
    None
    '''
    a_40, b_40 = get_beta_params(drills[0])
    a_2, b_2 = get_beta_params(drill_name)

    dist_40 = stats.beta(a=a_40, b=b_40)
    dist_2 = stats.beta(a=a_2, b=b_2)

    lower_40 = dist_40.ppf(0.025)
    upper_40 = dist_40.ppf(0.975)
    print("{}'s 95% HDI is {:.5f} to {:.5f}".format(short_name[drills[0]], lower_40, upper_40))
    lower_2 = dist_2.ppf(0.025)
    upper_2 = dist_2.ppf(0.975)
    print("{}'s 95% HDI is {:.5f} to {:.5f}\n".format(short_name[drill_name], lower_2, upper_2))

    x = np.arange(0, 1.001, 0.001)
    y_prior = stats.beta(a=1, b=1).pdf(x)
    y_40 = dist_40.pdf(x)
    y_2 = dist_2.pdf(x)
    line = ax.plot(x, y_prior, label='Uniform Prior')
    fill = ax.fill_between(x, 0, y_prior, alpha=0.5, color=line[0].get_c())
    line_40 = ax.plot(x, y_40, label='{} Posterior After {} Top Performers'
                      .format(short_name[drills[0]], n[drills[0]]))
    fill_40 = ax.fill_between(x, 0, y_40, alpha=0.5, color=line_40[0].get_c())
    line_2 = ax.plot(x, y_2, label='{} Posterior After {} Top Performers'
                     .format(short_name[drill_name], n[drill_name]))
    fill_2 = ax.fill_between(x, 0, y_2, alpha=0.5, color=line_2[0].get_c())

    ax.set_xlim(0, 0.3)
    ax.set_ylim(0, 55)
    ax.legend()
    ax.set_title('{} Vs. {}'.format(short_name[drills[0]], short_name[drill_name]))
    ax.set_xlabel('Rate of Drafted in 1st Rd')



def bayes_AB_test(drill_name):
    '''
    Performes a Bayesian AB test between the 40-Yard dash data and the
    passed-in combine drill. Prints the result.
    ----------
    Parameters
    ----------
    drill_name: str
        A string matching one of the six combine drills' names.
    ----------
    Returns 
    ----------
    None
    '''
    a_40, b_40 = get_beta_params(drills[0])
    a_2, b_2 = get_beta_params(drill_name)
    
    sample_40 = np.random.beta(a=a_40, b=b_40, size=10000)
    sample_2 = np.random.beta(a=a_2, b=b_2, size=10000)

    prob = (sample_40 > sample_2).mean() * 100
    print(
        '''
        There is a {:.2f}% probability that top performers in the {} are drafted 
        in the 1st Round at a higher rate than top performers in the {}
        '''.format(prob, short_name[drills[0]], short_name[drill_name]))



def bayes_AB_test_assumed_diff(drill_name, diff):    
    '''
    Performes a Bayesian AB test between the 40-Yard dash data and the
    passed-in combine drill including an assumed difference in sample frequency. 
    Prints the result.
    ----------
    Parameters
    ----------
    drill_name: str
        A string matching one of the six combine drills' names.
    ----------
    Returns 
    ----------
    None
    '''
    a_40, b_40 = get_beta_params(drills[0])
    a_2, b_2 = get_beta_params(drill_name)
    
    sample_40 = np.random.beta(a=a_40, b=b_40, size=10000)
    sample_2 = np.random.beta(a=a_2, b=b_2, size=10000)
    
    prob = (sample_40 > sample_2 + diff).mean() * 100
    print(
        '''
        There is a {:.2f}% probability that top performers in the {} are drafted 
        in the first round at a rate that is {:.1f} percentage points higher than top
        performers in the {}'''
        .format(prob, short_name[drills[0]], (diff * 100), short_name[drill_name]))


# Generate the visualization of the beta distributions used in the AB test.
fig, axs = plt.subplots(2, 3, figsize=(15, 8))
axs_f = axs.flatten()
for i, drill in enumerate(drills[1:]):
    ax = axs_f[i]
    bayes_AB_plot(drill)
axs_f[-1].remove()
fig.tight_layout()
plt.savefig('images/bayes_AB_all.png')


# Run the Bayesian AB test on the drills
for drill in drills[1:]:
    bayes_AB_test(drill)


# Store the max differences calculated in the z-test.
max_diffs = {drills[0]: 0.0,
             drills[1]: 0.067,
             drills[2]: 0.032,
             drills[3]: 0.012,
             drills[4]: 0.023,
             drills[5]: 0.031}
            

# Run the Bayesian AB test using the max assumed differences calculated
# in the z-test
for drill in drills[1:]:
    bayes_AB_test_assumed_diff(drill, max_diffs[drill])
