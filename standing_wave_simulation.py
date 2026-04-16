import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# --- 実験テキストに基づくパラメータ設定 ---
f = 5.0e9          # 周波数: 5 GHz [cite: 87]
c = 3.0e8          # 光速: 3.0e8 m/s [cite: 53]
lam = c / f        # 波長 lambda [cite: 48]
beta = 2 * np.pi / lam  # 位相定数 beta [cite: 48]

a_abs = 5.0        # 入射波振幅 |a| [cite: 87]
r_abs = 0.5        # 反射係数絶対値 |r| [cite: 87]
theta = 0  # 反射係数の位相 theta [cite: 87]

# 空間軸の設定 (0 to 100mm) [cite: 87]
x = np.linspace(0, 0.1, 500) 

# --- グラフの初期設定 ---
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlim(0, 100)
ax.set_ylim(-10, 10)
ax.set_xlabel('Position x [mm]')
ax.set_ylabel('Voltage V [V]')
ax.grid(True)

line_inc, = ax.plot([], [], 'b-', alpha=0.3, label='Incident Wave (Forward)')
line_ref, = ax.plot([], [], 'r-', alpha=0.3, label='Reflected Wave (Backward)')
line_sum, = ax.plot([], [], 'k-', lw=2, label='Standing Wave (Total)')
# 式11に基づく振幅分布 (Envelope) [cite: 85]
v_amp = a_abs * np.sqrt(1 + 2 * r_abs * np.cos(2 * beta * x + theta) + r_abs**2)
ax.plot(x * 1000, v_amp, 'g--', alpha=0.5, label='Amplitude Distribution |Vx|')
ax.plot(x * 1000, -v_amp, 'g--', alpha=0.5)
ax.legend(loc='upper right')

def update(frame):
    t = frame / (f * 20)  # 時間ステップ
    omega = 2 * np.pi * f
    
    # 複素表記式を実数成分の波動として計算 [cite: 52]
    # 入射波: a * exp(j(wt - bx))
    v_inc = a_abs * np.cos(omega * t - beta * x)
    # 反射波: a * r * exp(j(wt + bx + theta))
    v_ref = a_abs * r_abs * np.cos(omega * t + beta * x + theta)
    # 合成波
    v_total = v_inc + v_ref
    
    line_inc.set_data(x * 1000, v_inc)
    line_ref.set_data(x * 1000, v_ref)
    line_sum.set_data(x * 1000, v_total)
    return line_inc, line_ref, line_sum

ani = FuncAnimation(fig, update, frames=200, interval=100, blit=True)
plt.title(f'Standing Wave Simulation (f={f/1e9}GHz, |r|={r_abs})')
plt.show()