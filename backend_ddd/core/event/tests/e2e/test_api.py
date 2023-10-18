from json import loads

from core.api import utils


def test_add_event_form(client):
    headers = {
        "Authorization": "Bearer pytest_auth_token",
        "Content-Type": "application/json",
    }

    response = client.post(
        "http://127.0.0.1:5000/api/v1/form_schema",
        json={
            "event_id":"1234",
            "event_form_schema": { 
                "fields":[
                    {
                        "question": "What is your name?",
                        "type": "INPUT_STR",
                        "validation": [
                            {
                                "type": "MIN_LENGTH",
                                "value": 1
                            },
                            {
                                "type": "MAX_LENGTH",
                                "value": 25
                            },
                            {
                                "type": "REQUIRED",
                                "value": True
                            }
                        ],
                        "options": [""]
                    },
                    {
                        "question": "What is your batch?",
                        "type": "MULTIPLE_CHOICE",
                        "validation": [
                            {
                                "type": "REQUIRED",
                                "value": True
                            }
                        ],
                        "options": ["2021","2022","2023","2024"]
                    }
                ]
            }
        },
        headers=headers,
    )

    print(response)
    payload = loads(response.data.decode())
    
    assert (
        payload
        == utils.Response(
            message="Schema attached successfully",
            status_code=200,
        ).__dict__
    )


    {"fields":[{
        'question': "What is your problem?",
        "answer": "Hello bro"
    },
    {
        'question': "What is your problem?",
        "answer": "Hello bro"
    }]}
