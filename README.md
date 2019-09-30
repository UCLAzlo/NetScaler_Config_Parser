# NetScaler_Config_Parser

This project uses a Node.js server to provide access to a Python script which can group NetScaler vServers, Service Groups, and Servers in a CSV formatted output. The purpose of this is to easily identify and find any NetScaler object and it's related dependencies to be used for documentation purposes.

To run this project, clone this github repo and run the following:
  run npm install
  node ns_config_parser.js
*Note there is a dependency on python3 being an accessible command. So as to spawn the Parser written in Python

After the server is running, you can access the Python Config Parser via either option below:
- Use a Web Browser to access the running instance of Node at the root path ("localhost/"). Then you can paste the configuration file into the text area and press submit to receive the parsed version.
- Use a tool like Postman to POST directly to the config path ("localhost/config"). Put the original NetScaler configuration file as the body of the POST. The response body will be the CSV formatted output.
  
  
