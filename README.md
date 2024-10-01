# Discord Math Quiz Bot

This Discord bot generates math questions for users to solve. Users can select a difficulty level, earn points for correct answers, and view their rankings on the leaderboard.

## Features

- **Math Quiz**: Generates random math questions with addition, subtraction, multiplication, and division.
- **Difficulty Levels**: Users can choose between three difficulty levels: `easy`, `medium`, and `hard`.
- **Leaderboard**: Tracks user scores across sessions and displays the leaderboard with current rankings.
- **Persistent Score Storage**: Saves and loads the leaderboard from a JSON file to preserve scores between bot restarts.

## Installation

1. Clone this repository or download the source code.
2. Install the required Python packages using `pip`:
   ```bash
   pip install discord.py
