import base64
import os
from google.cloud import pubsub_v1
from flask import Flask, request
import json 
import pandas as pd 
from google.cloud import bigquery
from google.cloud import storage

app = Flask(__name__)
# [END run_pubsub_server_setup]
# [END cloudrun_pubsub_server_setup]


# [START cloudrun_pubsub_handler]
# [START run_pubsub_handler]
@app.route("/", methods=["POST"])
def index():
    envelope = request.get_json()
    if not envelope:
        msg = "no Pub/Sub message received"
        print(f"error: {msg}")
        return f"Bad Request: {msg}", 400

    if not isinstance(envelope, dict) or "message" not in envelope:
        msg = "invalid Pub/Sub message format"
        print(f"error: {msg}")
        return f"Bad Request: {msg}", 400

    pubsub_message = envelope["message"]
    try:
        if isinstance(pubsub_message, dict) and "data" in pubsub_message:
            name = base64.b64decode(pubsub_message["data"]).decode("utf-8").strip()
            replace_quotes= name.replace("'", '"')
            # output= ast.literal_eval(json.dumps(name))
            output = json.loads(replace_quotes)
            #print(str(type(name)))
            article = output["article_no"]
            client = bigquery.Client()
            query = """
                SELECT *
                FROM `store_goods_movement.mhs_store_goods_movement_ttyp310`
                WHERE id = ?
            """
            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter(None, "STRING", f'{article}'),
                ]
            )
            query_job = client.query(query, job_config=job_config)
            results = query_job.result() 
            dataframe = results.to_dataframe()
            print(f"{dataframe}" )
            print(str(type(dataframe)))
            op_message = dataframe.to_json(orient='records',date_format = 'iso')  #json string 
            dict_message = json.loads(op_message)
            json_message = json.dumps(dict_message[0])
            print(json_message)
            print(str(type(json_message)))
    
            client = storage.Client(project="ingka-dp-sap-dev")
            bucket = client.get_bucket("ingka-s2p-sapfin-store-goods-movements-ttyp310-error-dev")
            blob = bucket.blob('resubmission/'+ article +'.json')
            blob.upload_from_string(data=json_message, content_type="application/text")

    except Exception as e:
        print (e)

        # Optionally, explicitly request to use the BigQuery Storage API. As of
        # google-cloud-bigquery version 1.26.0 and above, the BigQuery Storage
        # API is used by default.
    
        
        # query_job = client.query(query) 
        # rows = query_job.result()
        # for row in rows:
        #     print(str(type(rows)))
        #     print(row)
        #     print(str(type(row)))
        #     df = row.to_dataframe()
        #     json_message= df.to_json()
        #     print(json_message)
        #     print(str(type(json_message)))

    
    print(f"{article}")

    return ("", 204)

    # if request.is_json:
    #     input = request.get_json()
    #     print(f"{input}")
    #     print(str(type(input)))
    #     return input 
        

if __name__ == "__main__":
    #PORT = int(os.getenv("PORT")) if os.getenv("PORT") else 8080

    # This is used when running locally. Gunicorn is used to run the
    # application on Cloud Run. See entrypoint in Dockerfile.
    app.run(debug=True)
