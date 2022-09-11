To run this program:

Navigate to the folder where you saved this project, then run the following command:

```
python main.py
```

Before you can do that, you need to install all of the required software listed below.

In order to run this program, first install the following software packages on your computer:

Step (0): Open a terminal.

Follow one of the methods shown in this video to open your terminal:

```
https://www.youtube.com/watch?v=8OFD_F5L_vk&ab_channel=Chris%27Tutorials
```

Step (1): Install homebrew.

Homebrew is a package manager for Apple. It makes it easy to install software with simple commands.

In your terminal, copy the following commands, then hit enter to execute one at a time.

```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

```
export PATH="/usr/local/opt/python/libexec/bin:$PATH"
```

Step (2): Install python.

```
brew install python
```

Check that python 3 was installed correctly:

```
python --version
```

Step (3): Install selenium.

```
pip install selenium
```

Step (4): Install Chrome Driver.

```
pip install webdriver-manager
```

Step (5): Install the Google Client library.

```
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```
