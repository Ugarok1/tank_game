# Idea
- There're 4 tanks ; 1 player tank ; 3 enemy tanks (slow but big health, fast but low health, almosst same speed as player, same health as player) 
- Player need to shoot enemies till they die (health <= 0) ; shooting on space ; bullets explode on collision with obstacles/borders/tanks (if with tanks - minus tank health)
- Player wins if he kills all tanks ; player loose if his health falls below 0, touch any enemy tank set health to 0
##### Note
if have a lot of time:
- enemy tanks can shoot
- different levels with acceleration of the whole game (enemy tank speed, player speed, bullet speed)
# Code
## Blocks:
- OBJECTS : declaration of main object (main tank, enemy tanks)
- UTILITY FUNCTIONS : functions that we will use for general logic, for calculations, etc
BULLET LOGIC IS ALMOST DONE
- BULLET LOGIC : bullet takes parent direction and moves in that direction till hits something (tank, obstacle, border) ; on hit - bullet create explosion object ; for each bullet object make animation (should be one function)
EXPLOSION LOGIC IS DONE
- EXPLOSION LOGIC : explosion is simple object of 2 values(time created ; position), position is calculated used parent bullet position and parent bullet size ; for each explosion object make animation with verification, if object was create more then 3 seconds before current time - delete that object
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
