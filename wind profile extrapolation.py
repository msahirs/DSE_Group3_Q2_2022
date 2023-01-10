from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.pipeline import make_pipeline
import matplotlib.pyplot as plt
import numpy as np
import scipy as sc

# pink line
def wind_model(h):
    dataset = np.array([[0, 11],
                        [2500, 15],
                        [5000, 29],
                        [7500, 41],
                        [10000, 51],
                        [12000, 43],
                        [13500, 32],
                        [16000, 20],
                        [17000, 11],
                        [20000, 9],
                        [23000, 11],
                        [25500, 15]])

    y = dataset[:,1]  # wind speed
    x = dataset[:,0]  # altitude
    f = sc.interpolate.interp1d(x,y,kind='quadratic')
    return f(h)

# degrees = [3, 4, 5, 6, 7, 8, 9, 10]
# for degree in degrees:
#     model = make_pipeline(PolynomialFeatures(degree), Ridge(alpha=1e-3))
#     model.fit(x.reshape(-1,1), y.reshape(-1,1))
#     y_plot = model.predict(x.reshape(-1,1))
#     plt.plot(x, y_plot, label=f"degree {degree}")

    # poly = PolynomialFeatures(degree=degree)#, include_bias=False)
    # poly_features = poly.fit_transform(x.reshape(-1,1))
    # poly_reg_model = LinearRegression()
    # poly_reg_model.fit(poly_features, y)
    # y_predicted = poly_reg_model.predict(poly_features)
    # coeff = poly_reg_model.coef_
    # plt.plot(x, y_predicted)
    #
    # xvalues = np.linspace(0, 30000, 5000)
    # yvalues = []
    # for x_value in xvalues:
    #     yvalue = 0
    #     for numbj, item in enumerate(coeff):
    #         yvalue += item * x_value ** (degree - numbj)
    #     yvalues.append(yvalue)
    #
    # # plt.plot(xvalues, yvalues)
    # print(coeff)

# xrange = np.arange(0,25001, 100)
# yinter = f(xrange)
#
# plt.scatter(x, y)
# plt.plot(xrange,yinter)
# plt.legend()
#
# plt.show()
