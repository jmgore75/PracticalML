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
    groups = tracker.runs.groupby(['run_hash'])
    for run_hash, grp in groups:
        ax1.plot(
            grp['train_time'], grp['cv_score'],
            'o')

    if run:
        ax1.plot(
            run["train_time"], run["cv_score"],
            '*', color="y", label="Latest")
    ax1.set_xlabel("Train time")
    ax1.set_ylabel("Test score")

    for run_hash, grp in groups:
        ax2.plot(
            grp['train_score'], grp['cv_score'],
            'o')
    if run:
        ax2.plot(
            run["train_score"], run["cv_score"],
            '*', color="y", label="Latest")
    ax2.set_xlabel("Train score")
    ax2.set_ylabel("Test score")
