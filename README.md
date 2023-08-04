<h2 align="center">Tic Tac Toe on Pygame with an AI that has 3 levels of difficulty.</h4>
<h4 align="center">Game modes: Player vs Player or Player vs Computer. </h3>
<p align="center">
  <img width="712" alt="Screenshot 2023-07-26 at 19 58 47" src="https://github.com/CrisMorinaga/Tic-Tac-Toe/assets/128830239/d687bb51-0ddc-4ea4-aa06-1ae9ce21309a">
</p>

<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#understanding-the-code">Understanding the code</a>
</p>


## Key Features

* Player vs Player
  - Play against your friends or family.
* Player vs Computer
  - Play against the computer.
* Choose your difficulty
  - Choose between 3 levels of difficulty, easy, medium, or hard (being this last one configured for you to lose or tie).

## How To Use

Clone this repo, install the requirements, and run the project! Easy as that :)

## Understanding the code
After configuring all the user UI and sprites it was necessary to start making the required logic for the game to work properly. To achieve this objective 3 steps were followed: 

* First: The Coordinate System
  - A function was created which is able to read the real-time X and Y mouse position and assign a coordinate according to it. 
  
    ```Python
    def check_mouse_position():
      mouse_position = pygame.mouse.get_pos()
      mouse_position_game = []
  
      mouse_x = mouse_position[0]
      if mouse_x < 195:
          mouse_position_game.append(120)
      elif 205 < mouse_x < 395:
          mouse_position_game.append(300)
      elif 405 < mouse_x < 595:
          mouse_position_game.append(480)
  
      mouse_y = mouse_position[1]
      if mouse_y < 195:
          mouse_position_game.append(120)
      elif 205 < mouse_y < 395:
          mouse_position_game.append(300)
      elif 405 < mouse_y < 595:
          mouse_position_game.append(480)
  
      return mouse_position_game
    ```

    
    > **Note**
    > ...

* Check win, lose, or draw states:
  - ...
 
* AI brain:
  - The AI behavior is relatively easy to understand. First, it was necessary for the AI to understand what it should do, when it should do it, and where. This might sound obvious but, AI doesn't have eyes like us... so it doesn't know which coordinate is empty, which is not, or which coordinate should it use to be able to win if needed.

## You may also like...

- [SmartBrain](https://github.com/CrisMorinaga/SmartBrain) - A website that uses Clarifai API to scan an image URL and detect faces on it.

---

> Linkedin [@Cristopher Morales](www.linkedin.com/in/cristopher-morales-c)

