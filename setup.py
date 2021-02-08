from setuptools import find_packages, setup

setup(
    name='covid19python-thomaswoehlke',
    version='0.0.14',
    packages=find_packages(),
    url='ttps://github.com/thomaswoehlke/covid19python.git',
    license='GNU General Public License v3.0',
    author='Thomas Woehlke',
    author_email='thomas.woehlke@gmail.com',
    description='Covid19 Data Aggregation - also a Project to learn Python Flask, SQLAlchemy, Celery et al.',
    install_requires=[
        "setuptools==53.0.0",
        "pip==21.0.1",
        "pip-licenses==3.3.0",
        "wheel==0.36.2",
        "dash>=1.19.0",
        "dash-extensions>=0.0.45",
        "dtale>=1.33.1",
        "wget>=3.2",
        "celery[redis]>=5.0.5",
        "Flask>=1.1.2",
        "Flask-SQLAlchemy>=2.4.4",
        "SQLAlchemy>=1.3.23",
        "psycopg2>=2.8.6",
        "#Flask-Authorization>=1.4",
        "Flask-Multipass>=0.3.3",
        "Flask-Cors>=3.0.10",
        "Flask-BS4>=4.5.3.0,<5.0.0.0",
        "test-flask>=0.2.0",
        "pytest-flask>=1.1.0",
        "Flask-Admin>=1.5.7",
        "Flask-Redisboard>=0.2.0",
        "Flask-Monitoring>=1.1.2",
        "flask-healthz>=0.0.2",
        "Flask-DB>=0.3.0",
        "flask-pwa>=0.1.0",
        "Flask-Moment>=0.11.0",
        "Flask-CKEditor>=0.4.4.1",
        "flask-checkr>=0.1.2",
        "flask-whooshalchemy3>=0.2.0",
        "Flask-PluginKit>=3.6.0",
        "Flask-ResponseBuilder>=2.0.12",
        "flask-was>=0.1.0",
        "Flask-GraphQL>=2.0.1",
        "flask-hintful>=0.0.7",
        "Flask-Caching>=1.9.0",
        "flask-roles>=0.5",
        "Flask-Babel>=2",
        "Flask-Login<0.6.0,>=0.5.0",
        "manual-sitemap>=19.6.0",
        "aiocronjob>=0.2.0",
        "npmdownloader>=1.2.1",
        "pyecharts>=1.9.0",
        "pyecharts-extras>=0.0.5",
        "reactive-pyecharts>=1.0.0",
        "visdom>=0.1.8.9",
        "tokenize-rt>=4.1.0",
        "pynndescent>=0.5.1",
        "torch>=1.7.1",
        "numpy>=1.19.0",
        "pandas>=1.1.0",
        "scipy>=1.5.0",
        "StatisticalDiagrams>=20.5",
        "PyGObject>=3.38.0",
        "gaphor>=2.2.1",
        "sphinx==3.4.3",
        "sphinx-tabs==2.0.0",
        "sphinx-issues==1.2.0",
        "pallets-sphinx-themes==1.2.3"
    ],
    extras_require={"dotenv": ["python-dotenv"]},
)
