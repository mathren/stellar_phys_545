# prototyped with Claude

import numpy as np
import matplotlib.pyplot as plt

def instability_profile(t, t_onset, t_saturation, y_initial, y_final, growth_rate):
    """
    Calculate the quantity as a function of time showing instability onset.

    Parameters:
    -----------
    t : array
        Time array
    t_onset : float
        Time when instability begins
    t_saturation : float
        Time when growth saturates
    y_initial : float
        Initial constant value
    y_final : float
        Final constant value after saturation
    growth_rate : float
        Exponential growth rate

    Returns:
    --------
    y : array
        Quantity values
    """
    y = np.zeros_like(t)
    dt_max = t_saturation-t_onset
    for i, time in enumerate(t):
        if time < t_onset:
            # Pre-instability: constant value
            y[i] = y_initial
        elif time < t_saturation:
            # Exponential growth phase
            dt = time - t_onset
            # Exponential growth from initial to final value
            y[i] = y_initial + (y_final - y_initial) * (np.exp(growth_rate * dt)-1)/(np.exp(growth_rate*dt_max)-1)
        else:
            # Post-saturation: new constant value
            y[i] = y_final

    return y

if __name__ == "__main__":
    # Parameters
    t_onset = 2.0          # Time when instability starts
    t_saturation = 6.0     # Time when growth saturates
    y_initial = 1.0        # Initial constant value
    y_final = 5.0          # Final saturated value
    growth_rate = 1.5      # Growth rate parameter

    # Time array
    t = np.linspace(0, 10, 1000)

    # Calculate the quantity
    y = instability_profile(t, t_onset, t_saturation, y_initial, y_final, growth_rate)

    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot the main curve
    ax.plot(t, y, 'b-') #, label='Quantity evolution')

    # Mark the critical times
    # ax.axvline(t_onset, color='red', linestyle='--', linewidth=1.5,
    #            alpha=0.7, label=f'Instability onset')
    # ax.axvline(t_saturation, color='green', linestyle='--', linewidth=1.5,
    #            alpha=0.7, label=f'Saturation')

    # Mark the constant levels
    ax.axhline(y_initial, color='gray', linestyle=':', linewidth=1, alpha=0.5)
    ax.axhline(y_final, color='gray', linestyle=':', linewidth=1, alpha=0.5)

    # Add shaded regions to highlight phases
    ax.axvspan(0, t_onset, alpha=0.1, color='blue', label='Stable phase')
    ax.axvspan(t_onset, t_saturation, alpha=0.1, color='red', label='Growth phase')
    ax.axvspan(t_saturation, t[-1], alpha=0.1, color='green', label='Saturated phase')

    # Labels and title
    ax.set_xlabel('Time (t)')
    ax.set_ylabel('Quantity (Q)')
    # ax.set_title('Onset of Instability: Transition from Stable to Unstable Growth',
    #              fontsize=16, fontweight='bold', pad=20)

    # Add annotations
    ax.annotate('Initial\nsteady\nstate', xy=(t_onset/2, y_initial),
                xytext=(t_onset/2, y_initial + 1),
                fontsize=20, ha='center',
                arrowprops=dict(arrowstyle='->', color='black', lw=1.5))

    ax.annotate('Exponential\ngrowth', xy=(t_onset + 1.5, 1.2),
                xytext=(t_onset + 1.5, 3.5),
                fontsize=20, ha='center',
                arrowprops=dict(arrowstyle='->', color='black', lw=1.5))

    ax.annotate('New saturated\nsteady state', xy=(t_saturation + 2, y_final),
                xytext=(t_saturation + 2, y_final - 2),
                fontsize=20, ha='center',
                arrowprops=dict(arrowstyle='->', color='black', lw=1.5))

    # Grid and legend
    # ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
    # ax.legend(loc='upper left', framealpha=0.9, frameon=True)

    # Set axis limits for better visualization
    ax.set_xlim(0, t[-1])
    ax.set_ylim(0, y_final + 1)
    ax.set_yticklabels([])
    ax.set_xticklabels([])

    tx = ax.twiny()
    tx.set_xlim(ax.get_xlim())
    tx.set_xticks([t_onset,  t_saturation], minor=False)
    tx.set_xticklabels(["Onset", "Saturation"])
    tx.tick_params(axis='both', which='major', labelsize=20)

    plt.tight_layout()
    plt.savefig('../html-content/images/instability_onset.png', dpi=300, bbox_inches='tight')
    plt.show()

    print("Plot saved successfully!")
    print(f"\nParameters used:")
    print(f"  Initial value: {y_initial}")
    print(f"  Final value: {y_final}")
    print(f"  Instability onset: t = {t_onset}")
    print(f"  Saturation time: t = {t_saturation}")
    print(f"  Growth rate: {growth_rate}")
