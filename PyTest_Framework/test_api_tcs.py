import requests
import uuid

endpoint = "https://todo.pixegami.io"

# write tests here
def test_can_call_endpoint():
    response = requests.get(endpoint)
    assert response.status_code == 200, "API call failed"


def test_can_create_task():
    """
    payload = {
        "content": "My API Test",
        "user_id": "test_user",
        "is_done": False
    }
    """
    #create a task
    payload = new_test_data()
    #create_task_response = requests.put(endpoint + "/create-task", json=payload)
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200, "API call failed"
    data = create_task_response.json()

    #get the task
    task_id = data['task']['task_id']
    #get_task_response = requests.get(endpoint + f"/get-task/{task_id}")  # f format string
    get_task_response = get_task(task_id)
    get_task_data = get_task_response.json()

    #Validate if it matches with what was passed in payload
    assert get_task_response.status_code == 200, "API call failed"
    assert get_task_data['content'] == payload['content']
    assert get_task_data['user_id'] == payload['user_id']

def test_can_update():

    # create a task
    payload = new_test_data()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200, "Create API failed"

    # update the task
    task_id = create_task_response.json()['task']['task_id']
    new_payload = {
        "user_id":payload["user_id"],
        "task_id":task_id,
        "content": "updated_data",
        "is_done": True
    }
    update_task_response = put_task(new_payload)
    assert update_task_response.status_code==200, "update API failed"

    # get and validate the task
    get_task_response = get_task(task_id)
    assert get_task_response.status_code==200, "Validate API failed"
    assert get_task_response.json()['content'] == new_payload["content"], "Content data doesn't match"
    assert get_task_response.json()['is_done'] == new_payload['is_done'],  "is_done data doesn't match"


def test_can_list_tasks():
    #create task for N number of time
    n= 3
    payload = new_test_data()
    for _ in range(n):
        create_task_response = create_task(payload)
        assert create_task_response.status_code == 200, "Create API failed"

    #list the tasks
    list_task_response = list_task(payload['user_id'])
    assert list_task_response.status_code == 200, 'List API failed'

    # validate the list count
    tasks = list_task_response.json()['tasks']
    assert len(tasks)== n, "count doesn't match"

def test_can_delete_tasks():
    #create a task
    payload = new_test_data()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200, "Create API failed"
    task_id = create_task_response.json()['task']['task_id']
    #Delete a task

    del_task_response = delete_task(task_id)
    assert del_task_response.status_code == 200, "Delete API failed"

    #Get the task to check if it exists
    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 404, "Task still exists"

def create_task(payload):
    create_task_response = requests.put(endpoint + "/create-task", json=payload)
    return create_task_response

def put_task(payload):
    update_task_response = requests.put(endpoint + "/update-task", json=payload)
    return update_task_response

def get_task(task_id):
    get_task_response = requests.get(endpoint + f"/get-task/{task_id}")  # f format string
    return get_task_response

def new_test_data():
    test_user_id = f"test_user_{uuid.uuid4().hex}"
    content = f"test_content_{uuid.uuid4().hex}"
    return {
        "content": content,
        "user_id": test_user_id,
        "is_done": False
    }

def list_task(user_id):
    list_task_response = requests.get(endpoint + f"/list-tasks/{user_id}")  # f format string
    return list_task_response

def delete_task(task_id):
    del_task_response = requests.delete(endpoint + f"/delete-task/{task_id}")  # f format string
    return del_task_response