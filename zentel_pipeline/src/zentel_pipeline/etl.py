from typing import Dict
import pandas as pd
import numpy as np
import logging
from pathlib import Path

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(message)s")

class ZentelETL:
    def __init__(self, folder_path: str = "data"):
        self.folder_path = folder_path
    
    @classmethod
    def get_sla_rating(cls,num):
        if num < 30:
            return 'Excellent'
        elif num > 30 and num < 60:
            return 'Good'
        elif num > 60 and num < 180:
            return 'Fair'
        else:
            return 'Critical'

    def load_tables(self,path: str) -> Dict[str, pd.DataFrame]:
        """Load  tables from CSV file into a DataFrame."""
        data_dir = Path(__file__).parent.parent.parent/self.folder_path
        file = data_dir/path
        logging.info(f"Loading data from {file}")
        return pd.read_csv(file)

    def clean_tickets(self,df: pd.DataFrame) -> pd.DataFrame:
        """Clean and preprocess the tickets DataFrame."""
        logging.info("Cleaning tickets data")
        df = df.apply(lambda col: col.str.strip() if col.dtype == "object" else col)
        logging.info("stripping out bad alues")
        df.replace(["-", "--", "none", "null", "N/A", "na", "#N/A"], None, inplace=True)
        logging.info("drop duplicates")
        df.drop_duplicates(inplace=True)

        # type conversions
        string_cols = ["Report ID", "Report Channel", "Customer Name", "State Key", "Fault Type", "Ticket Status", "Business Status"]
        df[string_cols] = df[string_cols].astype("string")

        date_cols = ["Ticket Open Time", "Ticket Resp Time", "Issue Res Time", "Ticket Close Time"]
        df[date_cols] = df[date_cols].apply(lambda col: pd.to_datetime(col, errors="coerce"))
        return df
        

    def compute_sla_metrics(self,tickets_df: pd.DataFrame) -> pd.DataFrame:
        """Enrich tickets DataFrame with user information."""
        # add response seconds, response sla pass, resolution minutes
        # ticket_resp_time - ticket_open_time
        
        tickets_df["Response Seconds"] = (tickets_df["Ticket Resp Time"] - tickets_df["Ticket Open Time"]).dt.total_seconds()
        tickets_df["Response SLA Pass"] = np.where(tickets_df["Response Seconds"] < 10, True, False)
        tickets_df["Resolution Minutes"] = (tickets_df["Issue Res Time"] - tickets_df["Ticket Resp Time"]).dt.total_seconds() / 60
        tickets_df["Resolution SLA"] = tickets_df["Resolution Minutes"].apply(ZentelETL.get_sla_rating)
        tickets_df["Esclation Status"] = np.where(tickets_df["Resolution SLA"] == "Critical", 'Flagged', 'Normal')
        return tickets_df

        

    def enrich_tickets(self,main_df: pd.DataFrame,
                            channel_type_df: pd.DataFrame,
                            employee_df: pd.DataFrame,
                            fault_type_df:pd.DataFrame,
                            locaton_df:pd.DataFrame,
                            service_type_df:pd.DataFrame,) -> pd.DataFrame:
        """Compute SLA metrics for the tickets DataFrame."""

        result_df = main_df.merge(channel_type_df, left_on='Report Channel', right_on="Channel Key", how='left') \
            .merge(employee_df, left_on='Operator', right_on="Employee_name", how='left') \
            .merge(fault_type_df, left_on='Fault Type', right_on="Fault", how='left') \
            .merge(locaton_df, on="State Key", how='left') \
            # .merge(service_type_df, left_on='Report Channel', right_on="Channel Key", how='left')
        return result_df

    def manager_operator_performance(self,df: pd.DataFrame, type="Daily") -> pd.DataFrame:
        """Analyze performance metrics for managers and operators."""
        # get completed tickets
        results_df = df[df["Ticket Status"] == "Completed"]
        if type == "Daily":
            result = results_df.groupby("Operator")["Resolution Minutes"].sum().reset_index().sort_values("Resolution Minutes", ascending=True)
        else:
            result = results_df.groupby("Operator")["Resolution Minutes"].sum().reset_index().sort_values("Resolution Minutes", ascending=True)
            
        
        return result
        

# zentel = ZentelETL("data")
# df = zentel.load_tables("service_data.csv")
# logger.info("Data loaded successfully.")
# print(list(df.columns))

# df = zentel.clean_tickets(df)
# # get df for other data
# channel_df = zentel.load_tables("channel_type.csv")
# employee_df = zentel.load_tables("employee.csv")
# fault_df = zentel.load_tables("fault_type.csv")
# location_df = zentel.load_tables("location.csv")
# service_type_df = zentel.load_tables("service_type.csv")
# logger.info("Data cleaned successfully.")

# # data merging and enrichment
# # follow this format
# enriched_df = zentel.enrich_tickets(df, channel_df, employee_df, fault_df, location_df, service_type_df)
# print(enriched_df.head())
# print(list(enriched_df.columns))

# sla_df = zentel.compute_sla_metrics(enriched_df)

# # rankings
# rankings_df = zentel.manager_operator_performance(sla_df)
# print(rankings_df.head())