# Registering Open Source Models to SAS Viya from SAS Viya Workbench

If you have ever registered an open source model from your own personal machine into SAS Viya, then you'll find the process to be identical. 
There is nothing special that you need to do differently from a code perspective: as long as SAS Viya Workbench can talk to your SAS Viya Server, 
then you can register the model the same way you have always done. 

In fact, this code will run both on your local machine **or** SAS Viya Workbench.

This project runs through an example where we:

* Build an XGBoost model on HMEQ
* Write all the files necessary for SAS Model Manager using [sasctl](https://sassoftware.github.io/python-sasctl/api/sasctl.html) and [pzmm](https://sassoftware.github.io/python-sasctl/api/sasctl.pzmm.html)
* Register the model to SAS Model Manager

## Folders
**model**: All model files needed for SAS Model Manager and a zip of these files that you can upload directly to it

## Data
[hmeq.csv](https://support.sas.com/documentation/onlinedoc/viya/examples.htm)

## Requirements
[requirements.txt](./requirements.txt)

## Expected directory structure:

- **Data**: `/workspaces/myfolder/data`
- **Model**: `/workspaces/myfolder/models`
