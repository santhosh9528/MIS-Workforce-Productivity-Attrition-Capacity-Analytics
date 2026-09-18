# Workforce Productivity, Attrition & Capacity Planning Analytics

An end-to-end workforce analytics and Management Information System (MIS) project developed using Excel, Python, Pandas, Power BI and DAX.

The solution evaluates workforce productivity, attendance, overtime, attrition, employee capacity and hiring requirements from January 2026 to August 2026, with a three-month forecast for September–November 2026.

## Business Objective

The objective of this project is to determine whether the organization has the right workforce capacity and to identify productivity, employee-retention and operational risks.

The analysis covers:

- Employee headcount, active employees, new joiners and exits
- Attrition, absenteeism and leave utilization
- Overtime and its relationship with productivity
- Productivity by department, location, designation, experience, manager, team and month
- Departments where headcount increased while productivity declined
- Employees and teams with consistently declining productivity
- Workforce capacity utilization
- Department-level workforce risk
- Monthly hiring requirements
- Three-month workforce capacity forecast
- Management exceptions and recommended actions

## Tools and Technologies

- Microsoft Excel
- Python
- Pandas
- NumPy
- Power BI
- Power Query
- DAX
- Git
- GitHub

## Dataset

The project integrates the following workforce datasets:

- Employee Master
- Attendance
- Leave
- Overtime
- Productivity
- Performance
- Hiring
- Attrition

All major KPIs can be traced back to the underlying employee-level or transaction-level data.

## Executive KPI Summary

| KPI | Result |
|---|---:|
| Total Employees | 80 |
| Active Employees | 72 |
| Opening Headcount | 68 |
| New Joiners | 12 |
| Employee Exits | 8 |
| Average Headcount | 70 |
| Attrition Rate | 11.43% |
| Absenteeism Rate | 3.97% |
| Hour-Based Absenteeism Rate | 6.37% |
| Leave Utilization Rate | 47.19% |
| Total Overtime Hours | 3,727.64 |
| Total Workload Units | 65,248 |
| Completed Units | 54,999 |
| Overall Productivity | 84.29% |
| Capacity Utilization | 87.28% |
| Revenue Contribution | 2,277,417.31 |
| Maximum Monthly Hiring Requirement | 63 |
| Forecast Workload Shortfall | 10,278.37 units |

## Key Findings

- Monthly productivity declined from 91.20% in January to 78.10% in August, a decrease of 13.10 percentage points.
- Operations was classified as a critical-risk department because of low productivity, high overtime and high attrition.
- Sales recorded declining productivity and a 25% attrition rate.
- Customer Support recorded the highest absenteeism and overtime exposure.
- The relationship between overtime and productivity was weak and negative, indicating that additional overtime did not consistently improve output.
- Employees with 0–1 year of experience recorded 74.98% productivity, compared with 86.19% for employees with more than one year of experience.
- All eight departments were forecast to face capacity pressure if recent workload and productivity trends continued.
- The forecast estimated additional capacity requirements of 43 FTEs in September, 51 in October and 63 in November.
- A total of 154 management exceptions were identified, including 17 critical, 45 high and 92 medium-priority exceptions.

## Management Recommendations

1. Perform an immediate root-cause review of Operations productivity and workload allocation.
2. Review Sales targets, productivity barriers and employee-retention drivers.
3. Reduce overtime that does not result in higher completed output.
4. Improve Customer Support scheduling and leave coverage.
5. Introduce structured 30-, 60- and 90-day monitoring for new joiners.
6. Improve productivity and redistribute workload before approving the full forecast hiring requirement.
7. Use phased hiring based on operational priority and actual workload requirements.
8. Review productivity, capacity, absenteeism, overtime and attrition every month.

## Power BI Dashboard

The Power BI report contains six interactive pages:

1. Executive Overview
2. Productivity Analysis
3. Attendance & Overtime
4. Attrition Analysis
5. Capacity & Hiring Forecast
6. Management Exceptions

### Executive Overview

![Executive Overview](Power%20Bi/Dashboards%20screenshot/Executive%20Overview.png)

### Productivity Analysis

![Productivity Analysis](Power%20Bi/Dashboards%20screenshot/Productivity%20Analysis.png)

### Attendance & Overtime

![Attendance and Overtime](Power%20Bi/Dashboards%20screenshot/Attendance%20%26%20Overtime.png)

### Attrition Analysis

![Attrition Analysis](Power%20Bi/Dashboards%20screenshot/Attrition%20Analysis.png)

### Capacity & Hiring Forecast

![Capacity and Hiring Forecast](Power%20Bi/Dashboards%20screenshot/Capacity%20%26%20Hiring%20Forecast.png)

### Management Exceptions

![Management Exceptions](Power%20Bi/Dashboards%20screenshot/Management%20Exceptions.png)

## Project Structure

```text
MIS_Workforce_Analytics/
│
├── Dataset/
│   └── MIS_Workforce_Productivity_Attrition_Capacity_Dataset.xlsx
│
├── Cleaned/
│   └── MIS_Workforce_Cleaned.xlsx
│
├── Analysis/
│   └── MIS_Workforce_KPI_Calculations.xlsx
│
├── Python/
│   ├── cleaning.py
│   ├── kpi_calculation.py
│   ├── productivity_analysis.py
│   ├── workforce_risk_analysis.py
│   ├── workforce_forecast.py
│   └── final_management_report.py
│
├── Power Bi/
│   ├── Dashboards.pbix
│   └── Dashboards screenshot/
│
├── Calculation Sheet/
├── Reconciliation Report/
├── Exception Report/
├── Executive Summary/
├── Findings & Recommendations/
├── Workforce Forecast/
├── output/
└── README.md
```

## Python Workflow

Run the Python scripts in the following order:

```powershell
py cleaning.py
py kpi_calculation.py
py productivity_analysis.py
py workforce_risk_analysis.py
py workforce_forecast.py
py final_management_report.py
```

The scripts perform the following activities:

1. Clean and validate the source datasets.
2. Generate reconciliation and data-quality reports.
3. Calculate workforce KPIs.
4. Analyze productivity across multiple workforce dimensions.
5. Analyze attendance, leave, overtime and attrition risks.
6. Identify declining employee and team productivity.
7. Generate a three-month capacity and hiring forecast.
8. Create the consolidated exception report and executive summary.

## Final Deliverables

- Cleaned workforce dataset
- KPI calculation workbook
- Reconciliation report
- Six-page Power BI dashboard
- Three-month workforce capacity forecast
- Consolidated management exception report
- Executive summary
- Key findings and management recommendations
- Reproducible Python analysis scripts

## Business Value

This project enables management to:

- Monitor workforce performance through traceable KPIs
- Identify departments with productivity and retention risks
- Understand whether overtime is improving output
- Detect under-capacity and over-capacity conditions
- Estimate future workforce requirements
- Prioritize high-impact management exceptions
- Make data-driven workforce planning decisions

## Author

**Santhosh Kumar M**  
Data Analyst Intern  
Madurai, Tamilnadu, India

**GitHub:** [github.com/santhosh9528](https://github.com/santhosh9528)

## Disclaimer

This project uses a simulated workforce dataset created for analytics practice and portfolio demonstration. The results do not represent confidential information from a real organization.
