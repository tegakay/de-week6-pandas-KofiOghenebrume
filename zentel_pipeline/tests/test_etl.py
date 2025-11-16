import pytest
from src.zentel_pipeline.etl import ZentelETL
import numpy as np
import pandas as pd

@pytest.fixture
def client():
    return ZentelETL()

def test_get_sla_rating(client):
    assert client.get_sla_rating(200) == "Critical"
    assert client.get_sla_rating(150) == "Fair"

def test_load_tables(client):
    df = client.load_tables("location.csv")
    assert not df.empty
    assert "State Key" in df.columns

def test_compute_sla_metrics(client):
    sample_data = {
        "Ticket Open Time": ["2023-01-01 08:00:00"],
        "Ticket Resp Time": ["2023-01-01 08:05:00"],
        "Issue Res Time": ["2023-01-01 09:00:00 "]
    }
    df = pd.DataFrame(sample_data)
    df = df.apply(lambda col: pd.to_datetime(col, errors="coerce"))
    cleaned_df = client.compute_sla_metrics(df)
    assert "Response Seconds" in cleaned_df.columns
    assert "Resolution Minutes" in cleaned_df.columns
