pip install -r requirements.txt
pytest --alluredir=allure_report
allure serve allure_report
#open the allure server in local browser