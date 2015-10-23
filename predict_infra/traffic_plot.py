import matplotlib.pyplot as plt
import scipy as sp

data = sp.genfromtxt("data/web_traffic.tsv", delimiter="\t")
x = data[:,0]
y = data[:,1]

# see how many hours contain invalid data
sp.sum(sp.isnan(y))

# logically negate the array of booleans that indicate
# whether an entry is a number or not
x = x[~sp.isnan(y)]
y = y[~sp.isnan(y)]


def show_web_traffic():
    plt.scatter(x,y,s=10)
    plt.title("Web traffic over the last month")
    plt.xlabel("Time")
    plt.ylabel("Hits/hour")
    plt.xticks([w*7*24 for w in range(10)],
               ['week %i' % w for w in range(10)])
    plt.autoscale(tight=True)
    plt.grid(True, linestyle='-', color='0.75')
    plt.show()

def error(f, x=x, y=y):
    return sp.sum((f(x)-y)**2)

def model_straight_line(x=x, y=y):
    fp1, residuals, rank, sv, rcond = sp.polyfit(x, y, 1, full=True)
    f1 = sp.poly1d(fp1)
    # generate X-values for plotting
    fx = sp.linspace(0,x[-1], 1000)

    plt.plot(fx, f1(fx), linewidth=4)
    plt.legend(["d=%i" % f1.order], loc="upper left")
    plt.scatter(x,y,s=10)
    plt.title("Web traffic over the last month")
    plt.xlabel("Time")
    plt.ylabel("Hits/hour")
    plt.xticks([w*7*24 for w in range(10)],
               ['week %i' % w for w in range(10)])
    plt.autoscale(tight=True)
    plt.grid(True, linestyle='-', color='0.75')
    plt.show()

    return ("Model parameters: %s" % fp1) , residuals, error(f1, x, y)


if __name__ == "__main__":
    print model_straight_line()
    show_web_traffic()
