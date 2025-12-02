"""
COMP 163 - Project 3: Quest Chronicles
Game Data Module - Starter Code

Name: Devane, Lemanuel

AI Usage: I used Chatgpt and Google Ai to help me with the structure or the code, in addition to assisting me with surveying different logic options and checking for syntax and other uncaught errors.

This module handles loading and validating game data from text files.
"""

import os
from custom_exceptions import (
    InvalidDataFormatError,
    MissingDataFileError,
    CorruptedDataError)

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

def load_quests(filename=os.path.join("data", "quests.txt")):
    """
    Load quest data from file
    
    Expected format per quest (separated by blank lines):
    QUEST_ID: unique_quest_name
    TITLE: Quest Display Title
    DESCRIPTION: Quest description text
    REWARD_XP: 100
    REWARD_GOLD: 50
    REQUIRED_LEVEL: 1
    PREREQUISITE: previous_quest_id (or NONE)
    
    Returns: Dictionary of quests {quest_id: quest_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    #if file does not exist, a MissingDataFileError is raised
    if not os.path.exists(filename):
        raise MissingDataFileError(f"Quest file not found: {filename}")
    
    quests = {}
    try:
        # Open with UTF-8 and replace invalid bytes to avoid Unicode errors, if file cant be read in bytes, errors will allow Python to read it in its default way(Chatgpt)
        with open(filename, "r", encoding="utf-8", errors="replace") as f:
            lines = f.read().splitlines()

        block = []
        for line in lines:
            
            # 1. Clean up the line (strip whitespace) for immediate checks
            cleaned_line = line.strip() 

            # 2. Check for the blank line separator first (triggers block processing)
            if cleaned_line == "": 
                if block:
                    try:
                        quest = parse_quest_block(block)
                        quest_id = quest["quest_id"]
                        validate_quest_data(quest)
                        quests[quest_id] = quest
                    except KeyError as e:
                        raise InvalidDataFormatError(f"Missing key in quest block: {e}")
                    except Exception as e:
                        raise CorruptedDataError(f"Invalid content in quest block: {e}")
                    block = []
            else:
                # =========================================================================
                # 🛠️ CRITICAL FIXES FOR CORRUPTED DATA ERROR (FIX #2) 🛠️
                # =========================================================================
                # Check for comments (optional but good)
                if cleaned_line.startswith('#'):
                    continue
                
                # CRITICAL: Check for the required delimiter (colon)
                if ':' not in cleaned_line:
                    raise InvalidDataFormatError(f"Line missing ': ': {line}")
                # =========================================================================

                # If the line passed validation, it is added to the current block
                block.append(line)
    
        
        # Process any final block without a trailing blank line
        if block:
            try:
                quest = parse_quest_block(block)
                quest_id = quest["quest_id"]
                validate_quest_data(quest)
                quests[quest_id] = quest
            except KeyError as e:
                raise InvalidDataFormatError(f"Missing key in quest block: {e}")
            except Exception as e:
                raise CorruptedDataError(f"Invalid content in quest block: {e}")

        return quests

    except FileNotFoundError:
        raise MissingDataFileError(f"Quest file not found: {filename}")
    except InvalidDataFormatError as e:
        # Propagate format errors
        raise e
    except Exception as e:
        # Any unexpected error → CorruptedDataError
        raise CorruptedDataError(f"Unable to read quest file: {e}")


def load_items(filename=os.path.join("data", "items.txt")):
    """
    Load item data from file
    """
    if not os.path.exists(filename):
        raise MissingDataFileError(f"Item file not found: {filename}")
    
    items = {}
    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
        
        block = []
        for line in lines:
            cleaned = line.strip()

            # Block separator '---'
            if cleaned == "---":
                if block:
                    item = parse_item_block(block)
                    item_id = item["item_id"]
                    items[item_id] = item
                    block = []
                continue

            # Blank line = end of block
            if cleaned == "":
                if block:
                    item = parse_item_block(block)
                    item_id = item["item_id"]
                    items[item_id] = item
                    block = []
                continue

            # Validate format
            if ": " not in line:
                raise InvalidDataFormatError(f"Line missing ': ': {line}")

            block.append(line)

        # Last block
        if block:
            item = parse_item_block(block)
            item_id = item["item_id"]
            items[item_id] = item
        
        return items
    
    except FileNotFoundError:
        raise MissingDataFileError(f"Item file not found: {filename}")
    except InvalidDataFormatError as e:
        raise e
    except Exception as e:
        raise CorruptedDataError(f"Unable to read item file: {e}")


def validate_quest_data(quest_dict):
    """
    Validate that quest dictionary has all required fields
    
    Required fields: quest_id, title, description, reward_xp, 
                    reward_gold, required_level, prerequisite
    
    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields
    """
    # TODO: Implement validation
    # Check that all required keys exist
    # Check that numeric values are actually numbers
    required_keys = ["quest_id", "title", "description", 
                     "reward_xp", "reward_gold", "required_level", "prerequisite"]
    
    for key in required_keys:
        if key not in quest_dict:
            raise InvalidDataFormatError(f"Missing required quest field: {key}")
    
    # Check numeric fields are integers
    for num_key in ["reward_xp", "reward_gold", "required_level"]:
        if not isinstance(quest_dict[num_key], int):
            raise InvalidDataFormatError(f"{num_key} must be an integer, got {quest_dict[num_key]}")
    
    return True

def validate_item_data(item_dict):
    """
    Validate that item dictionary has all required fields
    
    Required fields: item_id, name, type, effect, cost, description
    Valid types: weapon, armor, consumable
    
    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields or invalid type
    """
    # TODO: Implement validation
    required_keys = ["item_id", "name", "type", "effect", "cost", "description"]
    valid_types = ["weapon", "armor", "consumable"]
    
    for key in required_keys:
        if key not in item_dict:
            raise InvalidDataFormatError(f"Missing required item field: {key}")
    
    # Check type
    if item_dict["type"].lower() not in valid_types:
        raise InvalidDataFormatError(f"Invalid item type: {item_dict['type']}")
    
    # Check cost is integer
    if not isinstance(item_dict["cost"], int):
        raise InvalidDataFormatError(f"Item cost must be an integer, got {item_dict['cost']}")
    # Check effect is a single-stat dictionary
    effect = item_dict.get("effect")  # get effect from dict

# If effect is a string, parse it into a single-stat dictionary
    if isinstance(effect, str):
        parts = effect.split(":")
        if len(parts) != 2:
            raise InvalidDataFormatError(f"Invalid effect format: {effect}")
        stat = parts[0].strip().lower()  # normalize stat name
        try:
            val = int(parts[1].strip())
        except ValueError:
            raise InvalidDataFormatError(f"Effect value must be int: {parts[1].strip()}")
    
        item_dict["effect"] = {stat: val}  # replace string with dict in the original dict
        effect = item_dict["effect"]       # reassign for further checks
    if not isinstance(effect, dict) or len(effect) != 1:
        raise InvalidDataFormatError(f"Effect must be a single stat dictionary, got: {effect}")
    
    # Validate the single stat and value without unpacking
    stat_key, stat_val = list(effect.items())[0]
    if not isinstance(stat_key, str):
        raise InvalidDataFormatError(f"Effect stat must be a string, got: {stat_key}")
    if not isinstance(stat_val, int):
        raise InvalidDataFormatError(f"Effect value must be an integer, got: {stat_val}")

    return True

def create_default_data_files():
    """
    Create default data files if they don't exist
    This helps with initial setup and testing
    """
    # TODO: Implement this function
    # Create data/ directory if it doesn't exist
    # Create default quests.txt and items.txt files
    # Handle any file permission errors appropriately
    data_dir = "data"
    quests_file = os.path.join(data_dir, "quests.txt")
    items_file = os.path.join(data_dir, "items.txt")
    
    try:
        # Create data directory if it doesn't exist
        if not os.path.exists(data_dir):
            os.mkdir(data_dir)
        
        # Create default quests.txt
        if not os.path.exists(quests_file):
            with open(quests_file, "w") as f:
                f.write(
"""QUEST_ID: quest_001
TITLE: Goblin Trouble
DESCRIPTION: Defeat the goblins in the forest.
REWARD_XP: 100
REWARD_GOLD: 50
REQUIRED_LEVEL: 1
PREREQUISITE: NONE

QUEST_ID: quest_002
TITLE: Orc Patrol
DESCRIPTION: Stop the orcs from raiding the village.
REWARD_XP: 200
REWARD_GOLD: 100
REQUIRED_LEVEL: 2
PREREQUISITE: quest_001
"""
                )
        
        # Create default items.txt
        if not os.path.exists(items_file):
            with open(items_file, "w") as f:
                f.write(
"""ITEM_ID: sword_001
NAME: Basic Sword
TYPE: weapon
EFFECT: strength:5
COST: 50
DESCRIPTION: A simple iron sword.

ITEM_ID: potion_001
NAME: Health Potion
TYPE: consumable
EFFECT: health:20
COST: 25
DESCRIPTION: Restores 20 HP.
"""
                )
    
    except PermissionError as e:
        raise CorruptedDataError("Cannot create data files due to permission error: " + str(e))
    except Exception as e:
        raise CorruptedDataError("Failed to create default data files: " + str(e))

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_quest_block(lines):
    """
    Parse a block of lines into a quest dictionary
    
    Args:
        lines: List of strings representing one quest
    
    Returns: Dictionary with quest data
    Raises: InvalidDataFormatError if parsing fails
    """
    quest_data = {}

    try:
        for line in lines:
            # Skip empty lines
            if not line.strip():
                continue

            # Ensure line contains ': ' before splitting
            if ": " not in line:
                raise InvalidDataFormatError(f"Line missing ': ': {line}")

            key, value = line.split(": ", 1)
            key = key.strip().lower()  # normalize keys
            value = value.strip()

            # Convert numeric fields to int
            if key in ["reward_xp", "reward_gold", "required_level"]:
                try:
                    value = int(value)
                except ValueError:
                    raise InvalidDataFormatError(f"Invalid number for {key}: {value}")

            # Convert "prerequisite" NONE to None
            if key == "prerequisite" and value.upper() == "NONE":
                value = None

            quest_data[key] = value

        # Ensure all required fields exist
        required_keys = [
            "quest_id", "title", "description",
            "reward_xp", "reward_gold",
            "required_level", "prerequisite"
        ]
        for k in required_keys:
            if k not in quest_data:
                raise InvalidDataFormatError(f"Missing required field: {k}")

        return quest_data

    except InvalidDataFormatError:
        raise
    except Exception as e:
        raise InvalidDataFormatError(f"Failed to parse quest block: {e}")

def parse_item_block(lines):
    """
    Parse a block of lines into an item dictionary
    
    Args:
        lines: List of strings representing one item
    
    Returns: Dictionary with item data
    Raises: InvalidDataFormatError if parsing fails
    """
    item_data = {}
    valid_types = ["weapon", "armor", "consumable"]

    try:
        for line in lines:
            if not line.strip():
                continue

            if ": " not in line:
                raise InvalidDataFormatError(f"Line missing ': ': {line}")

            key, value = line.split(": ", 1)
            key = key.strip().lower()
            value = value.strip()

            # Numeric fields
            if key == "cost":
                try:
                    value = int(value)
                except ValueError:
                    raise InvalidDataFormatError(f"Invalid number for {key}: {value}")

            # Type check
            if key == "type" and value.lower() not in valid_types:
                raise InvalidDataFormatError(f"Invalid item type: {value}")

            # Effect parsing
            if key == "effect":
                parts = value.split(":")
                if len(parts) != 2:
                    raise InvalidDataFormatError(f"Invalid effect format: {value}")

                stat = parts[0].strip()
                

                try:
                    stat_value = int(parts[1].strip())
                except ValueError:
                    raise InvalidDataFormatError(f"Effect value must be int: {parts[1].strip()}")

                item_data[key] = {stat: stat_value}
            else:
                item_data[key] = value

        # Ensure required fields exist
        required_keys = ["item_id", "name", "type", "effect", "cost", "description"]
        for k in required_keys:
            if k not in item_data:
                raise InvalidDataFormatError(f"Missing required field: {k}")

        return item_data

    except InvalidDataFormatError:
        raise
    except Exception as e:
        raise InvalidDataFormatError(f"Failed to parse item block: {e}")


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== GAME DATA MODULE TEST ===")
    
    try:
        create_default_data_files()
        print("Default data files ensured.")
    except Exception as e:
        print(f"Failed to create default data files: {e}")

    # Step 2: Load quests
    try:
        quests = load_quests()
        print(f"Loaded {len(quests)} quests.")
        # Display first quest as sample
        if quests:
            first_quest_id = list(quests.keys())[0]
            print(f"Sample quest ({first_quest_id}): {quests[first_quest_id]}")
    except MissingDataFileError:
        print("Quest file not found.")
    except InvalidDataFormatError as e:
        print(f"Invalid quest format: {e}")
    except Exception as e:
        print(f"Unexpected error loading quests: {e}")

    # Step 3: Load items
    try:
        items = load_items()
        print(f"Loaded {len(items)} items.")
        # Display first item as sample
        if items:
            first_item_id = list(items.keys())[0]
            print(f"Sample item ({first_item_id}): {items[first_item_id]}")
    except MissingDataFileError:
        print("Item file not found.")
    except InvalidDataFormatError as e:
        print(f"Invalid item format: {e}")
    except Exception as e:
        print(f"Unexpected error loading items: {e}")




