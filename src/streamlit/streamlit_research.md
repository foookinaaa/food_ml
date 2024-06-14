# Streamlit research

### !!! Uncomment fastapi instructions in Dockerfile !!!

local check:
```
export PYTHONPATH='src'
streamlit run src/streamlit/app.py
```
```commandline
docker-compose --project-directory src/streamlit/. up --build
```
http://localhost:8501

![st_demo1](./images/demo1.png)
![st_demo2](./images/demo2.png)
![st_demo3](./images/demo3.png)
