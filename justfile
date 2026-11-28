set shell := ["powershell.exe", "-Command"] # Windows
# set shell := ["bash", "-c"] # Linux/Mac
# uv run --python 3.10 pytest

test:
    uv run --group test pytest -vs

test-functional:
    uv run --group test pytest tests/functional

test-integration:
    uv run --group test pytest tests/integration
    
    