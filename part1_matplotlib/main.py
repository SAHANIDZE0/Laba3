import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

os.makedirs('img', exist_ok=True)

x_deg = np.linspace(-360, 360, 721)
x_rad = np.deg2rad(x_deg)
p = np.exp(np.sin(x_rad)) + np.log(np.sin(0.5 * x_rad)**2 + 1) * np.cos(x_rad)
q = -np.log((np.sin(x_rad) - np.cos(x_rad))**2 + 2) + 8

fig1, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
ax1.plot(x_deg, p, label='p(x)')
ax1.set_title('p(x)')
ax1.grid(True)
ax1.legend()
ax2.plot(x_deg, q, label='q(x)')
ax2.set_title('q(x)')
ax2.set_xlabel('Градусы')
ax2.grid(True)
ax2.legend()
plt.xticks(np.arange(-360, 361, 90))
plt.tight_layout()
plt.savefig('img/task1.png')
plt.close(fig1)

x = np.linspace(-8, 8, 2000)
with np.errstate(divide='ignore', invalid='ignore'):
    y = 4 / (x**2 - 4)
y[np.abs(y) > 100] = np.nan

fig2, ax = plt.subplots(figsize=(10, 6))
ax.plot(x, y, label='y(x) = 4 / (x² - 4)')
ax.set_ylim(-10, 10)
ax.set_xlim(-8, 8)
ax.axvline(x=2, color='red', linestyle='--', label='x = 2')
ax.axvline(x=-2, color='red', linestyle='--', label='x = -2')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.grid(True)
ax.legend()
plt.savefig('img/task2.png')
plt.close(fig2)

fig3, ax = plt.subplots(figsize=(8, 6))
sky = patches.Rectangle((0, 0), 10, 8, facecolor='skyblue')
ax.add_patch(sky)
sun = patches.Circle((8, 7), 0.8, facecolor='yellow', edgecolor='orange')
ax.add_patch(sun)
ground = patches.Rectangle((0, 0), 10, 2, facecolor='green')
ax.add_patch(ground)
house = patches.Rectangle((2, 2), 3, 2.5, facecolor='brown', edgecolor='black')
ax.add_patch(house)
roof = patches.Polygon([[1.8, 4.5], [5.2, 4.5], [3.5, 6]], closed=True, facecolor='red', edgecolor='black')
ax.add_patch(roof)
door = patches.Rectangle((3.2, 2), 0.6, 1.2, facecolor='saddlebrown', edgecolor='black')
ax.add_patch(door)
window = patches.Rectangle((4.0, 3.2), 0.6, 0.6, facecolor='lightyellow', edgecolor='black')
ax.add_patch(window)
cloud1 = patches.Ellipse((2, 7), 2, 0.8, facecolor='white', edgecolor='gray')
cloud2 = patches.Ellipse((2.5, 7.2), 1.5, 0.7, facecolor='white', edgecolor='gray')
ax.add_patch(cloud1)
ax.add_patch(cloud2)
rainbow = patches.Arc((8, 0), 3, 3, theta1=0, theta2=180, color='purple', linewidth=3)
ax.add_patch(rainbow)
ax.set_xlim(0, 10)
ax.set_ylim(0, 8)
ax.set_aspect('equal')
ax.axis('off')
plt.savefig('img/task3.png', bbox_inches='tight')
plt.close(fig3)

print("Готово! Картинки сохранены в папку img")