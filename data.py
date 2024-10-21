import pandas as pd
import requests
import numpy as np

def cleaned_api():
    """
    Retrieves data from the Chicago city portal API.

    Returns:
        Cleaned API Chicago Public Schools DataFrame (SY2017-2018).
    """
    url_chicago_portal = "https://data.cityofchicago.org/resource/w4qj-h7bg.json"
    response_API = requests.get(url_chicago_portal)
    df = pd.read_json(response_API.text)

    filtered_df = df[
        [
            "zip",
            "student_attainment_rating",
            "culture_climate_rating",
            "mobility_rate_pct",
            "chronic_truancy_pct",
            "sat_grade_11_score_school",
            "one_year_dropout_rate_year",
            "one_year_dropout_rate_year_1",
            "suspensions_per_100_students_1",
            "suspensions_per_100_students_2",
            "school_latitude",
            "school_longitude",
            "long_name",
        ]
    ]

    attainment_mapping = {
        "FAR BELOW EXPECTATIONS": 1,
        "BELOW AVERAGE": 2,
        "AVERAGE": 3,
        "ABOVE AVERAGE": 4,
        "MET EXPECTATIONS": 5,
        "FAR ABOVE EXPECTATIONS": 6,
    }
    climate_mapping = {
        "NOT ENOUGH DATA": None,
        "WELL ORGANIZED": 5,
        "ORGANIZED": 4,
        "MODERATELY ORGANIZED": 3,
        "PARTIALLY ORGANIZED": 2,
        "NOT YET ORGANIZED": 1,
    }

    filtered_df["student_attainment_rating"] = filtered_df[
        "student_attainment_rating"
    ].map(attainment_mapping)
    filtered_df["culture_climate_rating"] = filtered_df["culture_climate_rating"].map(
        climate_mapping
    )

    filtered_df["drop_out_rate"] = (
        filtered_df["one_year_dropout_rate_year"]
        + filtered_df["one_year_dropout_rate_year_1"]
    ) / 2
    filtered_df["suspensions_rate"] = (
        filtered_df["suspensions_per_100_students_1"]
        + filtered_df["suspensions_per_100_students_2"]
    ) / 2
    filtered_df.drop(
        [
            "one_year_dropout_rate_year",
            "one_year_dropout_rate_year_1",
            "suspensions_per_100_students_1",
            "suspensions_per_100_students_2",
        ],
        axis=1,
        inplace=True,
    )

    return filtered_df