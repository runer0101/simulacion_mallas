import io
from typing import Dict

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle


def dibujar_circuito(vals: Dict[str, float]) -> io.BytesIO:
    fig, ax = plt.subplots(figsize=(8, 4))
    fig.patch.set_facecolor('#222')
    ax.set_facecolor('#222')
    ax.axis('off')

    ax.plot([0.5, 6.5], [3, 3], color='white', lw=3)
    ax.plot([0.5, 6.5], [1, 1], color='white', lw=3)
    ax.plot([0.5, 0.5], [1, 3], color='white', lw=3)
    ax.plot([2.5, 2.5], [1, 3], color='white', lw=3)
    ax.plot([4.5, 4.5], [1, 3], color='white', lw=3)
    ax.plot([6.5, 6.5], [1, 3], color='white', lw=3)

    ax.text(1.5, 3.15, f"R₁={vals['R1']}Ω", color='orange', fontsize=13, ha='center', va='bottom', fontweight='bold')
    ax.text(3.5, 3.15, f"R₃={vals['R3']}Ω", color='orange', fontsize=13, ha='center', va='bottom', fontweight='bold')
    ax.text(5.5, 3.15, f"R₅={vals['R5']}Ω", color='orange', fontsize=13, ha='center', va='bottom', fontweight='bold')
    ax.text(0.7, 2, f"R₂={vals['R2']}Ω", color='orange', fontsize=13, ha='left', va='center', fontweight='bold', rotation=90)
    ax.text(2.7, 2, f"R₄={vals['R4']}Ω", color='orange', fontsize=13, ha='left', va='center', fontweight='bold', rotation=90)
    ax.text(4.7, 2, f"R₆={vals['R6']}Ω", color='orange', fontsize=13, ha='left', va='center', fontweight='bold', rotation=90)

    fuente_x, fuente_y = 0.5, 2.6
    circle = Circle((fuente_x, fuente_y), 0.18, fill=False, edgecolor='cyan', lw=2)
    ax.add_patch(circle)
    ax.text(fuente_x - 0.15, fuente_y + 0.15, '+', color='cyan', fontsize=14, ha='center', va='center')
    ax.text(fuente_x - 0.15, fuente_y - 0.15, '-', color='cyan', fontsize=14, ha='center', va='center')
    ax.text(fuente_x - 0.4, fuente_y, f"V₁={vals['V1']}V", color='cyan', fontsize=13, ha='right', va='center', fontweight='bold')

    def flecha_corriente(x1, y1, x2, y2, label):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(facecolor='lime', edgecolor='lime', arrowstyle='->', lw=2))
        ax.text((x1 + x2) / 2, y1 - 0.18, label, color='lime', fontsize=15, ha='center', va='top', fontweight='bold')

    flecha_corriente(1, 0.9, 2, 0.9, 'I₁')
    flecha_corriente(3, 0.9, 4, 0.9, 'I₂')
    flecha_corriente(5, 0.9, 6, 0.9, 'I₃')

    ax.text(1.5, 0.6, 'Malla 1\n(Cocina)', color='white', fontsize=13, ha='center', va='center')
    ax.text(3.5, 0.6, 'Malla 2\n(Sala)', color='white', fontsize=13, ha='center', va='center')
    ax.text(5.5, 0.6, 'Malla 3\n(Dormitorios)', color='white', fontsize=13, ha='center', va='center')
    ax.set_xlim(0, 7)
    ax.set_ylim(0.3, 3.5)

    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close(fig)
    buf.seek(0)
    return buf
