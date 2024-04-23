import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
matplotlib.use('Agg')

def plot_data(data, name):
    plt.figure(name)
    x_values = [entry[0] for entry in data]
    y_values = [entry[1] for entry in data]
    z_values = [entry[2] for entry in data]

    fig = plt.figure(num=name, figsize=(20, 12))
    ax1 = fig.add_subplot()

    ax1.plot(x_values, y_values, 'bo')
    ax1.plot(x_values, y_values, label='h-index', color='blue')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('h-index', color='blue')

    ax2 = ax1.twinx()
    ax2.plot(x_values, z_values, 'ro')
    ax2.plot(x_values, z_values, label='citations', color='red')
    ax2.set_ylabel('citations', color='red')

    ax1.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))

    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines + lines2, labels + labels2, loc='best')

    plt.title("Citations and H-index by Year")
    plt.subplots_adjust(right=0.85)
    plt.subplots_adjust(top=0.90)

    plt.grid(True)
    plt.savefig(name + ".png", dpi=300)