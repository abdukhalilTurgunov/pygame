# 🎮 Arkanoid Deluxe

Arkanoid Deluxe is a classic-style arcade game built in Python using the Pygame library.
The player controls a paddle to bounce the ball and break all the bricks on the screen.
The game features various power-ups, lasers, shield mechanics, multi-ball, and more.

## 💻 Requirements

- Python 3.7+
- Pygame library (install with `pip install pygame`)

## 💥 How to run

```bash
python main.py
```

## 🎯 Game objective

- Destroy all the bricks on each level by bouncing the ball.
- Prevent the ball from falling below the paddle.
- Collect power-ups to gain special abilities and advantages.

## ⚡ Power-ups

| Type | Description                                |
|-------|--------------------------------------------|
| G (Grow)   | Increases paddle width.                 |
| M (Multi)  | Adds an extra ball.                    |
| S (Shield) | Adds a shield at the bottom to catch the ball. |
| F (Fireball) | Ball passes through bricks without bouncing. |
| L (Laser)  | Allows the paddle to shoot lasers.     |

## 🎮 Controls

| Key    | Action                                |
|---------|---------------------------------------|
| ← / → | Move the paddle left/right            |
| SPACE | Start the game or restart after win/game over |
| R     | Retry after game over                 |
| M     | Toggle sound on/off                   |
| F     | Fire lasers (if laser power-up is active) |

## 🧱 Levels

Levels are defined in the levels list.

When all bricks are cleared, the next level is loaded.

In the current setup, only one level is configured (`levels = [4, 6, 8]`), but you can easily add more by expanding the list (e.g., `[1, 2, 3]`).

## 💡 Features

✅ Sound effects (bounce, brick break, game over, laser, win)  
✅ Bottom shield to catch the ball once  
✅ Laser shooting ability  
✅ Multi-ball and fireball mechanics  
✅ Title screen, win screen, and game over screen  
✅ Sound toggle feature

## 🏆 Win screen

After all bricks are destroyed, a win screen is shown displaying the final score and remaining lives.

Win sound effect is played (if sound is enabled).

## 🧑‍💻 Author

Abdukhalil Turgunov  
✉️ abdukhalil_turgunov@student.itpu.uz
