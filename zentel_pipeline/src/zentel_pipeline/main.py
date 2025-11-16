from zentel_pipeline.etl import ZentelETL
import logging
from zentel_pipeline.analysis import ZentelAnalysis


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(message)s")

def main():
    zentel = ZentelETL("data")
    df = zentel.load_tables("service_data.csv")
    logger.info("Data loaded successfully.")
    print(list(df.columns))

    df = zentel.clean_tickets(df)
    # get df for other data
    channel_df = zentel.load_tables("channel_type.csv")
    employee_df = zentel.load_tables("employee.csv")
    fault_df = zentel.load_tables("fault_type.csv")
    location_df = zentel.load_tables("location.csv")
    service_type_df = zentel.load_tables("service_type.csv")
    logger.info("Data cleaned successfully.")

    # data merging and enrichment
    # follow this format
    enriched_df = zentel.enrich_tickets(df, channel_df, employee_df, fault_df, location_df, service_type_df)
    print(enriched_df.head())
    print(list(enriched_df.columns))

    # SLA computations
    sla_df = zentel.compute_sla_metrics(enriched_df)

    # rankings
    rankings_df = zentel.manager_operator_performance(sla_df)
    print(rankings_df.head())
    
    #Report Analysis
    analysis = ZentelAnalysis()
    # Generate Weekly KPI Report
    analysis.weekly_kpi_report(sla_df)

    # Generate Manager and Operator Performance Report
    manager_df = analysis.manager_operator_report(sla_df)
    logging.info("Operator Performance Report generated.")
    logging.info("The top 5 performers are:")
    print(manager_df.head())
    # with open("df_head.txt", "w") as f:
        # f.write(df.head().to_string())

    logging.info("The bottom 5 performers are:")
    print(manager_df.tail())

    # Perform Escalation Analysis
    analysis.escalation_analysis(sla_df)

    #Reason for slow response Time
    
if __name__ == "__main__":
    main()