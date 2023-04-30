### TODOs
- Load interest rate data from US, UK, AUS (Later add CAN and NZD)
- Move into Azure blob storage using PySpark & Airflow !*****!
- Clean and transform datasets
- Build multi-ouput GPs models to predict interest rates
- Visualisation: => Move into S3
- Data and Model monitoring


```
%%time
with model:
    gp_trace = pm.sample(1000, chains=1)
```

Sample with nutpie for faster speed.
```
%%time
import nutpie
compiled_model = nutpie.compile_pymc_model(model)
gp_trace = nutpie.sample(compiled_model, draws=1000, chains=1)
```

Convert panel to app for visualisation on Github
```
panel convert app.py --to pyodide-worker --out ../docs/app
```