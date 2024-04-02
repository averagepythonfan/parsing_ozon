## Парсер отзывов Ozon

Данный репозитории реализовывает скрипт позволяющий парсить фото-отзывы на Ozon.
Так же есть реализация детектора Yolos-Tiny, который позволяет распознавать на фото людей.


## Предустановки:
Чтобы запустить проект вам понадобиться:
1. установленный git, (официальный сайт)[https://git-scm.com/]
2. python версии 3.10 и выше, (сайт)[https://www.python.org/]
3. затем вам нужна библиотека poetry, после установки python можно воспользоваться командой `pip install poetry`, или перейти по (ссылке)[https://python-poetry.org/docs/]
4. docker и docker compose, установка для (Windows)[https://docs.docker.com/desktop/install/windows-install/]


## Ozon Reviews Parser

 - Prerequirements: python 3.10, poetry (pip install poetry)

1. git clone https://github.com/averagepythonfan/parsing_ozon.git
2. poetry install --no-root --only play
3. poetry run playwright install firefox
3. python3 async_parse.py {article}
4. parsed reviews in "result.json", scheme {"HASH": "LINK"}


## ML Model Workflow

- Prerequirements: docker, docker compose

1. docker compose build detector
2. create ".env" file, and enter token: "TOKEN=YOUR_TOKEN"
3. docker compose up detector -d
4. may launch  "http://localhost:9090/docs"
5. make a request:

### Code example:
```Python
import requests

params = {
    "user_id": "your_id", #might get from tg: https://t.me/getmyid_bot
    "images": [
        "https://sun9-50.userapi.com/impg/L7DtKyCbFQlSpdj0VDNaekK1KQcCGivnNEIQTA/2P2P0KFx3gM.jpg?size=2048x1536&quality=95&sign=ebac9dc1cd9d0b4ad8fb11f94adec62b&type=album",
        "https://sun9-43.userapi.com/impg/SpBoRQrcVzFaXGQrc49kGWAVaEPQplONnHzDKg/0N5XxkKO-ZQ.jpg?size=1432x2160&quality=95&sign=b3ed0acd37c240c1b65ca28897cc1e52&type=album",
        "https://sun7-23.userapi.com/impg/hDtiP3Yzn-YtqUvzspLUb610UTw3VI8qU9VavQ/LT2NW9f7Y3Y.jpg?size=1440x1798&quality=96&sign=11cacb25161a97c64fa6f0ad363db4df&type=album",
        "https://sun9-40.userapi.com/impg/nFrZFwYeDeUHfTk6GBMrub5VV2bZqShLXVLZPg/b53SMXoLsG4.jpg?size=1316x1200&quality=95&sign=146c0e568d1492a3ef056f5282fa879c&type=album",
        "https://sun7-17.userapi.com/impf/N9ZbnzcaFYE8z9_e9BzHNmfvUKRS0EIUKFJbAg/ycKcvHDicuY.jpg?size=1080x1350&quality=95&sign=3329459c6ff8932f442f7b0a1b9b7dff&type=album"
    ]
}


response = requests.post("http://localhost:9090/model/detect", json=params)

```

## Jupyter Lab Workflow:

1. poetry install --no-root --with dev,play
2. poetry run playwright install firefox
3. poetry run playwright install-deps
4. poetry run jupyter lab
5. open "local_run.ipynb"
