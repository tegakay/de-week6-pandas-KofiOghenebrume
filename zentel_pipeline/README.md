## Zentel Service Data Analysis Pipeline

A comprehensive ETL and analytics pipeline for processing and analyzing service data. This project extracts data from CSV files, transforms and enriches it with lookup tables, performs analytical computations, and generates visualizations and reports.

## Installation

Prerequisites
Python 3.8 or higher
Poetry (for dependency management)

# Clone the repository
git clone https://github.com/yourusername/zentel_pipeline.git
cd zentel_pipeline

# Install dependencies
poetry install

# Activate the virtual environment
poetry shell

# Running the pipeline
poetry run zentel-pipeline

## Reports
# The top 5 operators 
   Operator  Resolution Minutes
0      Akin         6986.250000
4      Boye         7129.983333
7      Fola        10595.466667
13    Kachi        10659.800000
20  Popoola        11734.000000

# The bottom 5 operators 
    Operator  Resolution Minutes
2      Atiku        50966.650000
9     Habeeb        52324.683333
3       Bola        53749.916667
24  Sherifat        55008.166667
11      John        55849.983333

# Slow Response time reasons
                 Fault Type  Count
0             Customers End   2591
1               Line damage    985
2           Routine Service    519
3          hardware failure    198
4  Support network failures    130

Steps should be taken on optimizing most frequent customer issues.
