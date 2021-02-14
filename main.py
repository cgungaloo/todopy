from flask import Flask, request, Response, render_template, redirect, url_for, make_response
import db_actions
import json

app = Flask(__name__, template_folder='templates')

@app.route('/')
def render_home():
    todo_list = db_actions.get_all_todo_items()
    items = todo_list['items']
    return render_template("base.html", todo_list=items)

@app.route('/item/new', methods=['POST'])
def add_item():
    req_data = request.get_json()
    item =req_data['item']
    res_data = db_actions.add_item_to_todo_list(item)

    if res_data is None:
        response = Response("{'error': 'Item not added - " + item + "'}", status=400 , mimetype='application/json')
        return response

    response = Response(json.dumps(res_data), mimetype='application/json')

    return response

@app.route('/add', methods=['POST'])
def add_item_page():
    title = request.form.get("title")
    print(title)
    db_actions.add_item_to_todo_list(title)
    return redirect(url_for("render_home")) 

@app.route('/items', methods=['GET'])
def get_all_items():
    res_data = db_actions.get_all_todo_items()
    response = Response(json.dumps(res_data), mimetype='application/json')
    return response

@app.route('/item/status', methods=['GET'])
def get_item_status():
    item = request.args.get('item')
    status = db_actions.get_status(item)
    
    if status is None:
        response = Response("{'error': 'Item Not Found - %s'}"  % item, status=404 , mimetype='application/json')
        return response

    res_data = {
        'status': status
    }

    response = Response(json.dumps(res_data), status=200, mimetype='application/json')
    return response

@app.route('/item/update',methods=['PUT'])
def update_item():
    req_data = request.get_json()
    item =req_data['item']
    status = req_data['status']
    res_data = db_actions.update_item(item,status)

    if res_data is None:
        response = Response("{'error': 'Item not updated - " + item + "'}", status=400 , mimetype='application/json')
        return response

    response = Response(json.dumps(res_data), mimetype='application/json')
    return response

@app.route('/item/delete', methods=['DELETE'])
def delete_item():
    req_data = request.get_json()
    item = req_data['item']

    res_data = db_actions.delete_item(item)

    if res_data is None:
        response = Response("{'error': 'Item Not deleted - %s'}"  % item, status=404 , mimetype='application/json')
        return response

    response = Response(json.dumps(res_data), mimetype='application/json')
    return response

@app.route("/delete/<string:todo_id>")
def delete(todo_id):
    db_actions.delete_item(todo_id)
    return redirect(url_for("render_home"))

@app.route("/update/<string:todo_id>", methods=['POST'])
def update(todo_id):
    todo_option = request.form.get("todo_option")
    db_actions.update_item(todo_id,todo_option)
    return redirect(url_for("render_home"))

   ### CORS section
@app.after_request
def after_request_func(response):
    origin = request.headers.get('Origin')
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Headers', 'x-csrf-token')
        response.headers.add('Access-Control-Allow-Methods',
                            'GET, POST, OPTIONS, PUT, PATCH, DELETE')
        if origin:
            response.headers.add('Access-Control-Allow-Origin', origin)
    else:
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        if origin:
            response.headers.add('Access-Control-Allow-Origin', origin)

    return response
### end CORS section    

if __name__ == '__main__':
    app.run()
