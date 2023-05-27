# Tapio Techincal Test.

#### I will try to implement clean architecture in this project.
- Develop a feature and the DB architecture to support it from the already existing
models and components of the platform. The approximative design of what the front end
would look like is provided.
## Requirements
Create a projection tool to allow our experts to design reduction strategies for our
clients. The usual carbon report would have several sources attached to it. The tool
would allow to register potential modification to those sources.
Implementation should:
- include additional/modified models
- include endpoints (DRF) for specific data
- be implemented using the Django framework
- pay extra care to optimization
## Specifications
- Allow to plan a modification to a source (either by applying a ratio to the
value or changing the emission_factor (EF) value)
- Modifications could be in series e.g. I first reduce my value by 2 then I
change the EF from 42 to 3.14 (switch from diesel to electric let's say)
- Provide information regarding the delta in total_emission regarding the source
- Provide information regarding the delta in total_emission for the report
- For source s with lifetime s (capital goods) the amortization should be
considered:
total_emission are divided along the lifetime of the source
after lifetime years the total_emission displaied is 0
making a modification on a source with lifetime means that the
original source could already be amortized 
> e.g. bought 1 car (lifetime
5 years) in 2020, if I buy another one in 2022 (with a modification)
both will be showed in the total emissions displaied for my
modification. If it's in 2028, only the second one will be showed
- When retrieving an information (by source or report ) we should be able to
specify a year (attention to lifetime )
- We should be able to retrieve data for a range of years (by source or report )
within a dict with the year as a key and the emissions as a value
## Bonus
- We could have several reduction strategies by report
- New source could be added in reduction strategies
- Modifications could be progressive, the growth should be partially showed when the year fits the time the growth started. e.g. I'll double my source by 2024
- Script to generate a dummy DB


## Bugs to fix

- [ ] Fix the bug in `total_emission` 
- > The total emission is not calculated correctly when the source is modified.
  > 
## Routes, Body and Response


### Create a new report

- **Route:** `/api/v1/reports/`
- **Method:** `POST`
- **Body:**
```json
{
    "name": "string",
    "date": "Date (mm/dd/yyyy)"  
}
```
- **Response:**
```json
{
    "id": 1,
    "message": "Report created successfully",
    "data": {
        "name": "string",
        "date": "2023-11-03"
    }
}
```

### Get all reports

- **Route:** `/api/v1/reports/`
- **Method:** `GET`
- **Query Params:** `?year=2023` or `?from_year=2023&to_year=2024`
- **Response:**
```json
{
    "details" : "Reports from {year} to {year}",
    "data": [
        {
            "id": 1,
            "name": "string",
            "date": "2023-11-03"
        },
        {
            "id": 2,
            "name": "string",
            "date": "2023-11-03"
        }
    ]
}
```

### Get a report by id

- **Route:** `/api/v1/reports/{id}/`
- **Method:** `GET`
- **Response:**
```json
{
    "total_emission_report": 140.0,
    "data": {
        "id": 2,
        "name": "Unity",
        "date": "2023-05-30",
        "sources": [
            {
                "id": 10,
                "description": "Description for Australia",
                "value": 10.0,
                "emission_factor": 5.0,
                "total_emission": 80.0,
                "lifetime": 10,
                "acquisition_year": 2020,
                "report": {
                    "id": 2,
                    "name": "Unity",
                    "date": "2023-05-30"
                }
            },
            {
                "id": 17,
                "description": "Description for France",
                "value": 10.0,
                "emission_factor": 6.0,
                "total_emission": 60.0,
                "lifetime": 7,
                "acquisition_year": 2021,
                "report": {
                    "id": 2,
                    "name": "Unity",
                    "date": "2023-05-30"
                }
            }
        ]
    }
}
```

### Update a report by id

- **Route:** `/api/v1/reports/{id}/`
- **Method:** `PUT`
- **Body:**
```json
{
    "name": "string",
    "date": "Date (mm-dd-yyyy)"  
}
```

- **Response:**
```json
{
    "id": 2,
    "name": "string",
    "date": "2023-05-30"
}
```

### Delete a report by id

- **Route:** `/api/v1/reports/{id}/`
- **Method:** `DELETE`
- **Response:**
```json
{
    "message": "Report deleted successfully"
}
```

### Create a new source

- **Route:** `/api/v1/reports/sources/`
- **Method:** `POST`
- **Body:**
```json
{
    "description": "string",
    "value": 0,
    "emission_factor": 0,
    "lifetime": 0,
    "acquisition_year": 0,
    "report": "Report ID"
}
```

- **Response:**
```json
{
    "data": {
        "description": "string",
        "value": 2.0,
        "emission_factor": 5.0,
        "lifetime": 9,
        "acquisition_year": 2020,
        "report": 2
    },
    "emission_with_calcul": 10.0,
    "emission_without_calcul": 10.0,
    "formula": "value * emission_factor",
    "id": 25
}
```

### Get all sources

- **Route:** `/api/v1/reports/sources/`
- **Method:** `GET`
- **Query Params:** `?year=2023` or `?from_year=2023&to_year=2024`
- **Response:**
```json
{
    "details" : "Sources from {year} to {year}",
    "data": [
        {
            "id": 1,
            "description": "string",
            "value": 2.0,
            "emission_factor": 5.0,
            "total_emission": 10.0,
            "lifetime": 9,
            "acquisition_year": 2020,
            "report": 2
        },
        {
            "id": 2,
            "description": "string",
            "value": 2.0,
            "emission_factor": 5.0,
            "total_emission": 10.0,
            "lifetime": 9,
            "acquisition_year": 2020,
            "report": 2
        }
    ]
}
```

### Get a source by id

- **Route:** `/api/v1/reports/sources/{id}/`
- **Method:** `GET`
- **Response:**
```json
{
    "id": 1,
    "description": "string",
    "value": 2.0,
    "emission_factor": 5.0,
    "total_emission": 10.0,
    "lifetime": 9,
    "acquisition_year": 2020,
    "report": {
        "id": 2,
        "name": "string",
        "date": "2023-05-30"
    }
}
```

### Update a source by id

- **Route:** `/api/v1/reports/sources/{id}/`
- **Method:** `PUT`
- **Body:**
```json
{
    "description": "string",
    "value": 0,
    "emission_factor": 0,
    "lifetime": 0,
    "acquisition_year": 0,
    "report": "Report ID"
}
```

- **Response:**
```json

{
    "id": 1,
    "description": "string",
    "value": 2.0,
    "emission_factor": 5.0,
    "total_emission": 10.0,
    "lifetime": 9,
    "acquisition_year": 2020,
    "report": 2
}
```

### Delete a source by id

- **Route:** `/api/v1/reports/sources/{id}/`
- **Method:** `DELETE`
- **Response:**
```json
{
    "message": "Source deleted successfully"
}
```

### Get all emission factors