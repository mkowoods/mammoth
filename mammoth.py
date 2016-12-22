#TODO: need to add navbar for the app
#TODO: NEED to add table that shows all open tasks
#TODO: NEED to add user authentication and API Key provisioning
#TODO: NEED to add user admin page


from flask import Flask, render_template, request
from tinydb import TinyDB, Query
import json
import logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
DB = TinyDB('./data/db.json')

@app.route('/')
def landing_page():
    return'<h3>Landing Page </h3>'

@app.route('/create_task/<api_key>')
def create_task(api_key):
    return render_template('create_task.html')

@app.route('/work_task/<task_id>')
def work_task(task_id):
    results = DB.get(eid = int(task_id))
    logging.info('Logging data: %s' % str(results) )
    return render_template('work_task.html', data=results)



@app.route('/add_task/<api_key>', methods = ['POST'])
def add_task(api_key): #TODO: need to modify to only take post commnands
    data = {
        'api_key': api_key,
        'solved': False
    }
    form_data = request.form['data']
    form_data = json.loads(form_data)

    for k,v in form_data.items():
        data[k] = v
    id = DB.insert(data)

    logging.info('Logging Task ID: %d, data: %s'% (id, data))
    return str(id)
if __name__ == '__main__':
    app.run(debug = True, port=5001)
