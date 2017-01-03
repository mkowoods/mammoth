#TODO: need to add navbar for the app
#TODO: NEED to add table that shows all open tasks
#TODO: NEED to add user authentication and API Key provisioning
#TODO: NEED to add user admin page


from flask import Flask, render_template, request
from tinydb import TinyDB, Query
import json
import logging
import time
import base64
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
DB = TinyDB('./data/db.json')

@app.route('/')
def landing_page():
    all_tasks = DB.search(Query()['task_type'] != '')
    return render_template('table.html', data = all_tasks)

@app.route('/create_phone_task/<api_key>')
def create_phone_task(api_key):
    return render_template('create_phone_task.html')

@app.route('/create_file_review_task/<api_key>')
def create_file_review_task(api_key):
    return render_template('create_file_review.html')

@app.route('/work_task/<task_id>')
def work_task(task_id):
    results = DB.get(eid = int(task_id))
    logging.info('Logging data: %s' % str(results) )
    return render_template('work_task.html', data=results)



@app.route('/add_task/<api_key>', methods = ['POST'])
def add_task(api_key): #TODO: need to modify to only take post commnands
    data = {
        'api_key': api_key,
        'solved': False,
        'create_date': time.time()
    }
    if request.files:
        file = request.files['file']
        data['file_name'] = file.filename
        data['file_data'] = base64.b64encode( file.stream.read() )
        for k, v in request.form.items():
            data[k] = v
    else:
        form_data = request.form['data']
        form_data = json.loads(form_data)

        for k,v in form_data.items():
            data[k] = v

    id = DB.insert(data)

    logging.info('Logging Task ID: %d, data: %s'% (id, data))
    return str(id)

@app.route('/mark_completed/<task_id>', methods=['POST'])
def update_task(task_id):
    data = request.form
    DB.update({'solved': True,
               'comment': data['comment'],
               'option_choice': data['option_choice']},
              eids=[int(task_id)])

    return 'true'

if __name__ == '__main__':
    app.run(debug = True, port=5001)
