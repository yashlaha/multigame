# multigame


### To run the game , clone the repository and open command window in the root folder (assuming that django/python is setup and installed in the PC)
### go into the multigame folder using the command and then run the command <b> python manage.py runserver 127.0.0.0:8000 </b>
### app willl be up and running on your ipserver on the link "ipaddress/game". for eg : 192.168.1.105:8000/game
### other users can now join the game at this ip address.

##### The Game starts with the home screen where person can either start the game or join an existing Game.
##### The onne who creates the game can choose the grid size.
##### The maximum number of limit is set to 4 persons per game.
##### Whenever the two persons join a game the game starts automatically the screen is locked for 10 seconds and then open up again for the users to click the box and the person to click first acquires that block and then the screens are again locked for 10 seconds and the scores are updated again.
##### If the user leaves the game he has to join as a new user and cannot continue with the last game. 
##### If the 2 players are already playing the 3rd user joins game only when the arena becomes active so as to keep the game in sync.
##### Every user that joins is assigned random color.
##### Game ends when all the grids are colored and the final scores are displayed on the screen.
