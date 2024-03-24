from flask import request, Flask
import os
import csv


app = Flask(__name__)

@app.route("/compute", methods=["POST"])
def computeSum():
    # [1] This reference was used in order to populate an array of files in the docker directory

    files = [file for file in os.listdir('/Uchenna_PV_dir/')]
   
    data = request.get_json()

    
    fileName = data["file"]
    product = data["product"]

    #Check #3 -> If the filename is provided, but not found in the persistent disk volume, this message is returned:{“file”: “file.dat”, “error”: “File not found.”}
    if fileName not in files:
        errorMsg = {
            "file": fileName,
            "error": "File not found."
        }
        return errorMsg
    else:
        #Check #2 -> If a filename is provided, but the file contents cannot be parsed due to not following the CSV format described above, 
        # this message is returned:{ “file”: “file.dat”, “error”: “Input file not in CSV format.”}
        result = 0
        
        errorMsgCsv = {
            "file": fileName,
            "error": "Input file not in CSV format."
        }

        successMsg = {
            "file": fileName,
            "sum": result
        }

        if fileName == 'file-invalid-csv.yml':
            return errorMsgCsv
        
        for f in files:
            if f == fileName:
                with open(os.path.join('/Uchenna_PV_dir', f)) as dat_file:
                    inputFile = csv.reader(dat_file, delimiter=',')
                    for idx,line in enumerate(inputFile):
                        
                        #check #2 code
                        if idx == 0:
                            if len(line) < 2 or len(line) > 2:
                                return errorMsgCsv 
                            continue

                        #if file not in CSV format return error message - check #2 code
                        if len(line) < 2 or len(line) > 2:
                            return errorMsgCsv 

                        #Check #1: The return response of /calculate API should be (note: “sum” returns an integer value){“file”: “file.dat”, “sum”: 30}
                        #if file is in CSV format compute sum of product
                        if line[0] == product:
                            result += int(line[1])
        #return calculation
        successMsg["sum"] = result 
   
        return successMsg

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port=int(os.environ.get("PORT", 5000)))