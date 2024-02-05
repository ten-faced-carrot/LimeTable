alias python=python3
python -m venv venv
./venv/bin/python -m pip install -r requirements.txt --break-system-packages
./venv/bin/python main.py