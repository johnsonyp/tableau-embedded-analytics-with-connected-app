from config.constants import TEMPLATE_DIR, STATIC_DIR
from config.settings import settings

from flask import Flask, render_template
from auth import jwt_token

app = Flask(
    __name__,
    template_folder=str(TEMPLATE_DIR),
    static_folder=str(STATIC_DIR)      
)

@app.route("/")
def index():
    heading = "My Embedded Tableau Dashboard"

    tableau_token = jwt_token(
        settings.CLIENT_ID,
        settings.SECRET_ID,
        settings.SECRET_KEY,
        settings.USER
    )

    # Dashboard // replace with your own values
    workbook_name = "Superstore"
    worksheet_name = "Overview"
    dashboard_url = f"https://{settings.REGION}.online.tableau.com/#/site/{settings.TABLEAU_SITE_ID}/views/{workbook_name}/{worksheet_name}"

    return render_template(
        "index.html",
        heading=heading,
        token=tableau_token,
        dashboard_url=dashboard_url
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)