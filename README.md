## Ozon Reviews Parser

 - Prerequirements: python 3.10, poetry (pip install poetry)

1. git clone https://github.com/averagepythonfan/parsing_ozon.git
2. poetry install --no-root --only play
3. python3 async_parse.py {article}
4. parsed reviews in "result.json", scheme {"HASH": "LINK"}
