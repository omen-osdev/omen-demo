# Omen Demo
Give [Omen](https://github.com/omen-osdev/omen) a try, right inside your browser!

## Getting Started

> [!TIP]
> We strongly recommend using a virtual environment to run the demo. </br>
> For Linux run:<br />```python3 -m venv .venv``` and then ```source .venv/bin/activate```.<br />
> For Windows run:<br/>```virtualenv .venv``` and then ```.venv\Scripts\activate```.


#### Install the necessary packages:
```bash
pip install -r requirements.txt
```

#### Running in development mode:
```bash
flask --app app run --debug --no-reload
```

> [!WARNING]
> The app will automatically destroy Docker containers after the set INSTANCE_LIMIT time is reached.<br />
> However, if the Flask app crashes or is manually stopped (e.g., via Ctrl+C) before that time, the running containers will not be automatically terminated.<br />
> Closing the browser tab does not stop the container, as the session persists for the duration of `INSTANCE_LIMIT` (e.g., 1 minute).<br />
> To manually terminate a container, run:<br />
> ```docker ps``` to get the container ID, then<br />
> ```docker kill <container_id>```. to immediately stop the container.
