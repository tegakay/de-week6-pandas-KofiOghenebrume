import pytest
from src.zentel_pipeline.analysis import ZentelAnalysis
import numpy as np
import pandas as pd

@pytest.fixture
def client():
    return ZentelAnalysis()
