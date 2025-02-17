# Deployment

- The app was deployed to [Heroku](https://www.heroku.com/).
- The database was deployed with [PostgreSQL](https://www.postgresql.org/).

- The app can be reached by the [link](https://fitsphere-5231c1c191f7.herokuapp.com/).

---

# Deployment Guide

## Local Deployment

*Note:*  
Ensure you have all necessary dependencies installed by running the following command:

```bash
pip3 install -r requirements.txt
```

1.  **Install the dependencies:**

    -   Open the terminal window and type:
    - `pip3 install -r requirements.txt`

    bash

    Copy code

    `pip3 install -r requirements.txt`

2.  **Create a `.gitignore` file** in the root directory of the project to prevent the exposure of your secret data. You should add `env.py` and `__pycache__` files.

3.  **Create a `.env` file.** This will contain the following environment variables:

    python

    Copy code

    ```python
    import os

      os.environ['SECRET_KEY'] = 'Add a secret key'
      os.environ['DATABASE_URL'] = 'will be used to connect to the database'
      os.environ['DEBUG'] = 'True'
    ```

    *During the development stage, `DEBUG` is set to `True`, but it is vital to change it to `False` for production.*

4.  **Run the following commands in the terminal to make migrations:**

    bash

    Copy code

    `python3 manage.py makemigrations
    python3 manage.py migrate`

5.  **Create a superuser to get access to the admin environment:**

    bash

    Copy code

    `python3 manage.py createsuperuser`

    Enter the required information (username, email, and password).

6.  **Run the app with the following command:**

    bash

    Copy code

    `python3 manage.py runserver`

7.  **Open the link provided in the terminal in your browser** to see the app.

8.  **If you need to access the admin page:**

    -   Add `/admin/` to the link provided.
    -   Enter your username and password (for the superuser you created).
    -   You will be redirected to the admin page.

* * * * *

Heroku Deployment
-----------------

1.  **Set up a local workspace on your computer for Heroku:**

    -   Create a list of requirements that the project needs to run:

    bash

    Copy code

    `pip3 freeze > requirements.txt`

    -   Commit and push the changes to GitHub.
2.  **Go to www.heroku.com**\
    Log in or create a Heroku account.

3.  **Create a new app on Heroku**\
    Create a new app with any unique name `<name app>`.

    ![Heroku. Create New App](documentation/deployment/new-heroku.png)

4.  **Create a Procfile in your local workspace**\

![Heroku. Procfile](documentation/deployment/procfile-heroku.png)

    This file will will contain the following:
    ```python
        web: gunicorn <name app>.wsgi:application
    ```

    -   Commit and push the changes to GitHub.
5.  **Go to resources in Heroku** and change the dyno to the free version.

![Heroku. Dyno](documentation/deployment/dyno-heroku.png)

6.  **Go to the settings app in Heroku and navigate to Config Vars**

![Heroku. Settings](documentation/deployment/settings-heroku.png)

    Click on "Reveal Config Vars" and add the following config variables:

    | Key | Value |
    | --- | --- |
    | DATABASE_URL | ... |
    | DISABLE_COLLECTSTATIC | 1 |
    | SECRET_KEY | ... |

7.  **Copy the value of `DATABASE_URL` and input it into the `.env` file.**\
    Generate a secret key (you may use Djecrety for secret key generation).

9.  **Migrate changes.**

10. **Set debug to `False` in `settings.py`.**

11. **Commit and push the changes to GitHub.**

12. **Connect your repository to Heroku.**

![Heroku. Connect to Heroku](documentation/deployment/repo-heroku.png)

1.  **Deploy the app to Heroku** by clicking "Deploy Branch" button. If you want to enable auto-deployment, click "Enable Automatic Deployment".

The deployment process will start.

![Heroku. Deploy to Heroku](documentation/deployment/deploy-heroku.png) 

Click "View build logs" to see the progress of the deployment.

![Heroku. Deploy to Heroku](documentation/deployment/build-log-heroku.png)

*Due to security updates, Heroku dashboard will not allow you to deploy your app from GitHub. Thus, you need to run the following commands in your terminal:*

| Action | Terminal Command | Comment |
| --- | --- | --- |
| Login to your Heroku account | `heroku login -i` |  |
| Create a new app on Heroku | `heroku create NAME-OF-YOUR-APP` | If you haven't created the app before, you can access the app via the Heroku dashboard and set up your config vars. |
| Add remote to your local repository | `heroku git:remote -a NAME-OF-YOUR-APP` | If you've already created the app on Heroku (before the security updates) and connected it using the Heroku dashboard. |
| Deploy new version of the app | `git push heroku main` |  |
| Rename app | `git remote rename NAME-OF-YOUR-APP NAME-OF-YOUR-APP-2` |  |

* * * * *

Final Deployment
----------------

1.  **Set `DEBUG` to `False` locally** and delete `DISABLE_COLLECTSTATIC` from config vars in Heroku dashboard.

2.  **Commit and push the changes to GitHub.**