Base schema
===========
- Primary request (type, data)
- Primary response (status, token, data)
- Request (token, type, data)
- Responce (status, data)

All requests are in JSON format.

Types
=====
- Testing request "run_tests"
- Update status request "update_status"
- Interrupt request "stop"

Status is one of: *ADDED*, *COMPILATION*, *FAILED*, *TESTING*, *FINISHED*, *NOT_FOUND*. Case doesn't matter. 

Exmaples (JavaScript object, not string representation!):

Testing request
---------------
Client-to-Server:
```json
{
    type: 'run_tests',
    data: {
        code: 'int main() {}',
        options: {
            optimization_level: '3' // only optimization level for today
        },
        tests: [{
            number: 100,
            template: {
                type: {type: 'value', value: 'integer'},
                min: {type: 'value', value: -10},
                max: {type: 'value', value: 10},
                name: {type: 'value', value: 'n'} // no repeats
            }
        }],
        verifier: 'print (\'OK\')',
        response_type: 'raw_data' // or 'failed_only' or 'statistic'
    }
}
```

In templates parameters must be objects with field **type** on of: *value* (and field **value**), *variable* (and field **name**), *test* (and filed **template**).

Server-to-Client:
```json
{
    status: 'added',
    token: '42fefr5rfdeje8345'
}
```

Update request
--------------
Client-to-Server:
```json
{
    type: 'update_status',
    token: '434fjfm438rt'
}
```

Server-to-Client:
```json
{
    status: 'finished',
    data: {
        ok: 155,
        wa: 15
    }
}

// or

{
    status: 'finished',
    data: [{
        input: '123',
        output: '789',
        result: '1' // WA - wrong answer
    }]
}

// or

{
    status: 'failed',
    data: 'error here'
}

{
    status: 'run'
}

```

Interrupt request
-----------------
Client-to-Server:
```json
{
    type: 'stop',
    token: 'ferifmu3dsf23r9dosc'
}
```

Server-to-Client:
```json
{
    status: 'failed',
    data: 'aborted by user request'
}
```
