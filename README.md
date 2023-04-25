# Anime Update (Anime Search/Chat Room Webapp) by Andre Eastwood
#### Video Demo:  https://youtu.be/LWJzKUegfpk
#### Description:
AnimeUpdate is a webapp that basically is a chat room which allows users to be able to communicate in a sitewide open chat.

This allows any user the ability to be heard by anyone and join in on current topics being discussed. Users can share their excitement for upcoming, airing, and past anime. For a casual anime watcher this can help them build a “to-watch” list based on it’s buzz. The AnimeUpdate webapp also allows the user the ability to search for any anime by title and get a summary of anime's plot and view the available poster provided by an api. The app queries the api for a particular anime’s title which it in returns an xml file. The app then parses the xml file for the required details to be displayed to the user such as the name/title, poster, and plot/summary.

In the Projects folder you can find two folders (static and template) , two python files, an sqlite file and this readme.
Please see breakdown of file and folders located in the Project folder:
Static contains:
- Anime.ico - the icon utilized in the web browser’s tab (the title of the page)
- Anime_logo.png - the imaged displayed in the logo
- Shonen_jump.jpg - the image that is displayed in the landing page beside the login form
- Style.css – which is the styling sheet for the entire webapp

Templates contains all seven (6) html files that the user will interact with:
- Account.html – this page is used to display the user’s account details which they had entered in the initial signup page for new users. The user will also be able to update any detail of their profile/account of their choosing and this will be pushed to the database by clicking on the “update” button. They are also able to change their password by clicking on the “change password” (which carries them to password update page).
- Index.html – This page is the main/home page that the user is carried to once they are logged in. The user will be able to view the public chat and comment if they so wish to. They are also able search for anime from this page.
- Layout.html – This is the general layout of the webapp for how it’s pages will be displayed to the user.
- Login.html – This page/template will display the landing page that the user will be carried to once launching or visiting the webapp. This page allows the user to enter their username and password in order to gain access to the webapp. The user is also able to be carried to the registration page by selecting the “sign up” link.
- Password.html – The password template allows the user the ability to enter their new password and update the database.
- Registration.html – This is where the user would be redirected to from the login page to signup as a new user.

The project folder also contains the following files:

Added_code.py - this python file is used to handle http error when they are returned from the server and pushed it to the err_mesg function as well it contains the function used to check whether the user is logged into the webapp.
App.py – This file is the major application file as this contains most functions that governs the processed carried out by the webapp.
Database.db – this sql file stores all user data for the webapp and is manipulated by the app.py file.


#### Testing:

- You can create a user by clicking "New Otaku? Register Here!" link on the login page
- You can also leave a comment in the chat.
- You can also click "Account" to view the users account details and also update any detail of the account you would like.
- You can also click the "update password" button on the account page to allow you to change your current password.

Error Handling Tests:

- You can attempt to submit in the login form without entering a username or password.
- You can enter the incorrect password for the user on the login page.
- You can leave any requested details on the registration page blank.
- You can attempt to update your password by entering two different passwords on update password page.
- You can leave a field blank when submitting on the password page.

