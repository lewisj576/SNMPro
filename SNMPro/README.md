# SNMPro
SNMPro is a standalone Python application which combines supervised regression algorithms (LR, RF, SVM) with periodically collected SNMP data to make accurate predictions on future network performance.

*** PLEASE ENSURE FOLLOWING DEPEDENCIES ARE INSTALLED ***
customtkinter, pandas, mysql-connector-python, numpy, scipy, scikit-learn, pysnmp

**** IMPORTANT ******
RUN main.py
sign-up to create a new account, or login to the test account (username: admin, password: admin) *note* if you sign up, you will not have access to dataset used in the thesis experiment, and will have to collect your own.
To utilize SNMPro's data collection functionality, a device on your LAN must be configured with SNMP and the IP address, port number (default '161'), and community string (default 'public') must be known.
Use either the 'fetch SNMP object' page to get single SNMP objects or the 'fetch periodic data' page to collect large scale dataset for training.

IF YOU ARE NOT COLLECTING YOUR OWN DATA, THEN SIGN INTO THE ADMIN ACCOUNT FOR TESTING MENTIONED ABOVE AND USE THE MACHINE LEARNING PAGE TO LOAD THE DATASET, SELECT PREPROCESSING TEHCNIQUES, SELECT RESPONSE VARIABLES, AND SELECT A REGRESSION ALGORITHM.


Once the model is trained the MAE and RMSE values for the evlated model will be printed in terminal. If you are happy wit the model, you can save it and load it using the generate predictions page, to predict future network bahaviour based on your trained model.
