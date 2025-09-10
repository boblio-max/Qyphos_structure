import matplotlib.pyplot as plt
import numpy as np
from typing import Dict
from . import backends as be

def plot_histogram(counts: Dict[str, int], title: str = "Measurement Outcomes"):
    # (Same code as the previous version, no changes needed)
    # ...
    pass # For brevity

def plot_density_matrix(dm: be.array, title="Density Matrix"):
    """Visualizes a density matrix using two heatmaps for real and imaginary parts."""
    dm_np = be.to_numpy(dm)
    real_part = np.real(dm_np)
    imag_part = np.imag(dm_np)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle(title, fontsize=16, fontweight='bold')

    # Plot Real Part
    cax1 = ax1.imshow(real_part, cmap='viridis', interpolation='nearest')
    ax1.set_title('Real Part')
    fig.colorbar(cax1, ax=ax1)

    # Plot Imaginary Part
    cax2 = ax2.imshow(imag_part, cmap='plasma', interpolation='nearest')
    ax2.set_title('Imaginary Part')
    fig.colorbar(cax2, ax=ax2)
    
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()
