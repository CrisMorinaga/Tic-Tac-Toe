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
  - A function was created which is able to read in real-time the value of X and Y according to the user mouse position and assign a coordinate to it. 
  
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
    
    ![CoordinateFunctionality](https://github.com/CrisMorinaga/Tic-Tac-Toe/assets/128830239/af63b3d0-263b-4a73-8530-ed7baba1e6a6)
    > **Note**
    > If the user places their mouse on top of any line the function will return only one coordinate, and as the code needs two coordinates to work, even if the user makes a click, the code won't register its click.

   - Every time the user clicks their right mouse that mouse coordinate is checked against the used_positions array. If the position is not found in it then it will be recorded on it and the user's turn will finish, otherwise, it won't register it and the user needs to click a new empty space, successfully avoiding the possibility of playing on the same spot more than once and preparing the game for the win, lose or tie logic.
     
     ```Python
      pos = check_mouse_position()
      [code...]
          elif player_vs_player:
            # Check for winning conditions, if nothing is found then the game continues
            if x_win is None and circle_win is None:
              if current_turn % 2 == 0:
                  # Assigns circle to player 2
                  shape = "circle"
              else:
                  # Assigns X to player 1
                  shape = "x"
              if pos not in used_positions and len(pos) > 1:
                  used_positions.append(pos)
                  current_turn += 1
                  if shape == "x":
                      x = X(100, x_pos=pos[0], y_pos=pos[1], line_width=5)
                      x_group.add(x)
                  else:
                      circle = Circle(75, 5)
                      circle.create_rect(x_pos=pos[0], y_pos=pos[1])
                      circle_group.add(circle)
      ```
  
* Second: Win, lose, or draw logic
  - Once the coordinate system is created and the used_positions array starts to become populated by coordinates, we need a way to check if the player using X or the player using Circles won. For this purpose, and knowing that a player needs to have made at least 3 movements to win, the check_winning_condition function is created.
    ```Python
    circle_group = pygame.sprite.Group()
    x_group = pygame.sprite.Group()
    [code...]
    def check_winning_condition(group, used_pos: list):
      if len(used_pos) >= 5:
          x_coordinate = Counter(form.rect.center[0] for form in group)
          y_coordinate = Counter(form.rect.center[1] for form in group)
          left_start_diagonal = [form for form in group if form.rect.center in [(120, 120), (300, 300), (480, 480)]]
          right_start_diagonal = [form for form in group if form.rect.center in [(120, 480), (300, 300), (480, 120)]]
  
          for y_coord, count in y_coordinate.items():
              if count == 3:
                  horizontal_line = draw_winning_line(screen, (25, y_coord), (575, y_coord))
                  return horizontal_line
  
          for x_coord, count in x_coordinate.items():
              if count == 3:
                  vertical_line = draw_winning_line(screen, (x_coord, 25), (x_coord, 575))
                  return vertical_line
  
          if len(left_start_diagonal) == 3:
              left_to_right_diagonal_line = draw_winning_line(screen, (25, 25), (575, 575))
              return left_to_right_diagonal_line
          elif len(right_start_diagonal) == 3:
              right_to_left_diagonal_line = draw_winning_line(screen, (575, 25), (25, 575))
              return right_to_left_diagonal_line
    ```

    With this, the base for the game is set and two users can start playing against each other. To finalize the project, an AI was created.
 
* Third: AI brain
  - The AI behavior is relatively easy to understand. First, it was necessary for the AI to understand what it should do, when it should do it, and where. This might sound obvious but, AI doesn't have eyes like us... so it doesn't know which coordinate slot is empty, which coordinate slot is being used, or which coordinate slot should it use to be able to win if needed.
  - To avoid making this readme longer than it should I will skip this section, if you are interested please feel free to contact me!

## You may also like...

- [SmartBrain](https://github.com/CrisMorinaga/SmartBrain) - A website that uses Clarifai API to scan an image URL and detect faces on it.

---

> Linkedin [@Cristopher Morales](https://www.linkedin.com/in/morales-cristopher)

