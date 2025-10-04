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
import keyboard
import cv2

class MiningBot:
    """Bot for automating mining in RuneScape Classic."""
    
    def __init__(self, inventory_slots: int = 27):
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
        self.tin_ore_color = [(134, 124, 123),(128, 118, 117),(137, 125, 125),(81, 75, 75),(121, 112, 112)]  # Grayish rgb(134 124 123) rgb(128 118 117) rgb(137 125 125) rgb(81 75 75) rgb(121 112 112)
        self.copper_ore_color = [(131, 91, 56),(119, 83, 51),(149, 104, 63)]  # Brownish rgb(131 91 56) rgb(119 83 51) rgb(149 104, 63)

        # Tolerance for color matching
        self.color_tolerance = 1


        self.tin_template = cv2.imread('Templates/Tin.png', 0)
        self.copper_template = cv2.imread('Templates/Copper.png', 0)

        self.w_tin, self.h_tin = self.tin_template.shape[::-1]
        self.w_copper, self.h_copper = self.copper_template.shape[::-1]

        self.inventory_tin_template = cv2.imread('Templates/InventoryTin.png', 0)
        self.inventory_copper_template = cv2.imread('Templates/InventoryCopper.png', 0)

        self.w_inv_tin, self.h_inv_tin = self.inventory_tin_template.shape[::-1]
        self.w_inv_copper, self.h_inv_copper = self.inventory_copper_template.shape[::-1]

        self.mind_ore_template = cv2.imread('Templates/MindOre.png', 0)
        self.w_mind, self.h_mind = self.mind_ore_template.shape[::-1]

        # self.waypoint_template = cv2.imread('Templates/Waypoint.png', 0)
        # self.w_waypoint, self.h_waypoint = self.waypoint_template.shape[::-1]

        self.pickaxe_template = cv2.imread('Templates/Pickaxe.png', 0)
        self.w_pickaxe, self.h_pickaxe = self.pickaxe_template.shape[::-1]

        self.to_bank_waypoints = [cv2.imread('Templates/Waypoint.png', 0),
                                   cv2.imread('Templates/Waypoint2.png', 0),
                                   cv2.imread('Templates/Waypoint3.png', 0),
                                   cv2.imread('Templates/Waypoint4.png', 0),
                                   cv2.imread('Templates/Waypoint5.png', 0),
                                   cv2.imread('Templates/Waypoint6.png', 0),
                                   cv2.imread('Templates/Waypoint7.png', 0)]
        
        self.to_mine_waypoints = [cv2.imread('Templates/ToMine1.png', 0),
                                   cv2.imread('Templates/ToMine2.png', 0),
                                   cv2.imread('Templates/ToMine3.png', 0),
                                   cv2.imread('Templates/ToMine4.png', 0),
                                   cv2.imread('Templates/ToMine5.png', 0),
                                   cv2.imread('Templates/ToMine6.png', 0),
                                   cv2.imread('Templates/ToMine7.png', 0),
                                   cv2.imread('Templates/ToMine8.png', 0),
                                   cv2.imread('Templates/ToMine9.png', 0)]

        self.exp_button_template = cv2.imread('Templates/ExpButton.png', 0)

        self.exit_template = cv2.imread('Templates/ExitBank.png', 0)

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

    def get_best_match(self, template_img) -> Optional[Tuple[int, int]]:
        screen_pil = self.capture_screen()
        screen_cv = np.array(screen_pil)
        screen_gray = cv2.cvtColor(screen_cv, cv2.COLOR_BGR2GRAY)
        
        # Perform the template matching
        res = cv2.matchTemplate(screen_gray, template_img, cv2.TM_CCOEFF_NORMED)
        # return max location
        location = np.argmax(res)
        point = np.zeros(2, dtype=int)
        template_w, template_h = template_img.shape[::-1]
        center_x = (location % res.shape[1]) + template_w // 2
        center_y = (location // res.shape[1]) + template_h // 2
        point[0] = center_x
        point[1] = center_y
        return point

    def find_location_with_template(self, template_img, template_w, template_h, threshold=0.5) -> List[Tuple[int, int]]:
        """
        Finds all occurrences of a template image on the screen.
        
        Args:
            template_img: The loaded OpenCV template image (in grayscale).
            template_w: The width of the template.
            template_h: The height of the template.
            threshold: The confidence threshold for a match (0.0 to 1.0).
            
        Returns:
            A list of center coordinates (x, y) for each match found.
        """
        # Capture the screen and convert it to a NumPy array and then grayscale
        screen_pil = self.capture_screen()
        screen_cv = np.array(screen_pil)
        screen_gray = cv2.cvtColor(screen_cv, cv2.COLOR_BGR2GRAY)
        
        # Perform the template matching
        res = cv2.matchTemplate(screen_gray, template_img, cv2.TM_CCOEFF_NORMED)

        #print biggest 5 matches
        #print(np.sort(res.flatten())[-5:])
        
        # Find the locations of matches that exceed the threshold
        locations = np.where(res >= threshold)
        res = res[locations]
        
        # Unzip the locations and store them as a list of (x, y) points
        points = []
        for pt in zip(*locations[::-1]):  # Switch (y, x) to (x, y)
            # Calculate the center of the found rectangle
            center_x = pt[0] + template_w // 2
            center_y = pt[1] + template_h // 2
            points.append((center_x, center_y))

        return points
    


    def find_gridpoints_with_matches(self, screen, matches, grid_size = 20):
        """
        Find grid points that have all matches in them.
        
        Args:
            matches: List of lists of (x, y) coordinates
            grid_size: Size of each grid cell
        """
        
        w, h = screen.size
        grid_w, grid_h = w // grid_size, h // grid_size
        match_types = len(matches)
        num_of_matches = np.zeros((grid_h, grid_w, match_types), dtype=int)
        avg_pos = np.zeros((grid_h, grid_w, 2), dtype=int)

        for i, match_list in enumerate(matches):
            for match in match_list:
                grid_x, grid_y = match[0] // grid_size, match[1] // grid_size
                num_of_matches[grid_y, grid_x, i] += 1
                avg_pos[grid_y, grid_x] += match

        gridpoints_with_all_matches = []
        for y in range(grid_h):
            for x in range(grid_w):
                if all(num_of_matches[y, x, i] > 0 for i in range(match_types)):
                    num_of_matches_in_cell = sum(num_of_matches[y, x, i] for i in range(match_types))
                    avg_pos[y, x] = avg_pos[y, x]//num_of_matches_in_cell
                    gridpoints_with_all_matches.append((avg_pos[y, x][0], avg_pos[y, x][1]))

        return gridpoints_with_all_matches

    
    def find_k_closest_point(self, screen, points, k):
        w,h = screen.size
        center = (w//2, h//2)
        dist = np.zeros(len(points))
        for i, point in enumerate(points):
            dist[i] = (point[0]-center[0])**2 + (point[1]-center[1])**2
        
        closest_indices = np.argsort(dist)[:k]
        return [points[i] for i in closest_indices]

    def click_on(self, position: Tuple[int, int]) -> None:
        """
        Click on ore at the given position.
        
        Args:
            position: (x, y) coordinates to click
        """
        pyautogui.moveTo(position[0], position[1])
        pyautogui.click()

    def find_ore(self, ore_type: str = 'both') -> Optional[Tuple[int, int]]:
        """
        Find ore on the screen.
        
        Args:
            ore_type: Type of ore to find ('tin', 'copper', or 'both')
            
        Returns:
            Tuple of (x, y) coordinates of ore, or None if not found
        """
        counter = 0
        while True:
            counter += 1
            screen = self.capture_screen()
            
            colors_to_check = []
            if ore_type in ['tin', 'both']:
                colors_to_check.append(self.tin_ore_color)
            if ore_type in ['copper', 'both']:
                colors_to_check.append(self.copper_ore_color)
            
            

            for color in colors_to_check:
                matches = []
                for c in color:
                    matches.append( self.find_color(screen, c, self.color_tolerance))

                screen_temp = screen.copy()



                gridpoints = self.find_gridpoints_with_matches(screen_temp, matches)

                gridpoints = self.find_k_closest_point(screen_temp, gridpoints, 5)

                # get random gridpoint
                rnd_point = gridpoints[np.random.randint(0, len(gridpoints))] if gridpoints else None
                return rnd_point
                # if rnd_point:
                #     # click on this point
                #     pyautogui.moveTo(rnd_point[0], rnd_point[1])
                #     pyautogui.click()
                #     time.sleep(3)  # wait a bit after clicking      
                #     # save screenshot
                #     # mark all points magenta
                #     for match_list in matches:
                #         for match in match_list:
                #             screen_temp.putpixel(match, (255, 0, 255))

                #     # mark the clicked point yellow
                #     screen_temp.putpixel(rnd_point, (255, 255, 0))
                #     screen_temp.save(f"/Debug Screenshots/debug_screenshot_click_{counter}.png")      
            # del screen_temp
            # del screen

                # # draw green circles for each gridpoint
                # for gp in gridpoints:
                #     screen_temp.putpixel(gp, (0, 255, 0))
                # if gridpoints:
                #     print(f"Found {len(gridpoints)} gridpoints with all matches for color {color} (set {counter})")

                # #save screenshot
                # screen_temp.save(f"/Debug Screenshots/debug_screenshot_{counter%2}.png")
                # counter += 1

                # add magenta pixels for each match
                # for match_list in matches:
                #     rnd_num = np.random.randint(0, 200) 
                #     for match in match_list:
                #         screen_temp.putpixel(match, (255, rnd_num, 255)) 


                # #save screenshot
                # screen_temp.save(f"/Debug Screenshots/debug_screenshot_{counter%2}.png")
                # print(f"Found {len(matches)} matches for color {color} (set {counter})")
                # counter += 1



                # Pause to allow user to see output
                # if matches:
                #     # Return the first match
                #     return matches[0]



    def count_ore(self, threshold=0.9) -> List[Tuple[int, int]]:
        """
        Finds all occurrences of a template image on the screen.
        
        Args:
            template_img: The loaded OpenCV template image (in grayscale).
            template_w: The width of the template.
            template_h: The height of the template.
            threshold: The confidence threshold for a match (0.0 to 1.0).
            
        Returns:
            A list of center coordinates (x, y) for each match found.
        """
        # Capture the screen and convert it to a NumPy array and then grayscale
        screen_pil = self.capture_screen()
        screen_cv = np.array(screen_pil)
        screen_gray = cv2.cvtColor(screen_cv, cv2.COLOR_BGR2GRAY)
        
        # Perform the template matching
        res = cv2.matchTemplate(screen_gray, self.inventory_copper_template, cv2.TM_CCOEFF_NORMED)

        #print biggest 5 matches
        # print(np.sort(res.flatten())[-5:])
        
        # Find the locations of matches that exceed the threshold
        locations = np.where(res >= threshold)
        
        # Unzip the locations and store them as a list of (x, y) points
        points = []
        for pt in zip(*locations[::-1]):  # Switch (y, x) to (x, y)
            # Calculate the center of the found rectangle
            center_x = pt[0] + self.w_inv_copper // 2
            center_y = pt[1] + self.h_inv_copper // 2
            points.append((center_x, center_y))
        
        print(len(points))
        time.sleep(1)
        return len(points)


    def wait_for_mining(self,) -> bool:
        """
        Wait for mining animation to complete.
        
        Args:
            timeout: Maximum time to wait in seconds
            
        Returns:
            True if mining completed, False if timeout
        """
        # mind_finish = []

        # while True: 
        #     mind_finish = self.find_ore_with_template(self.mind_ore_template, self.w_mind, self.h_mind, threshold=0.95)
        #     print(f"Mining animation matches: {len(mind_finish)}")
        #     if len(mind_finish) > 0:
        #         print("Mining animation finished.")
        #         return True
        #     time.sleep(0.5)

        start_time = time.time()

        while True:
            # print(f"Ore count: {self.count_ore()}, {self.ore_count}")
            delta_time = time.time() - start_time
            if delta_time > 10:
                print("Timeout waiting for mining to complete")
                return False
            if self.count_ore() > self.ore_count and not self.check_inventory_full():
                self.ore_count = self.count_ore()
                return True
    
    def check_inventory_full(self) -> bool:
        """
        Check if inventory is full.
        
        Returns:
            True if inventory is full, False otherwise
        """
        print("Checking if inventory is full...")
        print("Inventory count:", self.count_ore())
        print("Inventory slots:", self.inventory_slots)
        return self.ore_count >= self.inventory_slots
    
    def mine_ore(self) -> bool:
        """
        Mine a single ore.
        
        Returns:
            True if ore was mined, False otherwise
        """

        tin_rocks = self.find_location_with_template(self.tin_template, self.w_tin, self.h_tin)
        copper_rocks = self.find_location_with_template(self.copper_template, self.w_copper, self.h_copper)
        all_rocks = tin_rocks + copper_rocks
        
        print(f"All rocks: {len(all_rocks)}")


        # ore_position = self.find_ore('both')
        ore_position = all_rocks[np.random.randint(0, len(all_rocks))]

        print(f"Ore position: {ore_position}")
        
        if ore_position:
            # screen = self.capture_screen()
            # screen.putpixel(ore_position, (0, 255, 0))
            # screen.save(f"/Debug Screenshots/debug_screenshot_mine_{int(time.time())}.png")
            self.click_on(ore_position)

            self.ore_count = self.count_ore()
            
            if self.wait_for_mining():
                print(f"Ore mined! Total: {self.ore_count}/{self.inventory_slots}")
                return True
        
        return False
    
    def toggle_run(self) -> None:
        """
        Toggle run mode on/off by clicking the run button.
        """
        exp_button_pos = self.get_best_match(self.exp_button_template)
        pyautogui.moveTo(exp_button_pos[0]+40, exp_button_pos[1]+90)
        pyautogui.click()
        time.sleep(0.5)
    
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
        pickaxe_pos = self.get_best_match(self.pickaxe_template)
        pickaxe_pos = np.array([pickaxe_pos[0]-self.w_pickaxe//2, pickaxe_pos[1]-self.h_pickaxe//2])
        while True:
            inventory_ore_pos = self.find_location_with_template(self.inventory_copper_template, self.w_inv_copper, self.h_inv_copper, threshold=0.9)
            if len(inventory_ore_pos) == 0:
                print("No ore left in inventory to deposit")
                return True
            for ore in inventory_ore_pos:
                # print(f"Found {len(inventory_ore_pos)} ore in inventory")
                if ore[0] > pickaxe_pos[0] and ore[1] > pickaxe_pos[1]:
                    print("Found ore in inventory:", ore)
                    pyautogui.moveTo(ore[0], ore[1])
                    pyautogui.click(button='right')
                    pyautogui.moveTo(ore[0], ore[1]+88)
                    pyautogui.click()
                    time.sleep(0.5)
                    break

    def close_bank(self) -> None:
        """
        Close the bank interface.
        """
        
        exit_pos = self.get_best_match(self.exit_template)
        pyautogui.moveTo(exit_pos[0], exit_pos[1])
        pyautogui.click()
        time.sleep(0.5)
    
    def walk_to_mine(self) -> None:
        """
        Walk character back to the mining area.
        """
        print("Walking back to mine...")
        # In a real implementation, this would navigate back to mining area
        time.sleep(5)
        print("Arrived at mine")
    

    def go_to_bank(self) -> None:
        """
        Walk character the predefined waypoint path.
        """
        self.go_to_waypoints(self.to_bank_waypoints)

    def go_to_mine(self) -> None:
        """
        Walk character the predefined waypoint path.
        """
        self.go_to_waypoints(self.to_mine_waypoints)

    def go_to_waypoints(self, waypoint_templates) -> None:
        """
        Walk character the predefined waypoint path.
        """
        for i in range(len(waypoint_templates)):
            waypoint = self.get_best_match(waypoint_templates[i])
            print(f"Found waypoint {i+1} at: {waypoint}")
            print("Walking to waypoint...")
            self.click_on(waypoint)
            time.sleep(10)
            print("Arrived at waypoint")

    def run(self) -> None:
        """
        Main bot loop.
        """
        print("Starting RuneScape Mining Bot...")
        print("Press Ctrl+C to stop")
        print(f"Inventory size: {self.inventory_slots} slots")

        self.ore_count = self.count_ore()

        # Check for 'p' key press to stop the bot
        while True:
            if keyboard.is_pressed('enter'):
                print("Bot started by user (Enter key pressed)")
                break

        
        try:
            while True:
                self.toggle_run()
                # # Mining phase
                if not self.check_inventory_full():
                    while not self.check_inventory_full() and self.mining:
                        if not self.mine_ore():
                            print("No ore found, waiting...")
                            time.sleep(2)
                
                print(f"\n✓ Inventory full! ({self.ore_count}/{self.inventory_slots})")
                self.mining = False
                self.toggle_run()
                self.go_to_bank()

                self.deposit_ore()

                self.close_bank()

                self.ore_count = 0

                self.go_to_mine()
                self.mining = True

                # # Banking phase
                # print("\nInventory full! Going to bank...")
                # self.walk_to_bank()
                
                # if self.open_bank():
                #     self.deposit_ore()
                #     self.close_bank()
                
                # Return to mining
                # self.walk_to_mine()
                
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
    
    bot = MiningBot()
    bot.run()


if __name__ == "__main__":
    main()
