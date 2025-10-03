#!/usr/bin/env python3
"""
RuneScape Classic Mining Bot
Automates mining tin and copper ore, then deposits at the bank.
"""

import time
import pyautogui
from PIL import Image, ImageGrab
import numpy as np
from typing import Tuple, Optional, List


class MiningBot:
    """Bot for automating mining in RuneScape Classic."""
    
    def __init__(self, inventory_slots: int = 28):
        """
        Initialize the mining bot.
        
        Args:
            inventory_slots: Maximum number of inventory slots (default 28 for RuneScape)
        """
        self.inventory_slots = inventory_slots
        self.ore_count = 0
        self.mining = True
        
        # Safety settings
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.5
        
        # Color definitions for ore detection (RGB values)
        # These are approximate and may need adjustment for different screens
        self.tin_ore_color = (150, 150, 150)  # Grayish
        self.copper_ore_color = (139, 69, 19)  # Brownish
        
        # Tolerance for color matching
        self.color_tolerance = 30
        
    def capture_screen(self, region: Optional[Tuple[int, int, int, int]] = None) -> Image.Image:
        """
        Capture the screen or a specific region.
        
        Args:
            region: Optional tuple (x, y, width, height) for specific region
            
        Returns:
            PIL Image object
        """
        if region:
            return ImageGrab.grab(bbox=region)
        return ImageGrab.grab()
    
    def find_color(self, image: Image.Image, target_color: Tuple[int, int, int], 
                   tolerance: int = 30) -> List[Tuple[int, int]]:
        """
        Find all pixels matching a specific color within tolerance.
        
        Args:
            image: PIL Image to search
            target_color: RGB tuple of target color
            tolerance: Color matching tolerance
            
        Returns:
            List of (x, y) coordinates matching the color
        """
        img_array = np.array(image)
        matches = []
        
        for y in range(img_array.shape[0]):
            for x in range(img_array.shape[1]):
                pixel = img_array[y, x][:3]  # Get RGB, ignore alpha if present
                
                # Check if pixel is within tolerance of target color
                if all(abs(pixel[i] - target_color[i]) <= tolerance for i in range(3)):
                    matches.append((x, y))
        
        return matches
    
    def find_ore(self, ore_type: str = 'both') -> Optional[Tuple[int, int]]:
        """
        Find ore on the screen.
        
        Args:
            ore_type: Type of ore to find ('tin', 'copper', or 'both')
            
        Returns:
            Tuple of (x, y) coordinates of ore, or None if not found
        """
        screen = self.capture_screen()
        
        colors_to_check = []
        if ore_type in ['tin', 'both']:
            colors_to_check.append(self.tin_ore_color)
        if ore_type in ['copper', 'both']:
            colors_to_check.append(self.copper_ore_color)
        
        for color in colors_to_check:
            matches = self.find_color(screen, color, self.color_tolerance)
            if matches:
                # Return the first match
                return matches[0]
        
        return None
    
    def click_ore(self, position: Tuple[int, int]) -> None:
        """
        Click on ore at the given position.
        
        Args:
            position: (x, y) coordinates to click
        """
        pyautogui.click(position[0], position[1])
        print(f"Clicking ore at position {position}")
    
    def wait_for_mining(self, timeout: int = 10) -> bool:
        """
        Wait for mining animation to complete.
        
        Args:
            timeout: Maximum time to wait in seconds
            
        Returns:
            True if mining completed, False if timeout
        """
        # In a real implementation, this would check for mining animation
        # For now, we'll use a simple delay
        time.sleep(3)
        return True
    
    def check_inventory_full(self) -> bool:
        """
        Check if inventory is full.
        
        Returns:
            True if inventory is full, False otherwise
        """
        return self.ore_count >= self.inventory_slots
    
    def mine_ore(self) -> bool:
        """
        Mine a single ore.
        
        Returns:
            True if ore was mined, False otherwise
        """
        ore_position = self.find_ore('both')
        
        if ore_position:
            self.click_ore(ore_position)
            
            if self.wait_for_mining():
                self.ore_count += 1
                print(f"Ore mined! Total: {self.ore_count}/{self.inventory_slots}")
                return True
        
        return False
    
    def walk_to_bank(self) -> None:
        """
        Walk character to the bank.
        This is a placeholder that would need to be customized for specific locations.
        """
        print("Walking to bank...")
        # In a real implementation, this would:
        # 1. Find the bank on minimap or screen
        # 2. Click to move towards it
        # 3. Wait for arrival
        # For now, simulate with a delay
        time.sleep(5)
        print("Arrived at bank")
    
    def open_bank(self) -> bool:
        """
        Open the bank interface.
        
        Returns:
            True if bank opened successfully, False otherwise
        """
        print("Opening bank...")
        # In a real implementation, this would:
        # 1. Find the banker or bank booth
        # 2. Right-click and select "Bank"
        # 3. Wait for bank interface to open
        time.sleep(2)
        print("Bank opened")
        return True
    
    def deposit_ore(self) -> None:
        """
        Deposit all ore in the bank.
        """
        print(f"Depositing {self.ore_count} ore...")
        # In a real implementation, this would:
        # 1. Click on each ore stack in inventory
        # 2. Select deposit option
        # 3. Confirm all ore is deposited
        time.sleep(2)
        self.ore_count = 0
        print("All ore deposited")
    
    def close_bank(self) -> None:
        """
        Close the bank interface.
        """
        print("Closing bank...")
        # Press Escape or click close button
        pyautogui.press('esc')
        time.sleep(1)
    
    def walk_to_mine(self) -> None:
        """
        Walk character back to the mining area.
        """
        print("Walking back to mine...")
        # In a real implementation, this would navigate back to mining area
        time.sleep(5)
        print("Arrived at mine")
    
    def run(self) -> None:
        """
        Main bot loop.
        """
        print("Starting RuneScape Mining Bot...")
        print("Press Ctrl+C to stop")
        print(f"Inventory size: {self.inventory_slots} slots")
        
        try:
            while self.mining:
                # Mining phase
                while not self.check_inventory_full() and self.mining:
                    if not self.mine_ore():
                        print("No ore found, waiting...")
                        time.sleep(2)
                
                if not self.mining:
                    break
                
                # Banking phase
                print("\nInventory full! Going to bank...")
                self.walk_to_bank()
                
                if self.open_bank():
                    self.deposit_ore()
                    self.close_bank()
                
                # Return to mining
                self.walk_to_mine()
                
        except KeyboardInterrupt:
            print("\nBot stopped by user")
            self.mining = False
        except Exception as e:
            print(f"\nError occurred: {e}")
            self.mining = False


def main():
    """Main entry point for the script."""
    print("="*50)
    print("RuneScape Classic Mining Bot")
    print("="*50)
    print("\nThis bot will:")
    print("- Mine tin and copper ore")
    print("- Automatically bank when inventory is full")
    print("- Return to mining after banking")
    print("\nIMPORTANT: Position your RuneScape window and start near ores")
    print("Press Enter to start...")
    input()
    
    bot = MiningBot(inventory_slots=28)
    bot.run()


if __name__ == "__main__":
    main()
