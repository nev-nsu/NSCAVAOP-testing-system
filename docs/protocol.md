Base schema
===========
- Primary request (primary = true, type, data)
- Primary responce (status, token, data, finished = false)
- Request (primary = false, token, type, data)
- Responce (status, data, finished = true)

Types
=====
- Testing request "run_tests"
- Update status request "update_status"
- Commutation request "commutation" (in future for non-generated tests)
- Interrupt request "stop"

Status is one of: *ADDED*, *COMPILATION*, *FAILED*, *TESTING*, *FINISHED*, *NOT_FOUND*. Case doesn't matter. 

Testing request
---------------
```json
{
    primary: true,
    type: 'run_tests',
    data: {
        code: 'int main() {}',
        options: {
            optimization_level: '3' // only optimization level for today
        },
        tests: [{
            type: 'generated', // only 'generated' for today
            number: 100,
            template: {
                type: {type: 'value', value: 'integer'},
                min: {type: 'test', template: {...}},
                max: {type: 'variable', name: 'MAX'},
                name: {type: 'value', value: 'n'} // no repeats
            }
        }],
        verifier: 'def verify(raw_input, raw_output, template): return true',
        responce_type: 'raw_data' // or 'failed_only' or 'statistic'
    }
}
```

In templates parameters must be objects with field **type** on of: *value* (and field **value**), *variable* (and field **name**), *test* (and filed **template**).

```json
{
    status: 'added',
    token: '42fefr5rfdeje8345',
    finished: false
}
```

Update request
--------------
```json
{
    primary: false,
    type: 'update_status',
    token: '434fjfm438rt',
}
```

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
```json
{
    primary: false,
    type: 'stop',
    token: 'ferifmu3dsf23r9dosc'
}

```json
{
    status: 'failed',
    data: 'aborted by user request'
}
