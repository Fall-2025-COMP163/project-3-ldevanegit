"""
COMP 163 - Project 3: Quest Chronicles
Character Manager Module - Starter Code

Name: Devane, Lemanuel

AI Usage: I used Chatgpt and Google Ai to help me with the structure or the code, in addition to assisting me with surveying different logic options and checking for syntax and other uncaught errors.

This module handles character creation, loading, and saving.
"""

import os
from custom_exceptions import (
    InvalidCharacterClassError,
    CharacterNotFoundError,
    SaveFileCorruptedError,
    InvalidSaveDataError,
    CharacterDeadError
)

# ============================================================================
# CHARACTER MANAGEMENT FUNCTIONS
# ============================================================================

def create_character(name, character_class):
    """
    Create a new character with stats based on class
    
    Valid classes: Warrior, Mage, Rogue, Cleric
    
    Returns: Dictionary with character data including:
            - name, class, level, health, max_health, strength, magic
            - experience, gold, inventory, active_quests, completed_quests
    
    Raises: InvalidCharacterClassError if class is not valid
    """
    # TODO: Implement character creation
    # Validate character_class first
    # Example base stats:
    # Warrior: health=120, strength=15, magic=5
    # Mage: health=80, strength=8, magic=20
    # Rogue: health=90, strength=12, magic=10
    # Cleric: health=100, strength=10, magic=15
    
    # All characters start with:
    # - level=1, experience=0, gold=100
    # - inventory=[], active_quests=[], completed_quests=[]
    
    # Raise InvalidCharacterClassError if class not in valid list
    # List of valid classes
    valid_classes = ["Warrior", "Mage", "Rogue", "Cleric"]
    
    # Validate class
    if character_class not in valid_classes:
        raise InvalidCharacterClassError(
            f"Invalid class '{character_class}'. Must be one of: {', '.join(valid_classes)}"
        )
    
    # Base stats per class
    base_stats = {
        "Warrior": {"health": 120, "strength": 15, "magic": 5},
        "Mage": {"health": 80, "strength": 8, "magic": 20},
        "Rogue": {"health": 90, "strength": 12, "magic": 10},
        "Cleric": {"health": 100, "strength": 10, "magic": 15}
    }
    
    stats = base_stats[character_class]
    
    # Create character dictionary
    character = {
        "name": name,
        "class": character_class,
        "level": 1,
        "health": stats["health"],
        "max_health": stats["health"],
        "strength": stats["strength"],
        "magic": stats["magic"],
        "experience": 0,
        "gold": 100,
        "inventory": [],
        "active_quests": [],
        "completed_quests": []
    }
    
    return character

def save_character(character, save_directory="data/save_games"):
    """
    Save character to file
    
    Filename format: {character_name}_save.txt
    
    File format:
    NAME: character_name
    CLASS: class_name
    LEVEL: 1
    HEALTH: 120
    MAX_HEALTH: 120
    STRENGTH: 15
    MAGIC: 5
    EXPERIENCE: 0
    GOLD: 100
    INVENTORY: item1,item2,item3
    ACTIVE_QUESTS: quest1,quest2
    COMPLETED_QUESTS: quest1,quest2
    
    Returns: True if successful
    Raises: PermissionError, IOError (let them propagate or handle)
    """
    # TODO: Implement save functionality
    # Create save_directory if it doesn't exist
    # Handle any file I/O errors appropriately
    # Lists should be saved as comma-separated values

    # Ensure the save directory exists
    if not os.path.exists(save_directory):
        os.makedirs(save_directory, exist_ok=True)
    
    filename = f"{save_directory}/{character['name']}_save.txt"
    
    try:
        with open(filename, "w") as f:
            f.write(f"NAME: {character['name']}\n")
            f.write(f"CLASS: {character['class']}\n")
            f.write(f"LEVEL: {character['level']}\n")
            f.write(f"HEALTH: {character['health']}\n")
            f.write(f"MAX_HEALTH: {character['max_health']}\n")
            f.write(f"STRENGTH: {character['strength']}\n")
            f.write(f"MAGIC: {character['magic']}\n")
            f.write(f"EXPERIENCE: {character['experience']}\n")
            f.write(f"GOLD: {character['gold']}\n")
            f.write(f"INVENTORY: {','.join(character['inventory'])}\n")
            f.write(f"ACTIVE_QUESTS: {','.join(character['active_quests'])}\n")
            f.write(f"COMPLETED_QUESTS: {','.join(character['completed_quests'])}\n")
        
        return True
    
    except (PermissionError, IOError) as e:
        # Let the error raise
        raise e

def load_character(character_name, save_directory="data/save_games"):
    """
    Load character from save file
    
    Args:
        character_name: Name of character to load
        save_directory: Directory containing save files
    
    Returns: Character dictionary
    Raises: 
        CharacterNotFoundError if save file doesn't exist
        SaveFileCorruptedError if file exists but can't be read
        InvalidSaveDataError if data format is wrong
    """
    # TODO: Implement load functionality
    # Check if file exists → CharacterNotFoundError
    # Try to read file → SaveFileCorruptedError
    # Validate data format → InvalidSaveDataError
    # Parse comma-separated lists back into Python lists
    filename = f"{save_directory}/{character_name}_save.txt"
    
    # Check if file exists
    if not os.path.exists(filename):
        raise CharacterNotFoundError(f"No save file found for {character_name}")
    
    character = {}
    
    try:
        with open(filename, "r") as f:
            for line in f:
                if not line.strip():
                    continue
                if ": " not in line:
                    raise InvalidSaveDataError(f"Invalid line format: {line}")
                
                key, value = line.strip().split(": ", 1)
                key = key.lower()
                
                # Convert lists from comma-separated strings
                if key in ["inventory", "active_quests", "completed_quests"]:
                    character[key] = value.split(",") if value else []
                # Convert numeric fields to int
                elif key in ["level", "health", "max_health", "strength", "magic", "experience", "gold"]:
                    try:
                        character[key] = int(value)
                    except ValueError:
                        raise InvalidSaveDataError(f"Invalid number for {key}: {value}")
                else:
                    character[key] = value
        
        # Validate the loaded character
        validate_character_data(character)
        return character
    
    except InvalidSaveDataError as e:
        # Data format issues
        raise e
    except Exception as e:
        # Any other file reading issue
        raise SaveFileCorruptedError(f"Failed to read save file: {e}")

def list_saved_characters(save_directory="data/save_games"):
    """
    Get list of all saved character names
    
    Returns: List of character names (without _save.txt extension)
    """
    # TODO: Implement this function
    # Return empty list if directory doesn't exist
    # Extract character names from filenames
    if not os.path.exists(save_directory):
        return []  # No saves exist
    
    saved_files = os.listdir(save_directory)
    characters = []
    
    for file in saved_files:
        if file.endswith("_save.txt"):
            # Remove the suffix to get the character name
            characters.append(file[:-9])  # "_save.txt" is 9 characters
    return characters

def delete_character(character_name, save_directory="data/save_games"):
    """
    Delete a character's save file
    
    Returns: True if deleted successfully
    Raises: CharacterNotFoundError if character doesn't exist
    """
    # TODO: Implement character deletion
    # Verify file exists before attempting deletion
    filename = f"{save_directory}/{character_name}_save.txt"
    
    if not os.path.exists(filename):
        raise CharacterNotFoundError(f"No save file found for {character_name}")
    
    os.remove(filename)
    return True

# ============================================================================
# CHARACTER OPERATIONS
# ============================================================================

def gain_experience(character, xp_amount):
    """
    Add experience to character and handle level ups
    
    Level up formula: level_up_xp = current_level * 100
    Example when leveling up:
    - Increase level by 1
    - Increase max_health by 10
    - Increase strength by 2
    - Increase magic by 2
    - Restore health to max_health
    
    Raises: CharacterDeadError if character health is 0
    """
    # TODO: Implement experience gain and leveling
    # Check if character is dead first
    # Add experience
    # Check for level up (can level up multiple times)
    # Update stats on level up

    #cannot gain experience if dead
    if character['health'] <= 0:
        raise CharacterDeadError(f"{character['name']} is dead and cannot gain XP!")
    # Add experience
    character["experience"] += xp_amount
    
    # Check for level ups
    while character["experience"] >= character["level"] * 100:
        # Subtract XP needed for current level
        character["experience"] -= character["level"] * 100
        character["level"] += 1
        
        #Increase stats upon leveling up
        character["max_health"] += 10
        character["strength"] += 2
        character["magic"] += 2
        
        # Restore health to max
        character["health"] = character["max_health"]
        
        print(f"{character['name']} leveled up to level {character['level']}!")
    
    return character


def add_gold(character, amount):
    """
    Add gold to character's inventory
    
    Args:
        character: Character dictionary
        amount: Amount of gold to add (can be negative for spending)
    
    Returns: New gold total
    Raises: ValueError if result would be negative
    """
    # TODO: Implement gold management
    # Check that result won't be negative
    # Update character's gold
    new_gold = character["gold"] + amount
    
    if new_gold < 0:
        raise ValueError(f"{character['name']} cannot have negative gold!")
    
    character["gold"] = new_gold
    return character["gold"]

def heal_character(character, amount):
    """
    Heal character by specified amount
    
    Health cannot exceed max_health
    
    Returns: Actual amount healed
    """
    # TODO: Implement healing
    # Calculate actual healing (don't exceed max_health)
    # Update character health
    if is_character_dead(character):
        # Cannot heal a dead character, revival implemented later
        return 0
    
    current_health = character["health"]
    max_health = character["max_health"]
    
    # Calculate new health, ensuring it doesn't exceed max_health
    if current_health + amount > max_health:
        healed_amount = max_health - current_health
        character["health"] = max_health
    else:
        healed_amount = amount
        character["health"] = current_health + amount
    
    return healed_amount

def is_character_dead(character):
    """
    Check if character's health is 0 or below
    
    Returns: True if dead, False if alive
    """
    # TODO: Implement death check
    return character["health"] <= 0

def revive_character(character):
    """
    Revive a dead character with 50% health
    
    Returns: True if revived
    """
    # TODO: Implement revival
    # Restore health to half of max_health
    if not is_character_dead(character):
        # Character is alive still, nothing to do
        return False
    
    # Restore health to 50% of max_health when revived
    character["health"] = character["max_health"] // 2  # integer division, dont want a float num
    
    return True

# ============================================================================
# VALIDATION
# ============================================================================

def validate_character_data(character):
    """
    Validate that character dictionary has all required fields
    
    Required fields: name, class, level, health, max_health, 
                    strength, magic, experience, gold, inventory,
                    active_quests, completed_quests
    
    Returns: True if valid
    Raises: InvalidSaveDataError if missing fields or invalid types
    """
    # TODO: Implement validation
    # Check all required keys exist
    # Check that numeric values are numbers
    # Check that lists are actually lists
    required_keys = [
        "name", "class", "level", "health", "max_health",
        "strength", "magic", "experience", "gold",
        "inventory", "active_quests", "completed_quests"
    ]
    
    # Check all keys exist
    for key in required_keys:
        if key not in character:
            raise InvalidSaveDataError(f"Missing required character field: {key}")
    
    # Check numeric fields
    for num_key in ["level", "health", "max_health", "strength", "magic", "experience", "gold"]:
        if not isinstance(character[num_key], int):
            raise InvalidSaveDataError(f"{num_key} must be an integer, got {character[num_key]}")
    
    # Check lists
    for list_key in ["inventory", "active_quests", "completed_quests"]:
        if not isinstance(character[list_key], list):
            raise InvalidSaveDataError(f"{list_key} must be a list, got {character[list_key]}")
    
    return True

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== CHARACTER MANAGER TEST ===")
    
    # Create character
    char = create_character("Testhero", "Mage")
    
    # Save and reload
    save_character(char)
    loaded = load_character("Testhero")
    
    # Heal, add gold, gain experience
    heal_character(loaded, 30)
    add_gold(loaded, 50)
    gain_experience(loaded, 200)
    
    # Kill and revive
    loaded['health'] = 0
    revive_character(loaded)
    
    # Print concise summary
    print(f"Name: {loaded['name']}, Class: {loaded['class']}, Level: {loaded['level']}")
    print(f"HP: {loaded['health']}/{loaded['max_health']}, STR: {loaded['strength']}, MAG: {loaded['magic']}")
    print(f"Gold: {loaded['gold']}, Inventory: {loaded['inventory']}")
    
    # Cleanup test save
    delete_character("Testhero")

