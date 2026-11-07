set shell := ["powershell.exe", "-Command"] # Windows
# set shell := ["bash", "-c"] # Linux/Mac
# uv run --python 3.10 pytest

test:
    uv run --group test pytest -vs

test-scraper:
    uv run --group test pytest tests/test_mef_scraper.py

test-utils:
    uv run --group test pytest tests/test_utils.py
    
    