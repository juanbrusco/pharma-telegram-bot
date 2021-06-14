### API Rest for https://farma-salto.web.app       
- Python 3.8        

## Telegram Bot     
- library: <https://github.com/python-telegram-bot/python-telegram-bot>     
- first example: <https://tecnonucleous.com/2021/04/04/como-crear-nuestro-bot-de-telegram-con-python/>      
- deploy: <https://github.com/python-telegram-bot/python-telegram-bot/wiki/Hosting-your-bot>                
- python anywhere:          
    - go to pythonanywhere and open bash console     
    - open project folder and pull the changes      
    - set new env variables (export ...)        
    - install dependency pip3 install --user python-telegram-bot       
    - go to /pharma-admin-api/pharmacies_app and run `screen -S mybot`          
    - then run `python3 telegram_bot.py`        
    - detach from the screen by holding CTRL and pressing A, then D    
    - go to pythonanywhere dashboard/webapp and restart the app     
- heroku:       
    - <https://elements.heroku.com/buttons/anshumanfauzdar/telegram-bot-heroku-deploy>        
    - 1. Create "Procfile" with next content: `worker: python telegram_bot.py`              
    - 2. Create runtime.txt with next content: `python-3.8.5`             
    - 3. Heroku configuration. On terminal run:        
        `heroku login`      
        `heroku create <nombre de tu aplicación heroku>`        
        `heroku git:remote -a <nombre de tu aplicación heroku>`     
        `git push heroku branch_to_deploy:master`      
    - `heroku ps:scale worker=0`        
    - `heroku ps:scale worker=1`        

## Conda virtual environments 
See this [reference](https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/20/conda/) to learn more about Conda virtual environments. There is always a default virtual environment called `base`. **One should not work in that environment**. 

To build the virtual environment for the Python project oss-reporting, first navigate to that folder after cloning the git repository. 

**First time virt-env creation using .yml file** : To create the virtual environment corresponding to an environment.yml file in the repository, run the command below. The name of the environment is encoded inside the .yml file. The command will create the virtual environment (a folder by that name inside the Miniconda installation directory) and install Python packages required to run the code.
1. `conda update conda`
2. `conda env create -f environment.yml`  
The first command simply ensures you have the latest conda, which the miniconda installer may not have installed. The second command creates the Conda virtual environment `ossreporting`.

**Steady state work in a virt-env** : once the Conda virtual environment is created (first time, above), run the command
* `conda activate telegram_bot_env`  
to switch to that environment and have access to the required Python packages, when working on your project which requires that virtual environment.        

#### How To Keep Your Free Heroku App Alive and Prevent It From Going to Sleep      
1- <https://medium.com/better-programming/keeping-my-heroku-app-alive-b19f3a8c3a82>        
2- <https://github.com/jcarras/rise-and-shine>       