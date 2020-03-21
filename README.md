# MediaSubmissionsDownloaderForReddit

This script allows you to download your saved reddit submission that are media files. It can handle links to imgur images and albums, gfycat links and direct links to media files.

## Getting started

### Dependencies
Install dependencies using pip:
```
pip3 install -r requirements.txt
```

### Usage

#### Registering script on reddit
Before you will be able to run the script, you have to register a script app on your reddit account. This will give you the reddit client id and secret that have to be provided when running the script.

#### Registering imgur application  
You will also need imgur's client id which can be obtained by registering the application on the imgur's website.

#### Running the script
When running the script you have to provide required parameters. These can be passed as arguments or in `config.ini` file. 

An example of running the script by providing all parameters as arguments:
```
E:\MediaSubmissionsDownloaderForReddit\python src --imgur-client-id <IMGUR_CLIENT_ID> -reddit-client-id <REDDIT_CLIENT_ID> --reddit-client-secret <REDDIT_CLIENT_SECRET> --reddit-username <REDDIT_USERNAME> --reddit-password <REDDIT_PASSWORD>
[+] User: Ph0ndragX
[+] Loaded 100 submissions.
[+] Submissions will be saved to: output
[+] Starting submissions download.
[+] 100 submissions will be downloaded.
```

An example of running the script when all required parameters are provided in `config.ini` file.
```
E:\MediaSubmissionsDownloaderForReddit\python src
[+] User: Ph0ndragX
[+] Loaded 100 submissions.
[+] Submissions will be saved to: output
[+] Starting submissions download.
[+] 100 submissions will be downloaded.
```

It is possible to provide some parameters as arguments and other in `config.ini` file. 

## Licensing:
MediaSubmissionsDownloaderForReddit is licensed under the [GNU v3 Public License.](https://opensource.org/licenses/GPL-3.0)
