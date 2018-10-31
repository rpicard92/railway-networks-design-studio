# railway-networks-webgme-app

## What: 
1. This is a railway-networks-plugin for webgme that traverses through the tree stuctures and saves various infomation in an (.zip) artifact

## When:
1. Last Updated: 2018-10-30
2. First Started: 2018-10-30

## Why:
1. EECE-6833-01: Model-Integrated Computing class at Vanderbtilt University for MiniProject2

## Who: 
1. Developed for EECE-6833-01: Model-Integrated Computing class at Vanderbtilt University

## How:
1. Install dependencies:
    - a. Node.js (version >= 6)
    - b. MongoDB Community Server (version >= 3.0)
    - c. Git (must be available in PATH)
    - d. Python 3.X
2. Install webgme-cli globally with: "npm install -g webgme-cli" 
3. Start MongoDB with: "mongod --dbpath ~/data" (note: you may have to add this to the evniroment variables path)
4. Create a directory and in it run Git Bash: git clone https://github.com/rpicard92/railway-networks-webgme-app.git
5. Run: "npm install"
6. Run: "npm start"
7. Navigate to "http://localhost:8888" from a web browser
8. Create and import project: "rpicard92+RailwayNetwork_2cbd36.webgmex" located in the top directory of this project
9. Select the root node in the composition tab (i.e. click the background background). 
10. Under the property editor on the lower right, click "Meta", and choose the plugin named "MiniProject2Plugin" from the "validPlugins" field.
11. In the upper left click the play buttion (i.e. execute button), and click "MiniProject2Plugin", then "Run..." on the popup dialog.
12. Please note that it will take approximately 140 seconds to run the plugin. After it it finished you will be able to click show results and retrieve the (.zip) artifact with two JSON files.



