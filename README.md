# TechConf Registration Website

## Project Overview
The TechConf website allows attendees to register for an upcoming conference. Administrators can also view the list of attendees and notify all attendees via a personalized email message.

The application is currently working but the following pain points have triggered the need for migration to Azure:
 - The web application is not scalable to handle user load at peak
 - When the admin sends out notifications, it's currently taking a long time because it's looping through all attendees, resulting in some HTTP timeout exceptions
 - The current architecture is not cost-effective 

In this project, you are tasked to do the following:
- Migrate and deploy the pre-existing web app to an Azure App Service
- Migrate a PostgreSQL database backup to an Azure Postgres database instance
- Refactor the notification logic to an Azure Function via a service bus queue message

## Dependencies

You will need to install the following locally:
- [Postgres](https://www.postgresql.org/download/)
- [Visual Studio Code](https://code.visualstudio.com/download)
- [Azure Function tools V3](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=windows%2Ccsharp%2Cbash#install-the-azure-functions-core-tools)
- [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest)
- [Azure Tools for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-vscode.vscode-node-azure-pack)

## Project Instructions

### Part 1: Create Azure Resources and Deploy Web App
1. Create a Resource group
2. Create an Azure Postgres Database single server
   - Add a new database `techconfdb`
   - Allow all IPs to connect to database server
   - Restore the database with the backup located in the data folder
3. Create a Service Bus resource with a `notificationqueue` that will be used to communicate between the web and the function
   - Open the web folder and update the following in the `config.py` file
      - `POSTGRES_URL`
      - `POSTGRES_USER`
      - `POSTGRES_PW`
      - `POSTGRES_DB`
      - `SERVICE_BUS_CONNECTION_STRING`
4. Create App Service plan
5. Create a storage account
6. Deploy the web app

### Part 2: Create and Publish Azure Function
1. Create an Azure Function in the `function` folder that is triggered by the service bus queue created in Part 1.

      **Note**: Skeleton code has been provided in the **README** file located in the `function` folder. You will need to copy/paste this code into the `__init.py__` file in the `function` folder.
      - The Azure Function should do the following:
         - Process the message which is the `notification_id`
         - Query the database using `psycopg2` library for the given notification to retrieve the subject and message
         - Query the database to retrieve a list of attendees (**email** and **first name**)
         - Loop through each attendee and send a personalized subject message
         - After the notification, update the notification status with the total number of attendees notified
2. Publish the Azure Function

### Part 3: Refactor `routes.py`
1. Refactor the post logic in `web/app/routes.py -> notification()` using servicebus `queue_client`:
   - The notification method on POST should save the notification object and queue the notification id for the function to pick it up
2. Re-deploy the web app to publish changes

## Monthly Cost Analysis
-- My Account is on a Pay as you go subscription 
Complete a month cost analysis of each Azure resource to give an estimate total cost using the table below:

| Azure Resource                        | 	Service Tier                          		| Monthly Cost (USD)		|
|-------------------------------------------------------------------------------------------------------------------

|  *Azure Postgres Database*            |   Basic (Single instance, single core)		|   25.32      				|

|  *Azure Service Bus*   				|   Basic          								|	0.05					|

|  *Azure Function App*                 | 	Azure Function Consumption plan for Linux	|   13			       		|  
 
|  *Azure Web App *                		| 	App service Plan (F1: Free)        			|   0          			 	| 

|  *Azure Storage Account *             |  General Purpose 	V2 LRS      				|   21          			| 

Azure Storage Account amount Estimated via Azure pricing page 

## Architecture Explanation
This is a placeholder section where you can provide an explanation and reasoning for your architecture selection for both the Azure Web App and Azure Function.


Azure Web App Architecture

The web app  - 
1. A managed platform as a service azure web app approach is chosen for deploying the   web app. It is easy to deploy and choose the specific run time environments e.g language, server os type. This is a lightwweight service that doesnt need heavy compute resource. With a change in pricing tier we can verticaly scale the amount of resources assigned e,g ram & cpu while comfortably maintaing good levels of support. Were it a resource intensive web app I would have chosen a VM deployment approach.
2. With  app service approach one is able to set the amount of hardware and app service plan which allows for cost control.  The free option within Dev/Test is chosen for this exercises. Other plans available include production and isolated.
3. High availability and autoscaling is also supported.
4.  

ou can set the amount of hardware allocated to host your application, and cost varies based on the plan you choose. There are three different tiers

Platform as a Service (PaaS) that allows a developer to focus on the application while Azure takes care of the infrastructure.

Funtion App - Function as a service approach
1. The function app will be ran as a managed service which leaves us to concentrate on building the business logic instead of managing servers.It is better than managing our own infrastructure which is mostly not fully utilised most of the times. 
2. The function app approach is an on demand approach serverless approach which enables us to configure specific bits of code to run in response to specific events making for efficient computing. Each function app service endpoint responds to triggers from events. 
An azure funtion app allows us to use an event based approach where a trigger fires an action using very little code. 
	In our case we are able to trigger a send email action every time a valid message is put on the configured notification queue in the service bus.The message is a notification message id which is then used to fetch the actual message  from the database and send it to all conference attendees after customizing the subject.
3. Since the subscription account is a pay as you go Account , a consumption app plan will work well in this set up since we only only charges for the runtime of our function app, and includes some free time per Azure subscription.
4. The fucntion app approach makes it easy to break down functionality to specific APIs which are easy to deploy by uploading code or containers through azure cli or via VScode plugins
