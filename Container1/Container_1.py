from flask import jsonify, request, Flask
import requests
import os
import json
import csv

#REFERENCES
# 1 - https://github.com/SwarajJalkote/csv_to_dat 
# 2 - https://www.freecodecamp.org/news/how-to-create-a-csv-file-in-python/
# 3 - https://blog.finxter.com/5-best-ways-to-convert-csv-files-to-dat-format-using-python/
# 4 - x

app = Flask(__name__)

@app.route("/store-file", methods=["POST"])
def storeFile():

    if request.method == "POST":
        data = request.get_json()
        
        file = data["file"]

        # Check #3 -> If the file name is not provided, an error message is returned: {“file”: null, “error”: “Invalid JSON input.”}
        if file == None or file == "null":
            errMessage = {
                "file": None,
                "error": "Invalid JSON input."
            }
            
            return json.dumps(errMessage)
        else:
            '''
            Create a file and store the data given in the API request. The file should be stored in the GKE persistent storage.
            You must make sure that your container can access the persistent storage.
            '''
            
            #Check #1 -> If the file is stored successfully, this message should be returned: {“file”: “file.dat”, “message”: “Success.”}
            #references: [1, 2, 3] 
            success_msg = {"file": "file.yml", "message": "Success."}
            fail_msg = {"file": "file.dat", "message": "Error while storing the file to the storage."}
            file_data = data["data"]

            file_data_arr = file_data.split('\n')

            dat_data = []
            
            

            for row in enumerate(file_data_arr):
                row_data = row[1].split(',')
                col_val1, col_val2 = row_data[0], row_data[1]
                record = [''.join(col_val1), ''.join(col_val2)] 
                dat_data.append(record)
            
            #Try to write "file.dat" to the GKE persistent storage. If successful, return success_msg else, return fail_msg
            path = '/Uchenna_PV_dir/{}'.format(file)
            try:
                with open(path, 'w', newline='') as dat_file:
                    writer = csv.writer(dat_file)
                    writer.writerows(dat_data)

                return json.dumps(success_msg)
            except:
                #Check #2 -> If there was an error to store the file in the persistent storage, this message should be returned:
                #{ “file”: “file.dat”, “error”: “Error while storing the file to the storage.” }
                return json.dumps(fail_msg)
                

@app.route("/calculate", methods=["POST"])
def create():

    if request.method == "POST":
        data = request.get_json()
        
        file = data["file"]

        #Check #4 -> If the file name is not provided, an error message is returned:{“file”: null,“error”: “Invalid JSON input.”}
        if file == None or file == "null":
            errMessage = {
                "file": None,
                "error": "Invalid JSON input."
            }
            return json.dumps(errMessage)
        else:

            response = requests.post("http://localhost:5000/compute", json=data)

            return response.json()
       
       
if __name__ == "__main__":
    app.run(host = "0.0.0.0", port=int(os.environ.get("PORT", 6000)))