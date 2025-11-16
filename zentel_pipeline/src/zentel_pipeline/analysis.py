from typing import Dict
import pandas as pd
import numpy as np
import logging
import os
from zentel_pipeline.etl import ZentelETL
from zentel_pipeline.viz import ZentelViz

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(message)s")

weekly_kpi_path = os.path.join(os.getcwd(), "kpi_report.csv")
manager_path = os.path.join(os.getcwd(), "manager_report.csv")
escalation_path = os.path.join(os.getcwd(), "escalation_report.csv")


class ZentelAnalysis:
    def __init__(self):
        pass

    def weekly_kpi_report(self,df: pd.DataFrame) -> pd.DataFrame:
        """Generate a weekly KPI report from the tickets DataFrame."""
        zentel = ZentelETL()
        results_df = zentel.manager_operator_performance(df, type="Weekly")
        #Generate Visualizations
        viz = ZentelViz()
        viz.plot_manager_resolution_bar(results_df)

        results_df.to_csv(weekly_kpi_path, index=False)
        

    def manager_operator_report(self,df: pd.DataFrame) -> pd.DataFrame:
        """Generate a report on manager and operator performance."""
        zentel = ZentelETL()
        results_df = zentel.manager_operator_performance(df, type="Weekly")

        df.to_json(manager_path, orient="records", indent=4)
        return results_df

        

    def escalation_analysis(self,df: pd.DataFrame) -> pd.DataFrame:
        """Analyze ticket escalations within the DataFrame."""
        results_df = df[df["Esclation Status"] == "Flagged"]
        results_df.to_csv(escalation_path, index=False)