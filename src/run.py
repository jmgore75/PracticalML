####
labelFormat = '''<table style="max-width:100px">
<tr><th>Score</th><td>{score:.3f}</td></tr>
<tr><th>Train time</th><td>{training:.1f} s</td></tr>
<tr><th>Score time</th><td>{scoring:.1f} s</td></tr>
<tr><th>Size</th><td>{bytes} bytes</td></tr>
<tr><td colspan=2>{model}</td></tr>
</table>
'''


def labelRow(row):
    return labelFormat.format(
        model=row["model"], bytes=row["model_bytes"], score=row["cv_score"],
        training=row["train_time"], scoring=row["score_time"])


def plot_runs(fig, ax1, ax2, tracker, run=None):
    ax1.clear()
    ax1.set_xlabel("Train time")
    ax1.set_xscale('log')
    ax1.set_ylabel("Test error")
    ax1.set_yscale('symlog')
    ax2.clear()
    ax2.set_xlabel("Train error")
    ax2.set_xscale('symlog')
    ax2.set_ylabel("Test error")
    ax2.set_yscale('symlog')

    groups = tracker.runs.groupby(['model_type'])
    for mtype, grp in groups:
        ax1.plot(
            grp['train_time'], 1-grp['cv_score'],
            'o', label=mtype)
        ax2.plot(
            1-grp['train_score'], 1-grp['cv_score'],
            'o', label=mtype)

    ax1.legend(loc="auto")
    ax2.legend(loc="auto")

    if run:
        ax1.plot(
            run["train_time"], 1-run["cv_score"],
            '*', color="y", label="Latest", markersize=14)
        ax2.plot(
            1-run["train_score"], 1-run["cv_score"],
            '*', color="y", label="Latest", markersize=14)
