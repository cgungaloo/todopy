# curl -X GET http://127.0.0.1:5000/item/status?item=Finish+app
# curl -X DELETE http://127.0.0.1:5000/item\/delete -d '{"item": "Finish app"}' -H Content-type:application/json
# curl -X POST http://127.0.0.1:5000/item/new -d '{"item": "Finish app"}' -H 'Content-Type: application/json'
# curl -X PUT http://127.0.0.1:5000/item/update -d '{"item": "Finish app", "status": "In Progress"}' -H 'Content-Type: application/json'