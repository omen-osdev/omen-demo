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
> If the Flask app crashes, the running containers will not be automatically terminated.<br />
> To manually terminate a container, run:<br />
> ```docker ps``` to get the container ID, then<br />
> ```docker kill <container_id>```. to immediately stop the container.
