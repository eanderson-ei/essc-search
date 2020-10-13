# README

This library provides a search interface for the LAC ESSC Knowledge Graph. See `essc-knowledge-base` to create the initial knowledge graph. 

To run: `python index.py`.

START HERE: http://nicolewhite.github.io/neo4j-flask/ (see step 15 deploy to Heroku)

* Repo:https://github.com/xiarnousx/py2neo-flask/blob/master/app/blog/models.py
* Video: https://www.youtube.com/watch?v=ZMOHEh-caTc&t=1163s

* Same author, different vid: https://www.youtube.com/watch?v=3JMhX1sT98U&t=1282s

Copy graph from local: https://stackoverflow.com/questions/48999032/how-to-migrate-my-local-neo4j-dataset-to-the-graphenedb-instance/48999371#48999371

Example code (old) for accessing graph with py2neo: https://stackoverflow.com/questions/43608686/connection-error-to-graphenedb-hosted-on-heroku/43619906#43619906

To load csv, upload to github first and get raw link: https://stackoverflow.com/questions/41211383/cant-load-csv-data-into-graphenedb-instance/41260999#41260999

## Contents

**app.py**: barebones Dash app with authentication

**index.py**: 'home' page of the app that handles page navigation

**layouts.py**: includes all layouts and bootstrap components

**callbacks.py**: includes all callbacks except for a few in index.py to handle the page navigation

**assets/**

* this folder is automatically detected by Dash (as named) and includes a favicon and logo image files

**components/**

* **\_\_init\_\_.py**: allows importing from components
* **graph_database.py**: handles all graph database operations

## Next Steps

- [ ] 

## TODO

- [ ] 

## Tips

#### Limitations on node properties

Because tags and report filenames are being passed into an f string, single or double quotes can throw off the cypher query. As currently set up, tags and filenames must not include double quotes. An error will only occur when a double quote is encountered, so screen/block ahead of time.

#### Dynamic callbacks and callbacks in loops

If you are creating buttons or other features dynamically, and/or if you have a long or indeterminate list of buttons or other features as input, use `dash.callback_context` to create the callbacks:

```python
@app.callback(
    Output('my_output', 'children'),
    [Input(option, 'n_clicks') for option in button_list]
)
def dynamic_buttons(*button_clicks):
    ctx = dash.callback_context
    
    if not ctx.triggered:
        raise PreventUpdate

    option = ctx.triggered[0]['prop_id'].split('.')[0]
    return option
```

Inputs are passed as `*args` to the callback allowing for any number of inputs (in this case buttons). 

## Dash Quickstart Guide

### Starting a Dash project

How to start a Dash project

```bash
conda create -n <ENV_NAME> python
conda activate <ENV_NAME>
pip install dash==1.11.0  # use most recent version from Users Guide
pip install dash-auth==1.3.2  # for basic login protection
pip install requests  # this is not included in the docs, not sure why it isn't installed as a dependency, but it is needed
pip install dash-bootstrap-components  # if using Bootstrap
```
### Authentication
For authentication, save a `.json` file in `secrets/` with the following code (INCLUDE THIS FILE IN YOUR GITIGNORE. Note I also include a .keep file in there so people who clone the repo know where that should be.) You can include as many username, password pairs as you want, separated by a colon (double quotes required).

```json
{
    "username": "password"
}
```

When deploying to Heroku, go to the Config Vars option under 'Settings' and paste the content of the json file there. The `KEY` will be `VALID_USERNAME_PASSWORD_PAIRS` and the `VALUE` will be the contents of the json file.

When deploying to Heroku, go to the Config Vars option under 'Settings' and paste the content of the json file there. The `KEY` will be `VALID_USERNAME_PASSWORD_PAIRS` and the `VALUE` will be the contents of the json file.

### Assets

Store a logo, favicon, and custom css or javascript in a folder `./assets/` and they will automatically be discovered by Dash. Save the external stylesheet as your css if you want to edit or amend it. See [docs](https://dash.plotly.com/external-resources) for more. 

### Handling data

Data are just stored and read from the 'processed' data folder, so you need to run the read_*.py files before deploying if updating data (for now). Try a data class that reads everything in, joins it, and stores it in a temp div for later access. There are also constants in the code (e.g., Focal Area names) that are just stored as code, which could be improved.

### Deploying to Heroku

I deployed as soon as the structure was built to make it easier to debug the deployment. Here are the steps:

* Make sure app.py includes (after defining variable app)

  ```python
  server = app.server
  ```

* Create Procfile with contents. We're running from index, rather than app.

  ```
  web: gunicorn index:server
  ```

  Note no space after `index:`

* Install gunicorn if not already installed

  ```bash
  pip install gunicorn
  ```

  Create requirements.txt

  * `pip freeze>requirements.txt`
  * You can also list the key dependencies in a text file called requirements.txt. Should set up a pip or conda environment though.

* Create a heroku project

* ```bash
  heroku create <app name>
  ```

* Use Heroku to deploy

  ```bash
  git add .
  git commit -m "<message>"
  git push origin main
  heroku create <app name>
  git push heroku main
  heroku ps:scale web=1
  ```

* Be sure to update the requirements file as you go if you add new libraries.

### Tracking with Google Analytics

To track with Google Analytics, set up a new web property on Google Analytics, get the script, and paste it into the header tag in `index.py`.

```python
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Utilization Report</title>
        {%favicon%}
        {%css%}
        
        <!-- Global site tag (gtag.js) - Google Analytics -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=UA-151885346-2"></script>
        <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());

        gtag('config', 'UA-151885346-2');
        </script>

    </head>
    <body>
        <div></div>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
        <div></div>
    </body>
</html>
'''
```



