from flask import Flask, render_template, request
from groq import Groq
import joblib
import os
import requests

# Remember to set Environment Variables to the following API Keys
# os.environ['GROQ_API_KEY'] = os.getenv("groq")
TELEGRAM_BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']

app = Flask(__name__)

#----------------------------------------------
@app.route("/",methods=["GET","POST"])
def index():
    return(render_template("index.html"))

#----------------------------------------------
@app.route("/main",methods=["GET","POST"])
def main():  
    return(render_template("main.html"))

#----------------------------------------------
@app.route("/dbs",methods=["GET","POST"])
def dbs():  
    return(render_template("dbs.html"))

#----------------------------------------------
@app.route("/llama",methods=["GET","POST"])
def llama():  
    return(render_template("llama.html"))

#----------------------------------------------
@app.route("/llama_reply",methods=["GET","POST"])
def llama_reply():
    
    q = request.form.get("q")

    # load model
    client = Groq()
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role":"user",
                "content":q
            }
        ]
    )

    return(render_template("llama_reply.html", r=completion.choices[0].message.content))

#----------------------------------------------
@app.route("/deepseek",methods=["GET","POST"])
def deepseek():  
    return(render_template("deepseek.html"))

#----------------------------------------------
@app.route("/deepseek_reply",methods=["GET","POST"])
def deepseek_reply():
    
    q = request.form.get("q")

    # load model
    client = Groq()
    completion = client.chat.completions.create(
        model="deepseek-r1-distill-llama-70b",
        messages=[
            {
                "role":"user",
                "content":q
            }
        ]
    )

    return(render_template("deepseek_reply.html", r=completion.choices[0].message.content))
#----------------------------------------------

@app.route("/prediction",methods=["GET","POST"])
def prediction():
    q = float(request.form.get("q"))

    # load model
    model = joblib.load("dbs.jl")

    # make prediction
    pred = model.predict([[q]])

    return(render_template("prediction.html",r=pred))

#----------------------------------------------
@app.route("/start_telegram",methods=["GET","POST"])
def start_telegram():  
    domain_url = "https://dsai-superapp.onrender.com"

    # The following line is used to delete the existing webhook URL for the Telegram bot
    delete_webhook_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/deleteWebhook"
    requests.post(delete_webhook_url, json={"url": domain_url, "drop_pending_updates": True})

    # Set the webhook URL for the Telegram bot
    set_webhook_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/setWebhook?url={domain_url}/telegram_webhook"
    webhook_response = requests.post(set_webhook_url, json={"url": domain_url, "drop_pending_updates": True})
    # print('webhook:', webhook_response)

    if webhook_response.status_code == 200:
        # set status message
        status = "The telegram bot is running. Please check with the telegram bot @about_bunky_bot"
    else:
        status = "Failed to start the telegram bot. Please check the logs."
    
    return(render_template("telegram.html", status=status))


#----------------------------------------------
@app.route("/telegram_webhook",methods=["GET","POST"])
def telegram_webhook():

    # This endpoint will be called by Telegram when a new message is received
    update = request.get_json()

    if "message" in update and "text" in update["message"]:
        # Extract the chat ID and message text from the update
        chat_id = update["message"]["chat"]["id"]
        query = update["message"]["text"]

        # Pass the query to the Groq model
        client = Groq()
        completion_ds = client.chat.completions.create(
            model="deepseek-r1-distill-llama-70b",
            messages=[
                {
                    "role": "user",
                    "content": query
                }
            ]
        )
        response_message = completion_ds.choices[0].message.content

        # Send the response back to the Telegram chat
        send_message_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        requests.post(send_message_url, json={
            "chat_id": chat_id,
            "text": response_message
        })
    return('ok', 200)

#----------------------------------------------
@app.route("/stop_telegram",methods=["GET","POST"])
def stop_telegram():  
    domain_url = "https://dsai-superapp.onrender.com"

    # The following line is used to delete the existing webhook URL for the Telegram bot
    delete_webhook_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/deleteWebhook"
    webhook_response = requests.post(delete_webhook_url, json={"url": domain_url, "drop_pending_updates": True})

    if webhook_response.status_code == 200:
        # set status message
        status = "The telegram bot is stopped."
    else:
        status = "Failed to stop the telegram bot. Please check the logs."
    
    return(render_template("telegram.html", status=status))
    # return(render_template("telegram.html"))

#----------------------------------------------



#----------------------------------------------
@app.route("/start_telegram_spam",methods=["GET","POST"])
def start_telegram_spam():  
    domain_url = "https://dsai-superapp.onrender.com"

    # The following line is used to delete the existing webhook URL for the Telegram bot
    delete_webhook_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/deleteWebhook"
    requests.post(delete_webhook_url, json={"url": domain_url, "drop_pending_updates": True})

    # Set the webhook URL for the Telegram bot
    set_webhook_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/setWebhook?url={domain_url}/telegram_spam_webhook"
    webhook_response = requests.post(set_webhook_url, json={"url": domain_url, "drop_pending_updates": True})

    if webhook_response.status_code == 200:
        # set status message
        status = "The telegram bot is running. Please check with the telegram bot @about_bunky_bot"
    else:
        status = "Failed to start the telegram bot. Please check the logs."
    
    return(render_template("telegram.html", status=status))

#----------------------------------------------
@app.route("/telegram_spam_webhook",methods=["GET","POST"])
def telegram_spam_webhook():

    # This endpoint will be called by Telegram when a new message is received
    update = request.get_json()

    if "message" in update and "text" in update["message"]:
        # Extract the chat ID and message text from the update
        chat_id = update["message"]["chat"]["id"]
        query = update["message"]["text"]

    # # load model
    # model = joblib.load("spam_model.jl")

    # # make prediction
    # pred = model.predict([[query]])

    # #Step: Send the result back to telegram
    # if pred=="ham":
    #     response_message = "[Is not a Spam]"
    # else:
    #     response_message = "[Is a Spam]"

    response_message = "test"

    # Send the response back to the Telegram chat
    send_message_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    requests.post(send_message_url, json={
        "chat_id": chat_id,
        "text": response_message
                            })
    
    return('ok', 200)

#----------------------------------------------
@app.route("/stop_telegram_spam",methods=["GET","POST"])
def stop_telegram_spam():  
    domain_url = "https://dsai-superapp.onrender.com"

    # The following line is used to delete the existing webhook URL for the Telegram bot
    delete_webhook_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/deleteWebhook"
    webhook_response = requests.post(delete_webhook_url, json={"url": domain_url, "drop_pending_updates": True})

    if webhook_response.status_code == 200:
        # set status message
        status = "The telegram bot is stopped."
    else:
        status = "Failed to stop the telegram bot. Please check the logs."
    
    return(render_template("telegram.html", status=status))
    # return(render_template("telegram.html"))

#----------------------------------------------

if __name__ == "__main__":
    app.run()