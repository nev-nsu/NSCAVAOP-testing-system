#!/usr/bin/bash
curl -H "Content-Type: application/json" -X POST -d '{
    "primary": true,
    "type": "run_tests",
    "data": {
        "code": "int main() {}",
        "options": {
            "optimization_level": "3"
        },
        "tests": [{
            "type": "generated",
            "number": 5,
            "template": {
                "type": {"type": "value", "value": "integer"},
                "min": {"type": "value", "value": -10},
                "max": {"type": "value", "value": 10},
                "name": {"type": "value", "value": "n"} 
            }
        }],
        "verifier": "print(\"OK\")",
        "response_type": "raw_data" 
    }
}' localhost:8080/api/v1/test
