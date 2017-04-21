import numpy
import matplotlib.pyplot as pyplot
import scipy.optimize
import scipy.stats
import matplotlib.ticker as ticker
import matplotlib


id_fac = 1.5
mean_points = 100

(T, V, I, ti, ti_T, temps) = numpy.loadtxt('semi-t-ramp-80-180-v-1.1.txt')
ti_T = numpy.trim_zeros(ti_T, 'b')[1:]
temps = numpy.trim_zeros(temps, 'b')
V = numpy.abs(V)

av_V = numpy.zeros(21)
av_I = numpy.zeros(21)
I_err = numpy.zeros(21)
log_I_err = numpy.zeros(21)
av_T = numpy.zeros(21)
T_err = numpy.zeros(21)
for i in range(600, 12601, 600):
    av_V[i/600 - 1] = numpy.abs(numpy.average(V[i - mean_points:i]))
    av_I[i/600 - 1] = numpy.average(I[i - mean_points:i])
    I_err[i/600 - 1] = numpy.max(numpy.max(I[i - mean_points:i])-numpy.mean(I[i - mean_points:i]), numpy.mean(I[i - mean_points:i]) - numpy.min(I[i - mean_points:i]))
    av_T[i / 600 - 1] = numpy.average(T[i - mean_points:i])
    T_err[i / 600 - 1] = numpy.max(numpy.max(T[i - mean_points:i])-numpy.mean(T[i - mean_points:i]), numpy.mean(T[i - mean_points:i]) - numpy.min(T[i - mean_points:i]))


xval = 1/av_T
yval = numpy.log(av_I)
yerr = yval * I_err/av_I
xerr = xval * T_err/av_T

print yerr
print I_err/av_I





# Define the functional form of the model: vals is a numpy array holding the parameter values
def model_funct(x, vals):
    return vals[0] + vals[1]*x


# In[274]:

# define initial values for fitting parameters and calculate degrees of freedom
initial = numpy.array([1e-5, 6e-8]) # Initial guess for fit parameters
deg_freedom = xval.size - initial.size # Make sure you understand why!
print('DoF = {}'.format(deg_freedom))


# In[275]:

# A function that calculates chi-squared for the model function (model_funct, defined above), given a set of parameter
# values and data set with errors
def chisq(modelparams, x_data, y_data, y_err):
    chisqval=0
    for i in range(len(xval)):
        chisqval += ((y_data[i] - model_funct(x_data[i], modelparams))/y_err[i])**2
    return chisqval


# In[276]:

# Produce a fit using the scipy optimize sub-module:
# chisq is the function to be minimised - defined above, in this case giving chi-squared
# initial is a numpy array containing the initial 'guessed' values of the parameters - defined above
# args are additional arguments to pass to the chisq function after the array of parameters - in this case the data.
#
# There are many additional options that can be passed to the minimize function; see the scipy documentation - these are
# not required for the simple case here, but may be for more complex data. You will learn about how several of them work
# during in your Computational Physics course.
fit = scipy.optimize.minimize(chisq, initial, args=(xval, yval, yerr))

# Termination output message is fit.message - did the minimisation complete successfully?
print(fit.message)

# Resulting best fit parameter array is output as fit.x
a_soln = fit.x[0]
b_soln = fit.x[1]

print('best fit a = {} a_units?'.format(a_soln))
print('best fit b = {} b_units?'.format(b_soln))

# minimized value for chisq function is fit.fun
print('minimised chi-squared = {}'.format(fit.fun))


# In[277]:

# Calculate the minimized value of chi-squared again as a demonstration; this time using the chisq function directly,
# and best fit parameter values. Result should be the same as above...
chisq_min = chisq([a_soln, b_soln], xval, yval, yerr)
print('chi^2_min = {}'.format(chisq_min))


# In[278]:

# Calculate the reduced chi-squared value from minimized chi-squared
chisq_reduced = chisq_min/deg_freedom
print('reduced chi^2 = {}'.format(chisq_reduced))


# In[279]:

# Calculate the 'P-value', as described in Skills 1 & 2.
# 'scipy.stats.chi2.sf' is the Python equivalent of 'chidist' in Excel.
P = scipy.stats.chi2.sf(chisq_min, deg_freedom)
print('$P(chi^2_min, DoF)$ = {}'.format(P))


# In[289]:

# Plot the data and best fit - data has error-bars and no joining lines, fit is shown by a line.
fig = pyplot.figure(figsize=(6,5))
frame1=fig.add_axes((.1,.3,.8,.6))
pyplot.errorbar(xval, numpy.exp(yval), yerr=numpy.exp(yerr), xerr=xerr, marker='o', linestyle='None', markersize=4)
pyplot.semilogy()
# Axis labels


pyplot.ylabel('Current')

# Generate best fit line using model function and best fit parameters, and add to plot
fit_line=model_funct(xval, [a_soln, b_soln])
pyplot.plot(xval, numpy.exp(fit_line), 'r')

# Set suitable axis limits: you will probably need to change these...
pyplot.axis([0.005, 0.013, 1.5e-3,1e-2])
#pyplot.xlim(0.005, 0.013)
#pyplot.ylim(0.4, 1.3)
frame1.set_xticklabels([])
from matplotlib.ticker import MaxNLocator
pyplot.gca().yaxis.set_major_locator(MaxNLocator(prune='lower'))



# What about plotting the (normalised) residuals?
diff = (yval - fit_line) / yerr

frame2=fig.add_axes((.1,.1,.8,.2))

pyplot.ylabel('Normalised \n Residuals')
#pyplot.ylim(-3, 3)
#pyplot.xlim(0.03, 0.1)
ax = pyplot.gca()
ax.yaxis.set_major_locator(ticker.MultipleLocator(4))
pyplot.plot(xval, diff, marker='o', linestyle='None', markersize=4)
pyplot.xlabel('Inverse Temperature')


pyplot.grid()


# In[295]:

# Generate data for 2D plots of the chi squared landscape.
# Note that this is not a very computationally efficient approach, so unsuited to more complex problems.

# Axis ranges for 2D plot - adjust to suit
a_low, a_high = a_soln-0.017, a_soln+0.017
b_low, b_high = b_soln-2.5, b_soln+2.5

# Generate grid and data
da = (a_high - a_low)/1000.0
db = (b_high - b_low)/1000.0
a_axis = numpy.arange(a_low, a_high, da)
b_axis = numpy.arange(b_low, b_high, db)
plot_data = numpy.zeros((len(a_axis), len(b_axis)))
for i, bval in enumerate(b_axis):
    for j, aval in enumerate(a_axis):
        plot_data[i][j] = chisq([aval, bval], xval, yval, yerr)


# In[296]:

# As an example, produce a colour plot of chi-squared landscape.

pyplot.figure(figsize=(8,12))
im = pyplot.imshow(plot_data, extent = (a_low, a_high, b_low, b_high), origin = 'lower',
                   cmap=matplotlib.cm.copper, aspect='auto')
pyplot.ylim(b_low, b_high)
pyplot.xlim(a_low, a_high)

# Axis labels
pyplot.ylabel('b (units?)')
pyplot.xlabel('a (units?)')

# Colorbar and label
cbar=pyplot.colorbar(im, orientation = 'vertical')
cbar.set_label('$\chi^2$', fontsize=12)

# Add in best fit point and dashed lines
pyplot.plot(a_soln, b_soln, 'wo')
pyplot.plot((a_soln, a_soln), (b_low, b_soln), linestyle='--', color='w')
pyplot.plot((a_low, a_soln), (b_soln, b_soln), linestyle='--', color='w')


pyplot.figure()
# In[297]:

# A more useful example: Produce a contour plot of 'delta chi-squared' (= chi-squared(a,b) - chi-squared_min)
# Don't worry about 'unicode' warnings on the first run through

X, Y = numpy.meshgrid(a_axis, b_axis, indexing='xy')
contour_data = plot_data - chisq_min

# Contour levels to plot - delta chi-squared of 1, 4 & 9 correspond to 1, 2 & 3 standard deviations
levels = [1, 4, 9]
C_im = pyplot.contour(X, Y, contour_data, levels = levels, colors='b', origin = 'lower')
pyplot.clabel(C_im, levels, fontsize=12, inline=1, fmt=r'$\chi^2 = \chi^2_{min}+%1.0f$')
p = C_im.collections[0].get_paths()[0]
v = p.vertices
print numpy.max(v[:,1]) - b_soln
print b_soln - numpy.min(v[:,1])
print numpy.max(v[:,0]) - a_soln
print a_soln - numpy.min(v[:,0])


# Axis labels
pyplot.xlabel('Intercept')
pyplot.ylabel('Gradient')

# This allows you to modify the tick markers to assess the errors from the chi-squared contour plots.
xtick_spacing = 0.01
ytick_spacing = 0.1

ax = pyplot.gca()
ax.xaxis.set_major_locator(ticker.MultipleLocator(xtick_spacing))
ax.yaxis.set_major_locator(ticker.MultipleLocator(ytick_spacing))


# Add in best fit point and dashed lines to axes
pyplot.plot(a_soln, b_soln, 'ro')
pyplot.plot((a_soln, a_soln), (b_low, b_soln), linestyle='--', color='r')
pyplot.plot((a_low, a_soln), (b_soln, b_soln), linestyle='--', color='r')














#xx = numpy.linspace(0.005, 0.013, 1000)
#yy = func(xx, *popt)

#pyplot.plot(x, numpy.exp(y), 'o', xx, numpy.exp(yy))




eg = (numpy.mean(av_V)) - b_soln * 1.3806503e-23 * id_fac / 1.60217646e-19
print 'av V: ' + str(numpy.mean(av_V)) + ' \pm ' + str(numpy.max(numpy.max(av_V)-numpy.mean(av_V), numpy.mean(av_V) - numpy.min(av_V)))
print 'Eg: ' + str(eg) + ' \pm '
#a,b = popt
#pyplot.plot(1/av_T, numpy.log(av_I))

pyplot.show()