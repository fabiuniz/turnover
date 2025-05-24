apt-get install libcurl4-openssl-dev
apt install python3 python3-pip python3-venv -y
pip install -r requirements.txt
pip install pandas tensorflow numpy matplotlib seaborn scikit-learn jupyter
#pip install jupyter jupyter notebook
pip install uvicorn
pip install fastapi uvicorn
python3 turnover.py
uvicorn turnover:app --host 0.0.0.0 --port 8000 --reload

docker-compose up --build

# cp *.deb /var/cache/apt/archives; rm *.deb
# . setup_script_launcher.sh
# docker load -i python_3.9-slim.tar
# mkdir -p /home/userlnx/docker/script_docker/turnover
# chmod -R 777 /home/userlnx/docker/script_docker/turnover
# up files turnover
# up files pacotespip
# up file python_3.9-slim.tar
# docker load -i python_3.9-slim.tar; rm python_3.9-slim.tar
# docker-compose up --build
# docker system prune -a --volumes; clear ; docker images;
# docker exec -it turnover_app_1 /bin/bash
# root@6d278194616b:/app/static# mv dados_funcionarios.csv dados_funcionarios_.csv
# docker cp dashboard.py turnover_app_1:/app/dashboard.py 
# docker logs -f turnover_app_1
# docker-compose down
# docker-compose up -d


# which pip
# http://vmlinuxd:8000/predict/
# curl -X POST "http://vmlinuxd:8000/predict/" -H "Content-Type: application/json" -d '{"idade": 35, "salario": 8500, "tempo_empresa": 5, "avaliacao": 4.2}'
# pip download tensorflow -d /home/userlnx/docker/script_docker/relay/
# Backup: pip download -r <(pip freeze) -d /home/userlnx/docker/script_docker/relay
# Backup: pip download dash -d /home/userlnx/docker/script_docker/relay/
# Backup: pip download -r requirements.txt -d /home/userlnx/docker/script_docker/relay/
# restauração: pip install --no-index --find-links=/home/userlnx/docker/script_docker/relay -r requirements.txt
# curl -X POST -H "Content-Type: application/json" -d '{"input": "some_data"}' http://127.0.0.1:8051/api/process_data
# curl http://127.0.0.1:8050/
# ps aux | grep "python.*dashboard.py"
# tail -f your_app.log  # See the latest log entries in real-time grep "ERROR" your_app.log # Find lines containing "ERROR"
# pip download -r requirements.txt -d /home/userlnx/docker/script_docker/relay/
# 
# 
# 
# pip freeze > requirements.txt
# pip download --find-links=/bin/pip -r <(pip freeze) -d /home/userlnx/docker/script_docker/relay/
# 
# pip download dash -d /home/userlnx/docker/script_docker/relay/
# pip download fastapi -d /home/userlnx/docker/script_docker/relay/
# pip download matplotlib -d /home/userlnx/docker/script_docker/relay/
# pip download numpy -d /home/userlnx/docker/script_docker/relay/
# pip download pandas -d /home/userlnx/docker/script_docker/relay/
# pip download plotly -d /home/userlnx/docker/script_docker/relay/
# pip download pydantic -d /home/userlnx/docker/script_docker/relay/
# pip download requests -d /home/userlnx/docker/script_docker/relay/
# pip download scikit -d /home/userlnx/docker/script_docker/relay/
# pip download seaborn -d /home/userlnx/docker/script_docker/relay/
# pip download streamlit -d /home/userlnx/docker/script_docker/relay/
# pip download tensorflow -d /home/userlnx/docker/script_docker/relay/
# pip download uvicorn -d /home/userlnx/docker/script_docker/relay/
# 
# Restaurar pip install --no-index --find-links=/home/userlnx/docker/script_docker/relay/ -r requirements.txt

# pip show dash | awk '/^Version:/ { printf "dash==%s\n", $2 }'
# pip show fastapi | awk '/^Version:/ { printf "fastapi==%s\n", $2 }'
# pip show matplotlib | awk '/^Version:/ { printf "matplotlib==%s\n", $2 }'
# pip show numpy | awk '/^Version:/ { printf "numpy==%s\n", $2 }'
# pip show pandas | awk '/^Version:/ { printf "pandas==%s\n", $2 }'
# pip show plotly | awk '/^Version:/ { printf "plotly==%s\n", $2 }'
# pip show pydantic | awk '/^Version:/ { printf "pydantic==%s\n", $2 }'
# pip show requests | awk '/^Version:/ { printf "requests==%s\n", $2 }'
# pip show scikit-learn | awk '/^Version:/ { printf "scikit-learn==%s\n", $2 }'
# pip show seaborn | awk '/^Version:/ { printf "seaborn==%s\n", $2 }'
# pip show streamlit | awk '/^Version:/ { printf "streamlit==%s\n", $2 }'
# pip show tensorflow | awk '/^Version:/ { printf "tensorflow==%s\n", $2 }'
# pip show uvicorn | awk '/^Version:/ { printf "uvicorn==%s\n", $2 }'