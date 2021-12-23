from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse

from run import create_task, app

router = APIRouter(tags=['Tasks'])


@router.post('/tasks')
def run_task(data=Body(...)):
    amount = int(data['amount'])
    x = data['x']
    y = data['y']
    task = create_task.delay(amount, x, y)
    return JSONResponse({'Task result:': task.get()})


@router.get('/tasks/{task_id}')
def get_status(task_id):
    task_result = app.AsyncResult(task_id)
    res = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return JSONResponse(res)
