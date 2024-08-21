from flask import Flask, render_template

import jwt
import datetime
import uuid

app = Flask(__name__)

# Tableau Instance // replace with your own values
REGION = '10ay'
TABLEAU_SITE_ID = 'sitename'
USER = 'username'

# Connected App Credentals // replace with your own values
CLIENT_ID = 'your_connected_app_client_id'
SECRET_ID = 'your_connected_app_client_key'
SECRET_KEY = 'your_connected_app_secret_value'

def jwt_token(client_id,secret_id,secret_key,user):
    token = jwt.encode(
        payload={
            "iss": client_id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=5),
            "jti": str(uuid.uuid4()),
            "aud": "tableau",
            "sub": user,
            "scp": ["tableau:views:embed", "tableau:metrics:embed"]
        },
        key=secret_key,
        algorithm="HS256",
        headers= {
            "kid": secret_id,
            "iss": client_id
        }
    )
    return token


@app.route('/')
def index():
    heading = 'My Embedded Tableau Dashboard'
    tableau_token = jwt_token(CLIENT_ID,SECRET_ID,SECRET_KEY,USER)

    # Dashboard // replace with your own values
    workbook_name = 'Superstore'
    worksheet_name = 'Overview'
    dashboard_url = f'https://{REGION}.online.tableau.com/#/site/{TABLEAU_SITE_ID}/views/{workbook_name}/{worksheet_name}'

    return render_template(
        'index.html',
        heading=heading,
        token=tableau_token,
        dashboard_url=dashboard_url
    )

if __name__ == '__main__':
    app.run(debug=True)