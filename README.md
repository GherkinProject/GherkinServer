Welcome to Gherkin Project.
This is the server package to install Gherkin server.


### Requirements

Before the installation you must have the following packages.

1. Debian system

2. Python (>= 2.5)

3. Gstreamer

        sudo apt-get install python-gst0.10

4. Mutagen

        sudo apt-get install python-mutagen

You can install gherkin in your system or just use the python file:

### Direct use

To launch from lib:

    python src/start_server.py

### Real install

To install gherkin:

    sudo sh installServer.sh

Then, To launch program:

    ghk-server &

To remove gherkin:

    sudo sh removeServer.sh

### Database Mgmt

You can add files to your database directly in commandline.
If you prefer using a Gui, install the GherkinUi and use it in 'localhost'.
Otherwise, you can scan your db with the following commands:

1. Make files executable OR just use 'python' before the next steps commands:

        sudo chmod ug+x /usr/local/ghk-server/*_db.py

2. Scan your library:

        /usr/local/ghk-server/generate_db.py /absolute_path

Warning: this may take a long time

3. Adding other paths:

        /usr/local/ghk-server/update_db.py /absolute_path
