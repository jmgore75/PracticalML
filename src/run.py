# %matplotlib inline
import matplotlib.pyplot as plt
import mpld3
from mpld3 import plugins
mpld3.enable_notebook()

####


def plot_runs(fig, ax, tracker, run):
    groups = tracker.runs.groupby(['run_hash'])
    for run_hash, grp in groups:
        points = ax.plot(
            grp['train_time'], grp['test_score'],
            'o', label=model)
        labels = grp["model"]
        tooltip = plugins.PointLabelTooltip(points, labels)
        plugins.connect(fig, tooltip)

    if run:
        ax.plot(
            run["train_time"], run["test_score"],
            '*', color="y", s=50, label="Latest")
        ax.title(
            'Last: %.3f; Best: %.3f' % (grp['test_score'], tracker.max_score))
    ax.xlabel("Train time")
    ax.ylabel("Test score")
    ax.legend(loc="best")
    ax.figure()

    for model, grp in groups:
        ax.plot(
            grp['train_score'], grp['test_score'],
            'o', label=model)
    if run:
        ax.plot(
            run["train_score"], run["test_score"],
            '*', color="y", s=50, label="Latest")
        ax.title(
            'Last: %.3f; Best: %.3f' % (grp['test_score'], tracker.max_score))
    ax.xlabel("Train time")
    ax.ylabel("Test score")
    ax.legend(loc="best")

    mpld3.display()

#####

from tracking import RunTracker
path = "forestCover"
tracker = RunTracker("forestCover")

X = None
y = None

tracker.setData(X, y, True)

####
import classifiers

fig, ax = plt.subplots()

plot_runs(fig, ax, tracker)

for run in tracker.run_models(classifiers.starting_models(), cv):
    plot_runs(fig, ax, tracker, run)
