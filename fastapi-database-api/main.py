from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn

import db

app = FastAPI()
templates = Jinja2Templates(directory='test')
con = db.ConnectionDB(login='test', password='252825', database='test_alg')


@app.get('/', response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse('index.html', context={'request': request})


@app.get('/test_{cont}')
async def main(name: str = None, age: int = None, cont: str = 'test'):
    print(name, age, cont)
    if cont == 'aa':
        return {'messages': age}
    return {'messages': name}


@app.get('/tes')
async def main(name: str = None, age: int = None):
    print(name, age)
    return {'messages': name, 'age': age}


@app.post('/')
async def main_post(command: str = Form(None), dat: int = Form(None)):
    print(command)
    print(dat)
    return {'messages': 'post'}


@app.get('/get_data')
async def get_data():
    return con.get_data_fastapi()

@app.get('/get_all_data')
async def get_all_data():
    try:
        # получаю все данные из таблицы 'people'
        result = con.fetch_all_people()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred: {e}")


@app.get('/get_ten_data')
async def get_ten_data():
    try:
        # получаю первые 10 строк из таблицы 'people'
        result = con.fetch_ten_people()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred: {e}")




@app.post('/search_by_name')
async def search_by_name(name: str = Form(...)):
    try:
        # проверяю, что имя поступает
        print(f"Received name: {name}")
        # выполняю поиск по имени
        result = con.search_by_name(name)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred: {e}")




if __name__ == '__main__':
    uvicorn.run(
        app='main:app',
        host='localhost',
        port=8000,
        workers=2
    )



'''
import requests

data = requests.post(url='http://localhost:8000/', data={'command': '0', 'dat': 1})
print(data.text)


/test/index.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>28.10.24</title>
</head>
<body>
<h1>FastApi</h1>
</body>
</html>

'''