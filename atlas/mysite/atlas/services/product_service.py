from django.http import HttpResponse
from django.http import HttpRequest
import pandas as pd
import numpy as np
from atlas import static_data
#from atlas.PyScripts import ATLAS1
import datetime
import pandas as pd
import numpy as np
from atlas.PyScripts import task1
from atlas.config import dbConfig
import StringIO
import traceback


full_data_dict = {'filename_obj': None, 'file_data': None, 'senti_dict': dbConfig.dict['sentDict'],
                  'td_dict': dbConfig.dict['keywordsDict']}


def fetchRequests():
    df = pd.read_csv(dbConfig.dict["requestUrl"])
    jsonData = df.to_json(orient='records')
    return jsonData


def raiseRequest(request, site, refreshStatus):
    responseObject = {}
    keyObject = ["message", "status", "body"]
    curTime = datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M:%S %p")
    for i in keyObject:
        responseObject[i] = None

    columns = ['reqKw', 'reqTime', 'reqStatus']
    status = 'Pending'
    df = pd.read_csv(dbConfig.dict["requestUrl"])
    if refreshStatus:
        print refreshStatus
        if ((df['reqStatus'] == 'Pending') & (df['reqKw'] == request)).any():
            responseObject["message"] = "Conflict: A pending/processing entry for the product already exists"
            responseObject["status"] = 409
            responseObject["body"] = request
            return responseObject
        df.ix[(df.reqStatus == 'Completed') & (df.reqKw == request), 'reqTime'] = curTime
        df.ix[(df.reqStatus == 'Completed') & (df.reqKw == request), 'reqStatus'] = status
        with open(dbConfig.dict["requestUrl"], 'w') as f:
            (df).to_csv(f, index=False)
        f.close()
    else:
        # df.to_csv("C:\\Users\\akshat.gupta\\Documents\\django-atlas\\mysite\\atlas\\database\\request.csv", mode='a', index=False, sep=',', header=False)
        data = np.array([[request, curTime, status]])
        print("len(df): ", len(df))
        df1 = pd.DataFrame(data, columns=columns, index=[len(df)])
        with open(dbConfig.dict["requestUrl"], 'a') as f:
            (df1).to_csv(f, header=False)
        f.close()
    #task.work()
    task1.pool_exe(request, site)
    responseObject["message"] = "Success: Request raised successfully"
    responseObject["status"] = 200
    responseObject["body"] = request
    return responseObject


def getMetaDataFromProducts():
    ls = []
    for key, val in static_data.products.items():
        ls.append(val["metaData"])
    return ls


def reset_data_dict_map():
    global full_data_dict

    full_data_dict = {'filename_obj': None, 'file_data': None, 'senti_dict': dbConfig.dict['sentDict'],
                      'td_dict': dbConfig.dict['keywordsDict']}


def uploadFile(request):
    global full_data_dict
    print("INSIDE UPLOADFILE(REQUEST) FUNCTION")
    print("REQUEST")
    #print request
    responseObject = {}
    keyObject = ["message", "status", "body"]
    for i in keyObject:
        responseObject[i] = None
    #print "Content-Type: text/html"
    a = request.FILES

    #print("a:", a)

    # print (type(a))
    # print dir(request)
    # print(dir(a['kartik-input-711[]']))
    #              form = cgi.FieldStorage()

    curTime = datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M:%S %p")
    columns = ['reqKw', 'reqTime', 'reqStatus']
    status = 'Pending'
    df = pd.read_csv(dbConfig.dict["requestUrl"])

    ids = ['input441[]', 'input442[]', 'input44[]']

    #full_data_dict = {'filename_obj': None, 'file_data': None, 'senti_dict': dbConfig.dict['sentDict'], 'td_dict': dbConfig.dict['keywordsDict']}
    # [dataset name obj, data_df, senti dict, trig-driv dict]
    #print(full_data_dict)

    for i in ids:
        print("INSIDE FOR LOOP FOR REQUESTS IN UPLOADS")
        try:
            if request.FILES:
                filedata = request.FILES[i]
                if filedata:
                    filecontents = filedata.file.read()

                    if i == 'input441[]':
                        target = dbConfig.dict['sentDictsPath'] + filedata._name
                        #print(target)

                        full_data_dict['senti_dict'] = target
                        with file(target, 'w') as outfile:
                            outfile.write(filecontents)
                            responseObject["message"] = "Success: File Uploaded successfully"
                            responseObject["status"] = 200
                            responseObject["body"] = filedata._name
                        print("Senti dict uploaded")
                    elif i == 'input442[]':
                        target = dbConfig.dict['tdDictsPath'] + filedata._name
                        #print(target)
                        full_data_dict['td_dict'] = target
                        with file(target, 'w') as outfile:
                            outfile.write(filecontents)
                            responseObject["message"] = "Success: File Uploaded successfully"
                            responseObject["status"] = 200
                            responseObject["body"] = filedata._name
                        print("TD dict uploaded")
                    elif i == 'input44[]':
                        target = dbConfig.dict['uploadsUrl'] + filedata._name
                        #print(target)
                        full_data_dict['filename_obj'] = filedata._name
                        full_data_dict['file_data'] = filecontents
                        with file(target, 'w') as outfile:
                            outfile.write(filecontents)

                            responseObject["message"] = "Success: File Uploaded successfully"
                            responseObject["status"] = 200
                            responseObject["body"] = filedata._name
                            # open requests file and raise a request to analyse this file
                            data = np.array([[filedata._name, curTime, status]])
                            df1 = pd.DataFrame(data, columns=columns, index=[len(df)+1])
                            with open(dbConfig.dict["requestUrl"], 'a') as f:
                                df1.to_csv(f, header=False)
                            f.close()
                        print("full_data_dict")
                        print(full_data_dict)
                        print("calling task1")
                        task1.pool_exe_file(full_data_dict)
                        reset_data_dict_map()
        except:
            print("Error while uploading file:-")
            print traceback.print_exc()

    # try:
    #     if request.FILES['files[]']:
    #         filedata = request.FILES['files[]']
    #         if filedata.file:  # field really is an upload
    #             filecontents = filedata.file.read()
    #             target = dbConfig.dict['sentDictsPath'] + "\\" + filedata._name
    #             print(target)
    #             with file(target, 'w') as outfile:
    #                 outfile.write(filecontents)
    #             data_df = pd.read_csv(StringIO.StringIO(filecontents))
    #             print("sentidict saved")
    #             # full_data_dict['trigdriv_dict'] = data_df
    # except:
    #     print "Exception caught"
    #     #print traceback.print_exc()

    #print("calling task1")
    #task1.pool_exe_file(filedata._name, data_df)
    #task1.pool_exe_file(full_data_dict)
    return responseObject
