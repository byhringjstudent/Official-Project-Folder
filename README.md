**********************
Firing up the Web App!
**********************

Ports List:
3000, 3001, 5000, 5173

1. cd into Frontend
run "Python Flask_App.py"

2. cd into Backend
run "npm run dev"

3. cd into RagieBot
run "npm run dev -- -p 3001" not? 3000

** ready to run our webhook in the terminal?
** You do not need to generate a new webhook 
every time we reboot the app, this is the
purpose of our ngrok reserved domain. **

4. Open a separate terminal
Run this command inside your terminal to fire up the webhook
run "ngrok http --domain=sunbird-full-fully.ngrok-free.app 3000"
