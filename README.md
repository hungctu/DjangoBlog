# DjangoBlog
This is a website that I coded for the purpose of practicing the django framework that I am learning and researching

The website is built with some basic functions such as:
* Creating and writing user-created stories
* Managing accounts
* Managing user stories
  

## Tech Used
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white) ![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white) ![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white) ![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E) ![MySQL](https://img.shields.io/badge/mysql-%2300f.svg?style=for-the-badge&logo=mysql&logoColor=white) 


## How to Use

To install and run the website, you can follow these steps:

1. Clone the repository from GitHub.
2. Open the project in your IDE.
3. Install the dependencies: `pip install -r requirements.txt`
4. In settings.py at the Database you edit (mysql workbench):
   * 'NAME': "name",
   * "USER": "username",
   * "PASSWORD": "password",
   * "HOST": "host",
   * "PORT": "port",
5. Create a database and run the migrations:
   * `python manage.py makemigrations`
   * `python manage.py migrate`
6. Create a superuser: `python manage.py createsuperuser`
7. Run the development server: `python manage.py runserver`


## Reference material
You can visit <https://docs.djangoproject.com/en/4.2/ref/databases/> for instructions on connecting the right database to your database
