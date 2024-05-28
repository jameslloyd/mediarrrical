# mediarrr_ical

If you dont want to expose your mediarrr apps to the internet, but want to view the ical info in google calendar (or similar). This will combine the ical data from multiple apps and upload to an S3 / B2 bucket.



## Docker Config
ENVs need setting

```
B2KEYNAME
B2KEYID
B2KEY
B2ENDPOINT
```

and /app/config needs mounting to a folder containing a single file config.txt.  config.txt you should populate with a list of the ical urls to merge, each on separate lines.

### Example 
  
  docker run -d --name mediarrr_ical -e TZ=Europe/London -e B2KEYNAME=<**REPLACE WITH BUCKETNAME**> -e B2KEYID=<**REPLACE WITH KEYID**> -e B2KEY=<**REPLACE WITH KEY**> -e B2ENDPOINT=<**REPLACE WITH S3/B2 ENDPOITN**> -v <**REPLACE WITH LOCAL CONFIG FOLDER**>:/app/config jameslloyd/mediarrrical
