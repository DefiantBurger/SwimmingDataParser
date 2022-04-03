import matplotlib.pyplot as plt

from functions import get_swim_times

event = "Event 16  Boys 500 Yard Freestyle"
swimmers = ["Sean Maloney"]
plots = [(sw, get_swim_times(sw.split()[0], sw.split()[1], event)["seconds_times"]) for sw in swimmers]

for p in plots:
    try:
        plt.plot(p[1], label=p[0])
    except ValueError:
        continue

plt.legend()
plt.show()
