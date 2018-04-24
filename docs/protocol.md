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

Testing request
---------------
```json
{
    primary: true,
    type: 'run_tests',
    data: {
        code: 'int main() {}',
        options: {
            optimization_level: '3'
        },
        tests: [{
            type: 'generated', // only 'generated' for today
            number: 100,
            type: 'integer',
            min: -5,
            max: 5,
            name: "n" // no repeats
        }],
        verifier: 'def verify(raw_input, raw_output, template): return true',
        responce_type: 'raw_data' // or 'failed_only' or 'statistic'
    }
}
```

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

{
    status: 'finished',
    data: [{
        input: '123',
        output: '789',
        result: '1' // WA - wrong answer
    }]
}

{
    status: 'compilation failed',
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
    status: 'aborted',
    data: 'by user request'
}
