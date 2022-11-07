Check考 https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-programming-environment-on-an-ubuntu-22-04-server Setting虚拟环境

Step 1 — Setting Up Python 3,
1,  Ubuntu 22.04 and other versions of Debian Linux ship with Python 3 pre-installed. To make sure that your versions are up-to-date, update your local package index:

    sudo apt update
2,  Then upgrade the packages installed on your system to ensure you have the latest versions:

    sudo apt -y upgrade
3,  Check the version of Python 3 that is installed

    python3 -V
4,  Install pip, a tool that will install and manage programming packages we may want to use in our development projects.

    pip -V
    sudo apt install -y python3-pip
5,  There are a few more packages and development tools to install to ensure that you have a robust setup for your programming environment:

    sudo apt install -y build-essential libssl-dev libffi-dev python3-dev

Step 2 — Setting Up a Virtual Environment
1,  While there are a few ways to achieve a programming environment in Python, we’ll be using the venv module here, which is part of the standard Python 3 library. Let’s install venv by running the following:

    sudo apt install -y python3-venv
2,  Create a new directory with mkdir

    mkdir .venv
3,  Navigate to the directory where you’ll store your programming environments:

4,  create an environment by running the following command:

    python3 -m venv .vnev
5,  To use this environment, you need to activate it, which you can achieve by typing the following command that calls the activate script:

    source .venv/bin/activate


  /*
    Breakpoint	    Class infix	      Dimensions
    X-Small	        None	            <576px
    Small	          sm	              ≥576px
    Medium	        md	              ≥768px
    Large	          lg	              ≥992px
    Extra           large	xl	        ≥1200px
    Extra           extra large	xxl	  ≥1400px
  */



pip freeze > requirements.txt

flask shell