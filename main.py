"""
COMP 163 - Project 3: Quest Chronicles
Main Game Module - Starter Code

Name: devane, lemanuel

AI Usage: I used Chatgpt and Google Ai to help me with the structure or the code, in addition to assisting me with surveying different logic options and checking for syntax and other uncaught errors.

This is the main game file that ties all modules together.
Demonstrates module integration and complete game flow.
"""

# Import all our custom modules
import character_manager
import inventory_system
import quest_handler
import combat_system
import game_data
from custom_exceptions import (
    InvalidCharacterClassError,
    CharacterNotFoundError,
    SaveFileCorruptedError,
    ItemNotFoundError,
    InvalidItemTypeError,MissingDataFileError,InvalidDataFormatError)

# ============================================================================
# GAME STATE
# ============================================================================

# Global variables for game data
current_character = None
all_quests = {}
all_items = {}
game_running = False

# ============================================================================
# MAIN MENU
# ============================================================================

def main_menu():
    """
    Display main menu and get player choice
    
    Options:
    1. New Game
    2. Load Game
    3. Exit
    
    Returns: Integer choice (1-3)
    """
    print("\n=== MAIN MENU ===")
    print("1. New Game")
    print("2. Load Game")
    print("3. Exit")
    
    while True:
        choice = input("Select an option (1-3): ").strip()
        if choice in ["1", "2", "3"]:
            return int(choice)
        print("Invalid input. Enter 1, 2, or 3.")

def new_game():
    """
    Start a new game
    
    Prompts for:
    - Character name
    - Character class
    
    Creates character and starts game loop
    """
    global current_character
    print("\n=== CREATE NEW CHARACTER ===")
    
    name = input("Enter your character name: ").strip()
    print("Choose a class:")
    print("1. Warrior")
    print("2. Mage")
    print("3. Rogue")
    
    class_choice = input("Enter choice (1-3): ").strip()
    class_map = {"1": "Warrior", "2": "Mage", "3": "Rogue"}
    try:
        char_class = class_map[class_choice]
        current_character = character_manager.create_character(name, char_class)
        print(f"Character '{name}' the {char_class} created!")
        game_loop()
    except (InvalidCharacterClassError, KeyError) as e:
        print(f"Error creating character: {e}")

def load_game():
    """
    Load an existing saved game
    
    Shows list of saved characters
    Prompts user to select one
    """
    global current_character
    
    print("\n=== LOAD SAVED GAME ===")
    
    try:
        saved_list = character_manager.list_saved_characters()
        if not saved_list:
            print("No saved characters found.")
            return
        print("Saved characters:")
        for i, name in enumerate(saved_list, start=1):
            print(f"{i}. {name}")
        
        choice = input("Select a character to load: ").strip()
        index = int(choice) - 1
        selected_name = saved_list[index]
        current_character = character_manager.load_character(selected_name)
        print(f"Loaded character '{selected_name}'!")
        game_loop()
    except (CharacterNotFoundError, SaveFileCorruptedError, IndexError, ValueError) as e:
        print(f"Error loading character: {e}")


# ============================================================================
# GAME LOOP
# ============================================================================

def game_loop():
    """
    Main game loop - shows game menu and processes actions
    """
    global game_running, current_character
    
    game_running = True
    
    while game_running:
        choice = game_menu()
        
        if choice == 1:
            view_character_stats()
        elif choice == 2:
            view_inventory()
        elif choice == 3:
            quest_menu()
        elif choice == 4:
            explore()
        elif choice == 5:
            shop()
        elif choice == 6:
            save_game()
            print("Game saved. Exiting...")
            game_running = False

def game_menu():
    """
    Display game menu and get player choice
    
    Options:
    1. View Character Stats
    2. View Inventory
    3. Quest Menu
    4. Explore (Find Battles)
    5. Shop
    6. Save and Quit
    
    Returns: Integer choice (1-6)
    """
    print("\n=== GAME MENU ===")
    print("1. View Character Stats")
    print("2. View Inventory")
    print("3. Quest Menu")
    print("4. Explore")
    print("5. Shop")
    print("6. Save and Quit")
    
    while True:
        choice = input("Choose an action (1-6): ").strip()
        if choice in [str(i) for i in range(1, 7)]:
            return int(choice)
        print("Invalid choice. Enter a number 1-6.")

# ============================================================================
# GAME ACTIONS
# ============================================================================

def view_character_stats():
    """Display character information"""
    global current_character
    
    print("\n=== CHARACTER STATS ===")
    print(f"Name: {current_character['name']}")
    print(f"Class: {current_character['class']}")
    print(f"Level: {current_character.get('level',1)}")
    print(f"Health: {current_character['health']}/{current_character['max_health']}")
    print(f"Strength: {current_character['strength']}")
    print(f"Magic: {current_character['magic']}")
    print(f"Gold: {current_character['gold']}")
    print(f"Equipped Weapon: {current_character.get('equipped_weapon')}")
    print(f"Equipped Armor: {current_character.get('equipped_armor')}")
    
    quest_handler.display_quest_summary(current_character, all_quests)

def view_inventory():
    """Display and manage inventory"""
    global current_character, all_items
    
    while True:
        inventory_system.display_inventory(current_character, all_items)
        print("\nOptions:")
        print("1. Use Item")
        print("2. Equip Weapon")
        print("3. Equip Armor")
        print("4. Drop Item")
        print("5. Back")
        
        choice = input("Select an option: ").strip()
        
        if choice == "1":
            item_id = input("Enter item ID to use: ").strip()
            try:
                print(inventory_system.use_item(current_character, item_id, all_items[item_id]))
            except (ItemNotFoundError, InvalidItemTypeError) as e:
                print(e)
        elif choice == "2":
            item_id = input("Enter weapon ID to equip: ").strip()
            try:
                print(inventory_system.equip_weapon(current_character, item_id, all_items[item_id]))
            except (ItemNotFoundError, InvalidItemTypeError) as e:
                print(e)
        elif choice == "3":
            item_id = input("Enter armor ID to equip: ").strip()
            try:
                print(inventory_system.equip_armor(current_character, item_id, all_items[item_id]))
            except (ItemNotFoundError, InvalidItemTypeError) as e:
                print(e)
        elif choice == "4":
            item_id = input("Enter item ID to drop: ").strip()
            try:
                inventory_system.remove_item_from_inventory(current_character, item_id)
                print(f"Dropped {item_id}.")
            except ItemNotFoundError as e:
                print(e)
        elif choice == "5":
            break
        else:
            print("Invalid choice. Try again.")

def quest_menu():
    """Quest management menu"""
    global current_character, all_quests
    
    while True:
        print("\n=== QUEST MENU ===")
        print("1. View Active Quests")
        print("2. View Available Quests")
        print("3. View Completed Quests")
        print("4. Accept Quest")
        print("5. Abandon Quest")
        print("6. Complete Quest (DEBUG)")
        print("7. Back")
        
        choice = input("Choose an option: ").strip()
        
        try:
            if choice == "1":
                quest_handler.display_active_quests(current_character, all_quests)
            elif choice == "2":
                quest_handler.display_available_quests(current_character, all_quests)
            elif choice == "3":
                quest_handler.display_completed_quests(current_character, all_quests)
            elif choice == "4":
                quest_id = input("Enter quest ID to accept: ").strip()
                quest_handler.accept_quest(current_character, quest_id, all_quests)
            elif choice == "5":
                quest_id = input("Enter quest ID to abandon: ").strip()
                quest_handler.abandon_quest(current_character, quest_id)
            elif choice == "6":
                quest_id = input("Enter quest ID to complete: ").strip()
                quest_handler.complete_quest(current_character, quest_id)
            elif choice == "7":
                break
            else:
                print("Invalid choice.")
        except Exception as e:
            print(f"Error: {e}")


def explore():
    """Find and fight random enemies"""
    global current_character
    print("\n=== EXPLORATION ===")
    
    try:
        enemy = combat_system.generate_enemy(current_character)
        print(f"A wild {enemy['name']} appears!")
        result = combat_system.SimpleBattle(current_character, enemy)
        if result == "victory":
            print(f"You defeated {enemy['name']}!")
        elif result == "defeat":
            handle_character_death()
    except Exception as e:
        print(f"Exploration error: {e}")

def shop():
    """Shop menu for buying/selling items"""
    global current_character, all_items
    
    while True:
        print("\n=== SHOP ===")
        print(f"Gold: {current_character['gold']}")
        print("Items for sale:")
        for item_id, data in all_items.items():
            print(f"{item_id}: {data['name']} - {data['cost']} gold ({data['type']})")
        print("\nOptions:")
        print("1. Buy Item")
        print("2. Sell Item")
        print("3. Back")
        
        choice = input("Select an option: ").strip()
        
        try:
            if choice == "1":
                item_id = input("Enter item ID to buy: ").strip()
                inventory_system.purchase_item(current_character, item_id, all_items[item_id])
                print(f"Purchased {item_id}!")
            elif choice == "2":
                item_id = input("Enter item ID to sell: ").strip()
                gold_received = inventory_system.sell_item(current_character, item_id, all_items[item_id])
                print(f"Sold {item_id} for {gold_received} gold!")
            elif choice == "3":
                break
            else:
                print("Invalid choice.")
        except Exception as e:
            print(f"Shop error: {e}")

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def save_game():
    """Save current game state"""
    global current_character
    
    try:
        character_manager.save_character(current_character)
        print("Game saved successfully!")
    except Exception as e:
        print(f"Save error: {e}")


def load_game_data():
    """Load all quest and item data from files"""
    global all_quests, all_items
    
    global all_quests, all_items
    
    try:
        all_quests = game_data.load_quests()
        all_items = game_data.load_items()
    except MissingDataFileError:
        print("Data files missing. Creating defaults...")
        game_data.create_default_data_files()
        all_quests = game_data.load_quests()
        all_items = game_data.load_items()
    except InvalidDataFormatError as e:
        print(f"Error: {e}")
        raise

def handle_character_death():
    """Handle character death"""
    global current_character, game_running
    
    print("\n=== YOU HAVE DIED ===")
    if current_character['gold'] >= 10:
        choice = input("Revive for 10 gold? (y/n): ").strip().lower()
        if choice == 'y':
            character_manager.revive_character(current_character, cost=10)
            print("You have been revived!")
        else:
            print("Game over.")
            game_running = False
    else:
        print("Not enough gold to revive. Game over.")
        game_running = False
    pass

def display_welcome():
    """Display welcome message"""
    print("=" * 50)
    print("     QUEST CHRONICLES - A MODULAR RPG ADVENTURE")
    print("=" * 50)
    print("\nWelcome to Quest Chronicles!")
    print("Build your character, complete quests, and become a legend!")
    print()

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main game execution function"""
    
    # Display welcome message
    display_welcome()
    
    # Load game data
    try:
        load_game_data()
        print("Game data loaded successfully!")
    except MissingDataFileError:
        print("Creating default game data...")
        game_data.create_default_data_files()
        load_game_data()
    except InvalidDataFormatError as e:
        print(f"Error loading game data: {e}")
        print("Please check data files for errors.")
        return
    
    # Main menu loop
    while True:
        choice = main_menu()
        
        if choice == 1:
            new_game()
        elif choice == 2:
            load_game()
        elif choice == 3:
            print("\nThanks for playing Quest Chronicles!")
            break
        else:
            print("Invalid choice. Please select 1-3.")

if __name__ == "__main__":
    main()
try:
    load_game_data()
    print(f"Loaded {len(all_quests)} quests and {len(all_items)} items.")
    if all_quests:
        first_quest_id = list(all_quests.keys())[0]
        print(f"Sample Quest ({first_quest_id}): {all_quests[first_quest_id]}")
    if all_items:
            first_item_id = list(all_items.keys())[0]
            print(f"Sample Item ({first_item_id}): {all_items[first_item_id]}")
except (MissingDataFileError, InvalidDataFormatError) as e:
    print(f"Error loading game data: {e}")
    print("Creating default data files...")
    game_data.create_default_data_files()
    load_game_data()
    
    # Step 3: Quick test menu
while True:
    print("\n=== TEST MAIN MENU ===")
    print("1. Create New Character")
    print("2. View Loaded Game Data")
    print("3. Exit")
    choice = input("Select an option (1-3): ").strip()
        
    if choice == "1":
        name = input("Enter character name: ").strip()
        char_class = input("Enter class (Warrior, Mage, Rogue): ").strip()
        try:
            current_character = character_manager.create_character(name, char_class)
            print(f"Character created: {current_character}")
        except InvalidCharacterClassError as e:
            print(f"Error: {e}")
    elif choice == "2":
        print(f"\nQuests loaded: {len(all_quests)}")
        print(f"Items loaded: {len(all_items)}")
    elif choice == "3":
        print("Exiting test main module.")
        break
    else:
        print("Invalid choice. Enter 1-3.")
