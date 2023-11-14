from app import app

@app.get('/')
@app.get('/attendence/')
def hello():
    data = {'hello': 'world'}
    return data