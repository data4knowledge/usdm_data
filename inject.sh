# Valid
python inject.py source_data/protocols/EliLilly_NCT03421379_Diabetes/EliLilly_NCT03421379_Diabetes http://localhost:8000/v4/
python inject.py source_data/protocols/Alexion_NCT04573309_Wilsons/Alexion_NCT04573309_Wilsons http://localhost:8000/v4/
python inject.py source_data/protocols/CDISC_Pilot/CDISC_Pilot_Study http://localhost:8000/v4/
python inject.py source_data/temporary/devices/devices http://localhost:8000/v4/
python inject.py source_data/temporary/observational/observational http://localhost:8000/v4/

# Errors
python inject.py source_data/errors/EliLilly_NCT03421379_Diabetes_Error http://localhost:8000/v4/
python inject.py source_data/errors/CDISC_Pilot_Study_Error http://localhost:8000/v4/
