# Definition
On start game it opens window. Window is filled with green background, black obstacles and 4 tanks. 

##### First tank
First tank is player, it has normal size and normal speed. 

##### Other tanks
Three other tanks are enemies. 
- First enemy has bigger then normal size and slower speed. 
- Second enemy has smalled then normal size and a bit faster then normal speed.
- Third  enemy tank has normal size and a bit slower speed.

Each of four tanks have collision with obstacles, borders and with other tanks. 

###### Player controls
Player can control his tank with arrows, each arrow moves tank in his direction. Player can shoot if he press space each 3 seconds, if 3 seconda haven't pass yet, his tank should do nothing.

###### Enemy controls
Enemy tanks are controlled by logic, future named by tank AI. 
- Tank AI for first enemy tank moves it directly to player tank, goes around obstacles and shoot each 3 seconds. 
- Tank AI for second enemy tank moves it same horizontal position as player tank, and vertical position 200 pixels away from player tank, then shoot each 5 seconds.
- Tank AI for last enemy tank moves it same vertical position as player tank, and horizontal position 100 pixels away from player tank, then shoot each 3 seconds.

Shoot action from any tank create bullet with fixed for all bullets speed and direction same as where it was shoot. If bullet hit obstacle or border it explode. If hit any tank it explode and subtract tank health.

Explode action from bullet create orange circle for 3 seconds on position where bullet hit the object, after 3 seconds explosino disapear.

- Player win when he kill all enemy tanks, on the middle of the screen appears YOU WON blue text.
- Player loose when his health falls below zero, on the middle of the screen appears YOU LOOSE red text.
#### Extra functionality
- Different levels with random obstacles and growing game speed
- Randomly spawned power-ups for player tank
# Code
## Blocks:
- OBJECTS : declaration of main object (main tank, enemy tanks)
- UTILITY FUNCTIONS : functions that we will use for general logic, for calculations, etc

- (BULLET LOGIC IS ALMOST DONE) BULLET LOGIC : bullet takes parent direction and moves in that direction till hits something (tank, obstacle, border) ; on hit - bullet create explosion object ; for each bullet object make animation (should be one function)

- (EXPLOSION LOGIC IS DONE) EXPLOSION LOGIC : explosion is simple object of 2 values(time created ; position), position is calculated used parent bullet position and parent bullet size ; for each explosion object make animation with verification, if object was create more then 3 seconds before current time - delete that object
- PLAYER TANK LOGIC : 
	- move main tank to 4 directions, take care about collision with border and obstacles list ( `obstacles = [rectValues, rectValues, rectValues]`), rect values is `rectValues = ((xPosition, yPosition), ((xSize, ySize))` ;
	- player can shoot once per 2 seconds creating bullet object and adding this object to bullets list (bullets animation and logic is handled in bullet logic block)
- ENEMY TANKS LOGIC :
	- tank 1 (FAT TANK) : 3x normal health ; 0.6x normal speed ; 1.5x normal size ; AI - move the simplest way to player tank and maybe shoot
	- tank 2 (SPEED TANK) : 0.5x normal health ; 1.4x normal speed ; 0.75x normal size ; AI - move behind player tank, stand 100 pixels away and shoot (can shoot each 2 seconds);
	- tank 3 (NORMAL TANK) : 1x normal health ; 0.9x normal speed ; 1x normal size ; AI - move to player, stop if vertical/horizontal distance <= 100 pixels and shoot (can shoot each 2 seconds)
- GAME EVENTS LOGIC :
- start game screen without any tank (only obstacles) and big text START GAME
- on SPACE key press - clear START GAME text and start player, enemy tanks logic
- end game - call if player health <= 0 (loose screen) **OR** all enemy tanks are dead (win screen)
- win screen - YOU WON text on screen, wait 5s and exit
- loose screen - YOU LOOSE text on screen, wait 5s and exit
