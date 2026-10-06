import flask

#### CODE FROM EARLIER SUB-TASKS ###
# Write program code to create a global list named hash_tbl containing 70 empty slots.
hash_tbl = [ None for i in range(70)] # Empty hash table slots are represented by None.

def get_hash(equipment_id):
    # returns its corresponding hash index, using the hash algorithm above.
    # hash(k) = k mod 70
    return equipment_id % 70

def add_record(equipment_id, value):
    global hash_tbl # need this to ensure global hash table list can be accessed and modified within function

    # compute the initial index location using the function get_hash()
    index = get_hash(equipment_id)

    count = 0 # keeps track of how many times we've probed

    # insert the record into the list if the slot is open, or apply linear probing to locate the next open position
    while hash_tbl[index] != None:
        count += 1
        if count == len(hash_tbl):
            return False

        index = (index + 1) % len(hash_tbl)

    hash_tbl[index] = [equipment_id, value]

    # return True upon successful insertion, or False if no available slots remain.
    return True

def find_record(equipment_id):
    # compute the initial index location using the function get_hash()
    index = get_hash(equipment_id)

    count = 0 # keeps track of how many times we've probed

    # search through the table using linear probing to account for collisions
    while hash_tbl[index] != None and hash_tbl[index][0] != equipment_id:
        count += 1
        if count == len(hash_tbl):
            return False # full and not present

        index = (index + 1) % len(hash_tbl)

    # return the corresponding string value if the key exists, or False if the key is not present in the table.
    if hash_tbl[index] != None:
        return hash_tbl[index][1]
    else:
        return False

def load_data():
    # read all records from EQUIPMENT.txt
    file = open('EQUIPMENT.txt', 'r')

    count = 0

    # insert each record into hash_tbl using add_record()
    for line in file:
        line = line.strip() # remove \n at end of line
        line = line.split(' ')

        inserted = add_record(int(line[0]), line[1])

        # display an appropriate error message if any equipment item cannot be stored
        if not inserted:
            print('{} {} not inserted!'.format(line[0], line[1]))
        else:
            count += 1


    # display the total count of successfully loaded records upon completion.
    print('Successfully loaded {} records.'.format(count))

    file.close()

# Call the function load_data() and output the contents of hash_tbl.
load_data()
print(hash_tbl)

##################

app = flask.Flask(__name__)

@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/view/')
def view():
    global hash_tbl # required to access the hash table created earlier
    
    # displays all active (non-empty) equipment records stored in the hash_tbl.
    return flask.render_template('view.html', data=hash_tbl)

@app.route('/search/')
def search():
    return flask.render_template('form.html')

@app.route('/process_form/', methods=['POST'])
def process_form():
    global hash_tbl # required to access the hash table created earlier

    form_data = flask.request.form # dictionary
    id = form_data['id']
    
    descriptor = find_record(int(id))
    
    return flask.render_template('result.html', id=id, descriptor=descriptor)
    

### use this when running on your local machine
# app.run()

### this is only for online deployment purpose (so that you can preview the app online)
app.run(host="0.0.0.0", port=8080)
