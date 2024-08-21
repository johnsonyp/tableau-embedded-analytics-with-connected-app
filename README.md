# Tableau Embedded Analaytics with Connected App

This is a sample using of how you can use [Tableau Embedded Analytics](https://www.tableau.com/products/embedded-analytics) in conjunction with [Tableau Connected Apps](https://help.tableau.com/current/online/en-us/connected_apps.htm). For this demo, we will use **Python** and `Flask` to create both the front and back end for this example. There are a few notes/placeholders in the files that will guide you on what values you are needed to be replaced with your own instances.

## Overview

While embedding a Tableau dashboard is very straightforward in that the embed code snippet can be easily pulled when you use the *share* option from a dashboard - we can run into some challenges when it comes to wanting to create a more seamless experience.
```
<script type='module' src='https://public.tableau.com/javascripts/api/tableau.embedding.3.latest.min.js'></script>
<tableau-viz id='tableau-viz' src='{{dashboard_url}}' width='1395' height='670' toolbar='bottom' device='default' >
</tableau-viz>
```

The primary use case that comes to mind when needing to integrate with a Connected App is to prevent the need to "sign-in" multiple times. For instance, you have your own website or application which users are already accessing via some sign-in methods, an emedded Tableau dashboard will likely prompt them to sign-in via their Tableau account. This can lead to a poor user experience, especially if you are servicing clients  and not just internal staff.

Hence, we need Tableau's Connected App to help your application help communicate to Tableau that this user is already authorized and permitted to view whatever dashboard you have embedded. 

## Setup Connected App

The first step is to create your Connected App in Tableau. Tableau [provides a very straightforward guide](https://help.tableau.com/current/online/en-gb/connected_apps_direct.htm) on how to do so.

For the purposes of this example, we will use the **Direct Trust** option. Otherwise, ensure the app is enabled and grab the **Client ID**, **Secret ID** and **Secret Value**. You can replace the in the placeholders for the Connected App Credentials in the `main.py`.

## JWT Token Generation

Tableau uses a JWT (JSON Web Token) token to help authenticate users securly in order to skip the login screen. In Python, you can use the `PyJWT` library with the `uuid` library to help generate this token. Taleau also provides a more [in-depth guide](https://help.tableau.com/current/online/en-gb/connected_apps_direct.htm#step-3-configure-the-jwt) on the parameters needed to be passed to create this token.

The `main.py` provided should already provide a working function to generate the JWT. If you are interested in working more with connected apps, it is best to review the guide as well as understand the [scopes](https://help.tableau.com/current/online/en-us/connected_apps_scopes.htm) that can be included as it will enable certain permissions and features when using the token.

```
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
```

The `user` variable being paired with `sub` is the username that will be used to authenticate through to Tableau. Hence, it will use that user's permissions and settings when rendering the embedded viz. If the selected user does not have permission to the chosen dashboard, it will fail to load.

This will vary between apps, but for most scenarios the value passed to `sub` will be dynamically determined from your application based on who is signed-in currently to it. For our demo and example, we are just passing in a constant value for sampling purposes.

## Embeded Visualization

Once the token is generated we can very simply include it as part of the embed snippet in the html as an attribute. In our example, we will generate the JWT token during the default endpoint and pass that over to the front-end with `render-template`. Be sure to update the `dashboard_url` and its associated variables accordingly so it displays a dashboard from your tableau instance.

```
<tableau-viz 
    id="tableauViz" 
    src='{{ dashboard_url }}' 
    token="{{ token }}"
    onVizLoadError="handleLoadError"
    onTabSwitched="scrollTop"
>
</tableau-viz>
```

If you are familiar with `Flask` you can test all this by simply running the `main.py` and going to http://127.0.0.1:5000/ via a browser.

## Closing Thoughts

This is a quick example of how to make embedded analytics a bit more seamless if you are choosing to incorporate Tableau dashboards in your own application that already has a login portion. The ideas and scenarios provided here are a quick starting point, but do not cover all the bases that you may need to consider and implement.

Ultimately, Tableau is still handling a significant amount of work here in that the dashboards and their permissions are still controlled on that end. Users will still need to exist in Tableau in order to properly handle permission and activity tracking accordingly. As such, while a connected app may remove the "double sign-in" issue, you may encounter a "double account setup" issue with the need for users to exist on Tableau and your own application.

This repository currently does not cover the automation and further integration of users between Tableau and your own application. Tableau provides some [documentation](https://help.tableau.com/current/online/en-us/scim_config_online.htm) and varying methods on how to handle this.



## Notes


### Constants
In the  `main.py`, for your credentials, ensure you replace the Tableau Instance variables with your own.

**Region**: This is the server your Tableau Cloud is located on. If you're not sure, go to your Tableau Cloud and it will be in the first part of the url. (e.g. https://us-west-2b.online.tableau.com/#/site... the value will be `us-west-2b`)

**Tableau Site Id:** You can also find this in your url. (e.g. https://us-west-2b.online.tableau.com/#/site/my-company/explore will be `my-company`)


**User:** This will be the username of the user you want the Connected App to authorize against. If you are using SSO methods to login to Tableau, then the username will likely be the e-mail address.

### Other Functions
For our demo we will keep it simple and just use the `tableau-viz` tag, but there is far more with the [Tableau Embedding API](https://help.tableau.com/current/api/embedding_api/en-us/index.html) you can to further interact with your embed and the rest of your application it is hosted on.

You may notice there is an additional JavaScript function included in the `index.html` called `scrollTop`.

```
<script>
    function scrollTop() {
        window.scrollTo({
            top: 0,
            behavior: 'auto'
        });
    }
</script>
```
This is an extra snippet included to help resolve an issue that some dashboards may encounter when it has a large height dimension and long loading times. What happens is a the Processing pop-up will appear and cause Tableau to force the browser to jump the center of the dashboard (where that pop-up appears) and stay there after.

Not the best experience when jumping between tabs - as such, to help mitigate this, there is an `onTabSwitched` attribute that can be applied and call a JS function whenever it detects the viz has changed tabs. Our `scrollTop` function can be called and bring the browser window back to the top. Not necessarily the most elegant approach, but a band-aid nonetheless.


It is unknown if there will be a fix implemented by Tableau, but you can read [others' experience in the community](https://community.tableau.com/s/question/0D58b0000Bz2TLcCQM/embedded-dashboard-jumps-to-processing-loader-before-scrolling-to-the-top-of-the-page).
