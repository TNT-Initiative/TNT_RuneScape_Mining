#!/usr/bin/env python3
"""
Example/Demo script showing how the mining bot works without requiring RuneScape.
This simulates the bot's behavior for testing purposes.
"""

import time


class MiningBotDemo:
    """Demo version of the mining bot for testing."""
    
    def __init__(self):
        self.inventory_slots = 28
        self.ore_count = 0
        
    def simulate_mining(self):
        """Simulate the mining process."""
        print("\n" + "="*50)
        print("MINING BOT DEMO - Simulated Run")
        print("="*50)
        
        cycle = 1
        
        while cycle <= 3:  # Run 3 cycles for demo
            print(f"\n--- Cycle {cycle} ---")
            
            # Mining phase
            print("\nPhase 1: Mining ore...")
            while self.ore_count < self.inventory_slots:
                time.sleep(0.1)  # Fast simulation
                self.ore_count += 1
                ore_type = "tin" if self.ore_count % 2 == 0 else "copper"
                print(f"  Mined {ore_type} ore! ({self.ore_count}/{self.inventory_slots})")
                
                if self.ore_count >= self.inventory_slots:
                    print(f"\n  ✓ Inventory full! ({self.inventory_slots} ores)")
                    break
            
            # Banking phase
            print("\nPhase 2: Banking...")
            print("  Walking to bank...")
            time.sleep(0.3)
            print("  Opening bank...")
            time.sleep(0.2)
            print(f"  Depositing {self.ore_count} ores...")
            time.sleep(0.2)
            self.ore_count = 0
            print("  ✓ All ore deposited")
            print("  Closing bank...")
            time.sleep(0.2)
            
            # Return to mining
            print("\nPhase 3: Returning to mine...")
            time.sleep(0.3)
            print("  ✓ Back at mining location")
            
            cycle += 1
        
        print("\n" + "="*50)
        print("Demo completed! This shows how the bot would work:")
        print("1. Mines tin and copper ore until inventory is full")
        print("2. Walks to bank and deposits all ore")
        print("3. Returns to mining area")
        print("4. Repeats the cycle")
        print("="*50)


def main():
    """Run the demo."""
    print("This is a demonstration of the mining bot's logic")
    print("No actual game interaction will occur\n")
    
    demo = MiningBotDemo()
    demo.simulate_mining()


if __name__ == "__main__":
    main()
