import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# figure and axis
fig, ax = plt.subplots(figsize=(15, 2))

# patches for each window
estimation_window = mpatches.Rectangle((-12, 0), 11, 1, facecolor='blue', edgecolor='black')
event_window = mpatches.Rectangle((-1, 0), 3, 1, facecolor='green', edgecolor='black')
post_event_window = mpatches.Rectangle((2, 0), 59, 1, facecolor='red', edgecolor='black')

# add patches to the plot
ax.add_patch(estimation_window)
ax.add_patch(event_window)
ax.add_patch(post_event_window)

# labels and title
ax.text(-6, -0.5, 'Estimation Window', verticalalignment='center', horizontalalignment='center')
ax.text(0, 1.5, 'Event Window', verticalalignment='center', horizontalalignment='center')
ax.text(30, -0.5, 'Post-Event Window', verticalalignment='center', horizontalalignment='center')

# arrow and text for Earnings Announcement
arrowprops = dict(facecolor='black', edgecolor='black', arrowstyle='->,head_width=0.5,head_length=0.7')
ax.annotate('Earnings Announcement', xy=(0, 0), xytext=(0, -0.5),
            arrowprops=arrowprops,
            horizontalalignment='left', verticalalignment='center')

# axis limits and labels
ax.set_xlim(-12, 60)  # adjusted to remove gaps at the ends
ax.set_ylim(-1, 2)  # adjusted to make room for labels
ax.set_yticks([])
ax.set_xticks([-12, -1, 2, 60])  # adjusted tick positions
ax.set_xticklabels(['-12', '-1', '1', '60'])  # adjusted tick labels

# title
plt.title('Timeline for Abnormal Returns Analysis')

plt.show()
