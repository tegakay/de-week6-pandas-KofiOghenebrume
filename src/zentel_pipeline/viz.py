import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

data_dir = Path(__file__).parent.parent.parent /'reports'


class ZentelViz:
    def __init__(self):
        pass

    def plot_manager_resolution_bar(self, df: pd.DataFrame, ) -> None:
        """Plot weekly KPI from the provided DataFrame."""
        fig,ax = plt.subplots(figsize=(10, 6))
        ax.bar(df['Operator'], df['Resolution Minutes'], color='skyblue')
        ax.set_title('Operator Resolution Time')
        ax.set_xlabel('Operator')
        ax.set_ylabel('Resolution Time (Mins)')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        file = data_dir/'operator_resolution_time.png'
        fig.savefig(file)
        plt.close(fig)

