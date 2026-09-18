import pandas as pd
import numpy as np
from pathlib import Path


# =====================================================
# 1. FILE LOCATIONS
# =====================================================

file_path = Path(
    r"C:\Users\Hooooo\Documents\Excel\MIS_Workforce_Analytics\Cleaned\MIS_Workforce_Cleaned.xlsx"
)

output_folder = Path(
    r"C:\Users\Hooooo\Documents\Excel\MIS_Workforce_Analytics\output"
)

output_folder.mkdir(parents=True, exist_ok=True)


# =====================================================
# 2. LOAD DATASETS
# =====================================================

employee_master = pd.read_excel(
    file_path,
    sheet_name="Employee_Master"
)

productivity = pd.read_excel(
    file_path,
    sheet_name="Productivity"
)

hiring = pd.read_excel(
    file_path,
    sheet_name="Hiring"
)

attrition = pd.read_excel(
    file_path,
    sheet_name="Attrition"
)

print("All forecast datasets loaded successfully")


# =====================================================
# 3. DATE CONVERSION
# =====================================================

employee_master["Date_of_Joining"] = pd.to_datetime(
    employee_master["Date_of_Joining"],
    errors="coerce"
)

employee_master["Exit_Date"] = pd.to_datetime(
    employee_master["Exit_Date"],
    errors="coerce"
)

productivity["Month"] = pd.to_datetime(
    productivity["Month"],
    errors="coerce"
)

hiring["Month"] = pd.to_datetime(
    hiring["Month"],
    errors="coerce"
)

attrition["Exit_Date"] = pd.to_datetime(
    attrition["Exit_Date"],
    errors="coerce"
)


# =====================================================
# 4. NUMERIC CONVERSION
# =====================================================

for column in [
    "Workload_Units",
    "Completed_Units",
    "Productive_Hours",
    "Available_Hours",
    "Quality_Score",
    "Revenue_Contribution"
]:
    productivity[column] = pd.to_numeric(
        productivity[column],
        errors="coerce"
    ).fillna(0)


for column in [
    "Open_Positions",
    "Hires_Completed",
    "Open_Gap",
    "Avg_Time_to_Hire_Days",
    "Offer_Acceptance_Rate"
]:
    hiring[column] = pd.to_numeric(
        hiring[column],
        errors="coerce"
    ).fillna(0)


# =====================================================
# 5. CREATE MONTH LABELS
# =====================================================

productivity["Month_Label"] = (
    productivity["Month"]
    .dt.to_period("M")
    .astype(str)
)

hiring["Month_Label"] = (
    hiring["Month"]
    .dt.to_period("M")
    .astype(str)
)

attrition["Month_Label"] = (
    attrition["Exit_Date"]
    .dt.to_period("M")
    .astype(str)
)


# =====================================================
# 6. HISTORICAL HIRING PERFORMANCE
# =====================================================

hiring_analysis = hiring.groupby(
    ["Department", "Month_Label"]
).agg(
    Open_Positions=("Open_Positions", "sum"),
    Hires_Completed=("Hires_Completed", "sum"),
    Open_Gap=("Open_Gap", "sum"),
    Average_Time_to_Hire_Days=(
        "Avg_Time_to_Hire_Days",
        "mean"
    ),
    Average_Offer_Acceptance_Rate=(
        "Offer_Acceptance_Rate",
        "mean"
    )
).reset_index()

hiring_analysis[
    "Hiring_Completion_Percentage"
] = np.where(
    hiring_analysis["Open_Positions"] > 0,
    (
        hiring_analysis["Hires_Completed"]
        / hiring_analysis["Open_Positions"]
    ) * 100,
    0
)

hiring_analysis[
    "Hiring_Gap_Percentage"
] = np.where(
    hiring_analysis["Open_Positions"] > 0,
    (
        hiring_analysis["Open_Gap"]
        / hiring_analysis["Open_Positions"]
    ) * 100,
    0
)

hiring_analysis[
    [
        "Average_Time_to_Hire_Days",
        "Average_Offer_Acceptance_Rate",
        "Hiring_Completion_Percentage",
        "Hiring_Gap_Percentage"
    ]
] = hiring_analysis[
    [
        "Average_Time_to_Hire_Days",
        "Average_Offer_Acceptance_Rate",
        "Hiring_Completion_Percentage",
        "Hiring_Gap_Percentage"
    ]
].round(2)

hiring_analysis = hiring_analysis.sort_values(
    by=[
        "Month_Label",
        "Department"
    ]
)

print("\nHISTORICAL HIRING PERFORMANCE")
print(hiring_analysis.to_string(index=False))

hiring_analysis.to_csv(
    output_folder /
    "historical_hiring_performance.csv",
    index=False
)


# Department hiring summary
department_hiring_summary = hiring.groupby(
    "Department"
).agg(
    Total_Open_Positions=("Open_Positions", "sum"),
    Total_Hires_Completed=("Hires_Completed", "sum"),
    Total_Open_Gap=("Open_Gap", "sum"),
    Average_Time_to_Hire_Days=(
        "Avg_Time_to_Hire_Days",
        "mean"
    ),
    Average_Offer_Acceptance_Rate=(
        "Offer_Acceptance_Rate",
        "mean"
    )
).reset_index()

department_hiring_summary[
    "Hiring_Completion_Percentage"
] = np.where(
    department_hiring_summary[
        "Total_Open_Positions"
    ] > 0,
    (
        department_hiring_summary[
            "Total_Hires_Completed"
        ]
        / department_hiring_summary[
            "Total_Open_Positions"
        ]
    ) * 100,
    0
)

department_hiring_summary[
    [
        "Average_Time_to_Hire_Days",
        "Average_Offer_Acceptance_Rate",
        "Hiring_Completion_Percentage"
    ]
] = department_hiring_summary[
    [
        "Average_Time_to_Hire_Days",
        "Average_Offer_Acceptance_Rate",
        "Hiring_Completion_Percentage"
    ]
].round(2)

department_hiring_summary = (
    department_hiring_summary.sort_values(
        by="Hiring_Completion_Percentage"
    )
)

department_hiring_summary.to_csv(
    output_folder /
    "department_hiring_summary.csv",
    index=False
)


# =====================================================
# 7. DEPARTMENT MONTHLY PRODUCTIVITY BASE
# =====================================================

department_monthly = productivity.groupby(
    ["Department", "Month"]
).agg(
    Headcount=("Employee_ID", "nunique"),
    Workload_Units=("Workload_Units", "sum"),
    Completed_Units=("Completed_Units", "sum"),
    Productive_Hours=("Productive_Hours", "sum"),
    Available_Hours=("Available_Hours", "sum"),
    Revenue_Contribution=(
        "Revenue_Contribution",
        "sum"
    )
).reset_index()

department_monthly[
    "Productivity_Percentage"
] = np.where(
    department_monthly["Workload_Units"] > 0,
    (
        department_monthly["Completed_Units"]
        / department_monthly["Workload_Units"]
    ) * 100,
    0
)

department_monthly[
    "Capacity_Utilization_Percentage"
] = np.where(
    department_monthly["Available_Hours"] > 0,
    (
        department_monthly["Productive_Hours"]
        / department_monthly["Available_Hours"]
    ) * 100,
    0
)

department_monthly[
    "Workload_Per_Employee"
] = np.where(
    department_monthly["Headcount"] > 0,
    (
        department_monthly["Workload_Units"]
        / department_monthly["Headcount"]
    ),
    0
)

department_monthly[
    "Completed_Units_Per_Employee"
] = np.where(
    department_monthly["Headcount"] > 0,
    (
        department_monthly["Completed_Units"]
        / department_monthly["Headcount"]
    ),
    0
)

department_monthly = department_monthly.sort_values(
    by=[
        "Department",
        "Month"
    ]
)

department_monthly.to_csv(
    output_folder /
    "department_monthly_capacity_base.csv",
    index=False
)


# =====================================================
# 8. THREE-MONTH WORKFORCE FORECAST
# =====================================================

forecast_records = []

latest_historical_month = productivity["Month"].max()

forecast_months = [
    latest_historical_month + pd.DateOffset(months=1),
    latest_historical_month + pd.DateOffset(months=2),
    latest_historical_month + pd.DateOffset(months=3)
]


for department, department_data in department_monthly.groupby(
    "Department"
):

    department_data = department_data.sort_values(
        by="Month"
    ).reset_index(drop=True)

    number_of_months = len(department_data)

    historical_index = np.arange(
        number_of_months
    )

    future_index = np.arange(
        number_of_months,
        number_of_months + 3
    )

    # ---------------------------------------------
    # Workload linear trend
    # ---------------------------------------------

    if number_of_months >= 2:

        workload_slope, workload_intercept = np.polyfit(
            historical_index,
            department_data["Workload_Units"],
            1
        )

        productivity_slope, productivity_intercept = np.polyfit(
            historical_index,
            department_data[
                "Productivity_Percentage"
            ],
            1
        )

        revenue_slope, revenue_intercept = np.polyfit(
            historical_index,
            department_data[
                "Revenue_Contribution"
            ],
            1
        )

        workload_forecast = (
            workload_slope * future_index
            + workload_intercept
        )

        productivity_forecast = (
            productivity_slope * future_index
            + productivity_intercept
        )

        revenue_forecast = (
            revenue_slope * future_index
            + revenue_intercept
        )

    else:

        workload_forecast = np.repeat(
            department_data[
                "Workload_Units"
            ].iloc[-1],
            3
        )

        productivity_forecast = np.repeat(
            department_data[
                "Productivity_Percentage"
            ].iloc[-1],
            3
        )

        revenue_forecast = np.repeat(
            department_data[
                "Revenue_Contribution"
            ].iloc[-1],
            3
        )

    # Prevent invalid negative forecast
    workload_forecast = np.maximum(
        workload_forecast,
        0
    )

    revenue_forecast = np.maximum(
        revenue_forecast,
        0
    )

    # Keep productivity within realistic limits
    productivity_forecast = np.clip(
        productivity_forecast,
        50,
        100
    )

    # Latest month-end active employee headcount
    forecast_month_end = (
        latest_historical_month
        + pd.offsets.MonthEnd(0)
    )

    department_mask = (
        employee_master["Department"] == department
    )

    joined_mask = (
        employee_master["Date_of_Joining"]
        <= forecast_month_end
    )

    not_exited_mask = (
        employee_master["Exit_Date"].isna()
        |
        (
            employee_master["Exit_Date"]
            > forecast_month_end
        )
    )

    current_headcount = employee_master.loc[
        department_mask
        & joined_mask
        & not_exited_mask,
        "Employee_ID"
    ].nunique()

    # Recent 3-month workload capacity per employee
    recent_data = department_data.tail(3)

    average_workload_per_employee = (
        recent_data[
            "Workload_Per_Employee"
        ].mean()
    )

    average_capacity_utilization = (
        recent_data[
            "Capacity_Utilization_Percentage"
        ].mean()
    )

    for index, forecast_month in enumerate(
        forecast_months
    ):

        forecast_workload = float(
            workload_forecast[index]
        )

        forecast_productivity = float(
            productivity_forecast[index]
        )

        forecast_revenue = float(
            revenue_forecast[index]
        )

        # Productive output capacity per employee
        productive_capacity_per_employee = (
            average_workload_per_employee
            * (
                forecast_productivity / 100
            )
        )

        if productive_capacity_per_employee > 0:

            exact_required_headcount = (
                forecast_workload
                / productive_capacity_per_employee
            )

            required_headcount = int(
                np.ceil(exact_required_headcount)
            )

        else:

            exact_required_headcount = 0
            required_headcount = 0

        headcount_gap = (
            required_headcount
            - current_headcount
        )

        recommended_hires = max(
            headcount_gap,
            0
        )

        excess_headcount = max(
            current_headcount
            - required_headcount,
            0
        )

        available_output_capacity = (
            current_headcount
            * productive_capacity_per_employee
        )

        if available_output_capacity > 0:

            forecast_capacity_utilization = (
                forecast_workload
                / available_output_capacity
            ) * 100

        else:

            forecast_capacity_utilization = 0

        expected_completed_units = min(
            forecast_workload,
            available_output_capacity
        )

        workload_shortfall = max(
            forecast_workload
            - available_output_capacity,
            0
        )

        if forecast_capacity_utilization > 100:

            capacity_status = "Under-Capacity"

        elif forecast_capacity_utilization < 70:

            capacity_status = "Over-Capacity"

        elif forecast_capacity_utilization < 85:

            capacity_status = "Available Capacity"

        else:

            capacity_status = "Balanced Capacity"

        forecast_records.append({
            "Forecast_Month":
                forecast_month.strftime("%Y-%m"),

            "Department":
                department,

            "Current_Headcount":
                current_headcount,

            "Forecast_Workload_Units":
                round(forecast_workload, 2),

            "Forecast_Productivity_Percentage":
                round(forecast_productivity, 2),

            "Average_Workload_Per_Employee":
                round(
                    average_workload_per_employee,
                    2
                ),

            "Productive_Capacity_Per_Employee":
                round(
                    productive_capacity_per_employee,
                    2
                ),

            "Exact_Required_Headcount":
                round(
                    exact_required_headcount,
                    2
                ),

            "Required_Headcount":
                required_headcount,

            "Headcount_Gap":
                headcount_gap,

            "Recommended_Hires":
                recommended_hires,

            "Excess_Headcount":
                excess_headcount,

            "Forecast_Capacity_Utilization_Percentage":
                round(
                    forecast_capacity_utilization,
                    2
                ),

            "Expected_Completed_Units":
                round(
                    expected_completed_units,
                    2
                ),

            "Workload_Shortfall_Units":
                round(
                    workload_shortfall,
                    2
                ),

            "Forecast_Revenue_Contribution":
                round(
                    forecast_revenue,
                    2
                ),

            "Recent_Average_Capacity_Utilization":
                round(
                    average_capacity_utilization,
                    2
                ),

            "Capacity_Status":
                capacity_status
        })


workforce_forecast = pd.DataFrame(
    forecast_records
)

workforce_forecast = workforce_forecast.sort_values(
    by=[
        "Forecast_Month",
        "Recommended_Hires",
        "Department"
    ],
    ascending=[
        True,
        False,
        True
    ]
)

print("\nTHREE-MONTH WORKFORCE CAPACITY FORECAST")
print(workforce_forecast.to_string(index=False))

workforce_forecast.to_csv(
    output_folder /
    "three_month_workforce_capacity_forecast.csv",
    index=False
)


# =====================================================
# 9. MONTHLY HIRING REQUIREMENT
# =====================================================

monthly_hiring_requirement = workforce_forecast.groupby(
    "Forecast_Month"
).agg(
    Current_Headcount=(
        "Current_Headcount",
        "sum"
    ),
    Required_Headcount=(
        "Required_Headcount",
        "sum"
    ),
    Recommended_Hires=(
        "Recommended_Hires",
        "sum"
    ),
    Excess_Headcount=(
        "Excess_Headcount",
        "sum"
    ),
    Forecast_Workload_Units=(
        "Forecast_Workload_Units",
        "sum"
    ),
    Expected_Completed_Units=(
        "Expected_Completed_Units",
        "sum"
    ),
    Workload_Shortfall_Units=(
        "Workload_Shortfall_Units",
        "sum"
    ),
    Forecast_Revenue_Contribution=(
        "Forecast_Revenue_Contribution",
        "sum"
    )
).reset_index()

monthly_hiring_requirement[
    "Overall_Forecast_Productivity_Percentage"
] = np.where(
    monthly_hiring_requirement[
        "Forecast_Workload_Units"
    ] > 0,
    (
        monthly_hiring_requirement[
            "Expected_Completed_Units"
        ]
        / monthly_hiring_requirement[
            "Forecast_Workload_Units"
        ]
    ) * 100,
    0
)

monthly_hiring_requirement[
    [
        "Forecast_Workload_Units",
        "Expected_Completed_Units",
        "Workload_Shortfall_Units",
        "Forecast_Revenue_Contribution",
        "Overall_Forecast_Productivity_Percentage"
    ]
] = monthly_hiring_requirement[
    [
        "Forecast_Workload_Units",
        "Expected_Completed_Units",
        "Workload_Shortfall_Units",
        "Forecast_Revenue_Contribution",
        "Overall_Forecast_Productivity_Percentage"
    ]
].round(2)

print("\nMONTHLY HIRING REQUIREMENT")
print(monthly_hiring_requirement.to_string(index=False))

monthly_hiring_requirement.to_csv(
    output_folder /
    "monthly_hiring_requirement.csv",
    index=False
)


# =====================================================
# 10. DEPARTMENT HIRING REQUIREMENT
# Maximum requirement across 3 forecast months
# =====================================================

department_hiring_requirement = workforce_forecast.groupby(
    "Department"
).agg(
    Current_Headcount=(
        "Current_Headcount",
        "max"
    ),
    Maximum_Required_Headcount=(
        "Required_Headcount",
        "max"
    ),
    Maximum_Recommended_Hires=(
        "Recommended_Hires",
        "max"
    ),
    Maximum_Excess_Headcount=(
        "Excess_Headcount",
        "max"
    ),
    Average_Forecast_Productivity=(
        "Forecast_Productivity_Percentage",
        "mean"
    ),
    Average_Forecast_Capacity_Utilization=(
        "Forecast_Capacity_Utilization_Percentage",
        "mean"
    ),
    Total_Forecast_Workload=(
        "Forecast_Workload_Units",
        "sum"
    ),
    Total_Workload_Shortfall=(
        "Workload_Shortfall_Units",
        "sum"
    )
).reset_index()

department_hiring_requirement[
    [
        "Average_Forecast_Productivity",
        "Average_Forecast_Capacity_Utilization",
        "Total_Forecast_Workload",
        "Total_Workload_Shortfall"
    ]
] = department_hiring_requirement[
    [
        "Average_Forecast_Productivity",
        "Average_Forecast_Capacity_Utilization",
        "Total_Forecast_Workload",
        "Total_Workload_Shortfall"
    ]
].round(2)

department_hiring_requirement[
    "Department_Capacity_Status"
] = np.select(
    [
        department_hiring_requirement[
            "Maximum_Recommended_Hires"
        ] > 0,

        department_hiring_requirement[
            "Average_Forecast_Capacity_Utilization"
        ] < 70,

        department_hiring_requirement[
            "Average_Forecast_Capacity_Utilization"
        ] < 85
    ],
    [
        "Under-Capacity",
        "Over-Capacity",
        "Available Capacity"
    ],
    default="Balanced Capacity"
)

department_hiring_requirement = (
    department_hiring_requirement.sort_values(
        by="Maximum_Recommended_Hires",
        ascending=False
    )
)

print("\nDEPARTMENT HIRING REQUIREMENT")
print(
    department_hiring_requirement.to_string(
        index=False
    )
)

department_hiring_requirement.to_csv(
    output_folder /
    "department_hiring_requirement.csv",
    index=False
)


# =====================================================
# 11. FORECAST EXCEPTION REPORT
# =====================================================

forecast_exceptions = workforce_forecast[
    (
        workforce_forecast["Recommended_Hires"] > 0
    )
    |
    (
        workforce_forecast[
            "Forecast_Productivity_Percentage"
        ] < 80
    )
    |
    (
        workforce_forecast[
            "Forecast_Capacity_Utilization_Percentage"
        ] > 100
    )
    |
    (
        workforce_forecast[
            "Workload_Shortfall_Units"
        ] > 0
    )
].copy()


def forecast_exception_reason(row):

    reasons = []

    if row["Recommended_Hires"] > 0:
        reasons.append(
            "Hiring Required"
        )

    if (
        row["Forecast_Productivity_Percentage"]
        < 80
    ):
        reasons.append(
            "Low Forecast Productivity"
        )

    if (
        row[
            "Forecast_Capacity_Utilization_Percentage"
        ] > 100
    ):
        reasons.append(
            "Workforce Under-Capacity"
        )

    if row["Workload_Shortfall_Units"] > 0:
        reasons.append(
            "Expected Workload Shortfall"
        )

    if len(reasons) == 0:
        return "No Exception"

    return ", ".join(reasons)


forecast_exceptions[
    "Exception_Reason"
] = forecast_exceptions.apply(
    forecast_exception_reason,
    axis=1
)


def forecast_priority(row):

    if (
        row["Recommended_Hires"] >= 3
        or
        row[
            "Forecast_Capacity_Utilization_Percentage"
        ] >= 120
    ):
        return "Critical"

    elif (
        row["Recommended_Hires"] >= 1
        or
        row[
            "Forecast_Productivity_Percentage"
        ] < 75
    ):
        return "High"

    else:
        return "Medium"


forecast_exceptions[
    "Exception_Priority"
] = forecast_exceptions.apply(
    forecast_priority,
    axis=1
)

priority_order = {
    "Critical": 1,
    "High": 2,
    "Medium": 3
}

forecast_exceptions[
    "Priority_Order"
] = forecast_exceptions[
    "Exception_Priority"
].map(priority_order)

forecast_exceptions = forecast_exceptions.sort_values(
    by=[
        "Priority_Order",
        "Forecast_Month",
        "Recommended_Hires"
    ],
    ascending=[
        True,
        True,
        False
    ]
)

forecast_exceptions = forecast_exceptions.drop(
    columns=["Priority_Order"]
)

print("\nFORECAST EXCEPTION REPORT")
print("Total exceptions:", len(forecast_exceptions))

if forecast_exceptions.empty:
    print("No forecast exceptions identified")
else:
    print(forecast_exceptions.to_string(index=False))

forecast_exceptions.to_csv(
    output_folder /
    "forecast_exception_report.csv",
    index=False
)


# =====================================================
# 12. MANAGEMENT FORECAST SUMMARY
# =====================================================

total_departments = workforce_forecast[
    "Department"
].nunique()

under_capacity_departments = (
    department_hiring_requirement[
        department_hiring_requirement[
            "Department_Capacity_Status"
        ]
        ==
        "Under-Capacity"
    ]["Department"].nunique()
)

over_capacity_departments = (
    department_hiring_requirement[
        department_hiring_requirement[
            "Department_Capacity_Status"
        ]
        ==
        "Over-Capacity"
    ]["Department"].nunique()
)

balanced_departments = (
    department_hiring_requirement[
        department_hiring_requirement[
            "Department_Capacity_Status"
        ].isin([
            "Balanced Capacity",
            "Available Capacity"
        ])
    ]["Department"].nunique()
)

maximum_monthly_hires = (
    monthly_hiring_requirement[
        "Recommended_Hires"
    ].max()
)

total_forecast_shortfall = (
    workforce_forecast[
        "Workload_Shortfall_Units"
    ].sum()
)

average_forecast_productivity = (
    workforce_forecast[
        "Forecast_Productivity_Percentage"
    ].mean()
)

forecast_summary = pd.DataFrame({
    "Metric": [
        "Forecast Start Month",
        "Forecast End Month",
        "Departments Analyzed",
        "Under-Capacity Departments",
        "Over-Capacity Departments",
        "Balanced or Available Capacity Departments",
        "Maximum Monthly Hiring Requirement",
        "Total Forecast Workload Shortfall",
        "Average Forecast Productivity",
        "Total Forecast Exceptions"
    ],
    "Value": [
        forecast_months[0].strftime("%Y-%m"),
        forecast_months[-1].strftime("%Y-%m"),
        total_departments,
        under_capacity_departments,
        over_capacity_departments,
        balanced_departments,
        maximum_monthly_hires,
        round(total_forecast_shortfall, 2),
        round(average_forecast_productivity, 2),
        len(forecast_exceptions)
    ]
})

print("\nMANAGEMENT FORECAST SUMMARY")
print(forecast_summary.to_string(index=False))

forecast_summary.to_csv(
    output_folder /
    "management_forecast_summary.csv",
    index=False
)


# =====================================================
# 13. COMPLETION MESSAGE
# =====================================================

print("\n=====================================================")
print("WORKFORCE FORECAST COMPLETED SUCCESSFULLY")
print("=====================================================")

print("\nOutput location:")
print(output_folder)