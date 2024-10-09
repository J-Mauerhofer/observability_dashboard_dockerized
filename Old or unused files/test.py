import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_arrow(ax, start, end, color='black'):
    ax.annotate('', xy=end, xytext=start,
                arrowprops=dict(arrowstyle='->', color=color, lw=1))

# Set up the plot
fig, ax = plt.subplots(figsize=(12, 8))

# Define node positions
positions = {
    'A': (0.2, 0.5),
    'B': (0.3, 0.8), 'C': (0.3, 0.2),
    'D': (0.6, 0.8), 'E': (0.6, 0.2),
    'F': (0.8, 0.7), 'G': (0.8, 0.3)
}

# Draw nodes
for node, pos in positions.items():
    circle = plt.Circle(pos, 0.05, fill=False)
    ax.add_patch(circle)
    ax.text(pos[0], pos[1], node, ha='center', va='center')

# Draw arrows
draw_arrow(ax, positions['B'], positions['D'])
draw_arrow(ax, positions['B'], positions['E'])
draw_arrow(ax, positions['C'], positions['D'])
draw_arrow(ax, positions['C'], positions['E'])
draw_arrow(ax, positions['F'], positions['G'])
draw_arrow(ax, positions['G'], positions['F'])
draw_arrow(ax, positions['F'], (positions['F'][0]+0.03, positions['F'][1]+0.03), color='red')
draw_arrow(ax, positions['G'], (positions['G'][0]+0.03, positions['G'][1]-0.03), color='red')

# Add labels
ax.text(0.2, 0.57, '<init>', ha='center', va='bottom')
ax.text(0.3, 0.87, 'updateSystem:\nI7 true', ha='center', va='bottom')
ax.text(0.3, 0.13, 'updateSystem:\nI7 false', ha='center', va='top')
ax.text(0.6, 0.87, 'updateSystem:\nI34 true', ha='center', va='bottom')
ax.text(0.6, 0.13, 'updateSystem:\nI34 false', ha='center', va='top')
ax.text(0.8, 0.77, 'calcAvgTempDiff:\nI16 true', ha='center', va='bottom')
ax.text(0.8, 0.23, 'calcAvgTempDiff:\nI16 false', ha='center', va='top')

# Set the limits and remove axes
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')

# Add a title
plt.title("Dependency Graph for SmartThermostat", fontsize=16)

# Show the plot
plt.tight_layout()
plt.show()