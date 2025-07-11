Test urls:
- https://entraide-internationale.fr/IMG/xml.php?a=
- https://www.google.com
- http://testsafebrowsing.appspot.com/s/malware.html

Deployment command: gcloud run deploy url-checker   --source=.   --region=us-central1   --allow-unauthenticated  --port 8080