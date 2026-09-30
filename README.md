# Employee Management Application 

## Structure
```
employee_management/
├── main.py                     # entry point (menu / application flow)
└── employee_app/               # package
    ├── __init__.py             # package init, exports Employee & EmployeeService
    ├── models.py               # Employee model            (Member 1)
    ├── utils.py                # validation & helpers      (Member 1)
    └── employee_service.py     # CRUD business logic       (Member 2)
```

## Run
```
python main.py
```
Requires Python 3.7+ (no external libraries).


## Import flow
`main.py` -> `employee_app` (`__init__`) -> `employee_service` -> `models`, `utils`
