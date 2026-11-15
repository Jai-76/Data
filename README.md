# MNC Workforce Readiness and Wellbeing Dashboard

## 1. Project purpose

This project is a data visualization case study for a multinational company.
It combines employee performance, role readiness, learning activity, workload,
wellbeing risk and internal mobility into one analytical pipeline.

The project uses synthetic data. It does not contain real employee information
and must not be used to make promotion, termination, compensation or hiring
decisions.

## 2. What the project produces

The project creates:

1. A synthetic dataset containing 600 employee records.
2. A Role Readiness Index from 0 to 100.
3. Wellbeing risk bands for aggregate analysis.
4. Four workforce segments based on performance and readiness.
5. Five PNG graph images for a presentation or dashboard.

## 3. Folder structure

```text
data visulation/
|
|-- programs/
|   |-- generate_workforce_data.py
|   `-- analyze_workforce.py
|
|-- data/
|   `-- workforce.csv
|
|-- img/
|   |-- f1_workforce_profile.png
|   |-- f2_correlation_matrix.png
|   |-- f3_performance_readiness_segments.png
|   |-- f4_wellbeing_outcomes.png
|   `-- f5_development_levers.png
|
|-- MNC_Workforce_Readiness_Wellbeing_Analysis.md
`-- README.md
```

## 4. Software requirements

- Python 3.10 or later
- NumPy
- pandas
- Matplotlib

Install the libraries with:

```powershell
python -m pip install numpy pandas matplotlib
```

## 5. How to run

Open PowerShell in the project folder:

```powershell
cd "D:\data visulation"
```

Generate the synthetic workforce data:

```powershell
python programs\generate_workforce_data.py
```

Generate the analysis output and graph images:

```powershell
python programs\analyze_workforce.py
```

The data file is saved in `data\workforce.csv`.
The five graph images are saved in `img`.

## 6. Explanation of the Python files

### `generate_workforce_data.py`

This file creates a reproducible synthetic workforce dataset. It generates:

- Business unit, region and career level
- Tenure
- Performance rating
- Goal attainment
- Quality and delivery scores
- Critical-skill match
- Learning hours
- Certifications
- Stretch assignments
- Collaboration score
- Workload score
- Wellbeing risk score
- Role Readiness Index
- Internal mobility outcome

The random seed is fixed at `2026`, so the same results are produced each time
the file is executed.

### `analyze_workforce.py`

This file reads `data\workforce.csv`, performs the analysis and creates five
visualizations.

It also prints:

- Number of employees
- Average performance
- Average readiness
- Average wellbeing risk
- Internal mobility rate
- Segment-level summary

## 7. Graph explanations

### Figure 1: Workforce profile

Shows the distribution of performance, Role Readiness Index and wellbeing risk
bands.

### Figure 2: Correlation matrix

Shows associations between performance, skills, delivery, learning, workload,
wellbeing risk and readiness. Correlation does not prove causation.

### Figure 3: Performance and readiness segments

Divides employees into four groups:

- High performance and role ready
- High performance and not yet ready
- Developing performance and role ready
- Developing performance and not yet ready

The point colour represents the wellbeing risk score.

### Figure 4: Wellbeing and workforce outcomes

Compares average performance and internal mobility across wellbeing risk bands.

### Figure 5: Development levers

Compares learning-hour quartiles with readiness and internal mobility.

## 8. Suggested presentation explanation

Use the following explanation when presenting the project:

> This project demonstrates how an MNC can combine performance, skills,
> learning and wellbeing indicators in one decision-support dashboard.
> The dashboard helps HR and business leaders identify development needs,
> workforce-readiness gaps and team-level wellbeing signals.
> The data is synthetic, so the results demonstrate the method rather than
> reporting actual employee outcomes.

## 9. Important limitations

- The data is simulated.
- The results are illustrative only.
- Correlation is not causation.
- The Role Readiness Index uses selected weights and must be validated.
- Wellbeing scores are not medical or clinical diagnoses.
- Individual wellbeing information should not be exposed in management reports.
- Small groups should be aggregated to protect employee privacy.
- Human review is required for every real workforce decision.

## 10. Recommended next steps for a real MNC

1. Obtain approval from HR, Legal, Privacy and employee representatives.
2. Replace synthetic fields with approved and validated data sources.
3. Use a validated wellbeing survey instrument.
4. Apply pseudonymization, role-based access and minimum group-size rules.
5. Pilot the dashboard in one or two business units.
6. Test fairness across region, job family, career level and other lawful groups.
7. Review the index weights and thresholds every quarter.

