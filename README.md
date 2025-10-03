# TNT_RuneScape_Mining

A Python automation script for mining in RuneScape Classic. The bot automatically mines tin and copper ore, then deposits them at the bank when the inventory is full.

## Features

- **Screen Capture**: Uses PIL (Pillow) to capture and analyze the game screen
- **Mouse Control**: Uses pyautogui to control mouse movements and clicks
- **Ore Detection**: Automatically detects tin and copper ore on screen using color matching
- **Inventory Management**: Tracks inventory and banks when full (28 slots)
- **Automated Banking**: Walks to bank, deposits ore, and returns to mining
- **Customizable**: Configuration file for adjusting colors and timing

## Requirements

- Python 3.7+
- pillow
- pyautogui
- opencv-python
- numpy

## Installation

1. Clone this repository:
```bash
git clone https://github.com/TNT-Initiative/TNT_RuneScape_Mining.git
cd TNT_RuneScape_Mining
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Open RuneScape Classic in your browser or client
2. Position your character near tin and copper ore rocks
3. Run the bot:
```bash
python mining_bot.py
```

4. Press Enter when prompted to start the bot
5. Press Ctrl+C to stop the bot at any time

## Configuration

Edit `config.txt` to customize:
- Ore colors (RGB values) - adjust based on your screen/graphics settings
- Color matching tolerance
- Timing delays
- Inventory size

## How It Works

1. **Screen Capture**: The bot continuously captures screenshots using PIL
2. **Ore Detection**: Searches for tin (gray) and copper (brown) ore using color matching
3. **Mining**: Clicks on detected ore and waits for mining animation
4. **Inventory Check**: Tracks ore count (default 28 slots)
5. **Banking**: When full, walks to bank, opens bank interface, deposits all ore
6. **Return**: Walks back to mining area and repeats

## Important Notes

⚠️ **Disclaimer**: This bot is for educational purposes only. Using automation scripts may violate RuneScape's Terms of Service and could result in account bans. Use at your own risk.

- The bot uses failsafe mode - move mouse to corner of screen to emergency stop
- Default pause between actions is 0.5 seconds to prevent detection
- You may need to adjust color values in config.txt based on your screen
- The banking and walking logic are simplified placeholders and may need customization for specific game locations

## Troubleshooting

**Ore not detected:**
- Adjust RGB color values in `config.txt`
- Increase `color_tolerance` value
- Ensure game window is visible and not obscured

**Bot clicking wrong locations:**
- Calibrate colors for your specific screen/graphics settings
- Make sure RuneScape window is in focus

## License

This project is open source and available under the MIT License.