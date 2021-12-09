import base64
import os
from google.cloud import pubsub_v1
from flask import Flask, request


app = Flask(__name__)
# [END run_pubsub_server_setup]
# [END cloudrun_pubsub_server_setup]


# [START cloudrun_pubsub_handler]
# [START run_pubsub_handler]
@app.route("/", methods=["POST"])
def index():
    if request.is_json:
        input = request.get_json()
        convert_string = str(input)
        message = convert_string.encode("utf-8")
        #message = str.encode(str(country),"utf-8")
        #output = jsonify(country)
        #result=base64.b64decode(output).decode("utf-8")
        # message = str.encode(str(output),"utf-8")
        project_id = os.environ.get("GCP_PROJECT", None)
        topic_name = os.environ.get('PUB_SUB_TOPIC', 'Specified environment variable PUB_SUB_TOPIC is not set.')
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path(project_id, topic_name)
        future = publisher.publish(topic_path, data=message)
        print(future.result())
        return message
        

if __name__ == "__main__":
    #PORT = int(os.getenv("PORT")) if os.getenv("PORT") else 8080

    # This is used when running locally. Gunicorn is used to run the
    # application on Cloud Run. See entrypoint in Dockerfile.
    app.run(debug=True)
