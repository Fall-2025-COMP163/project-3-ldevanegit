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
    CorruptedDataError
)

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

def load_quests(filename="data/quests.txt"):
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
            if line.strip() == "":
                if block:
                    try:
                        quest = parse_quest_block(block)
                        quest_id = quest["quest_id"]
                        quests[quest_id] = quest
                    except KeyError as e:
                        raise InvalidDataFormatError(f"Missing key in quest block: {e}")
                    except Exception as e:
                        raise CorruptedDataError(f"Invalid content in quest block: {e}")
                    block = []
            else:
                block.append(line)
        
        # Process any final block without a trailing blank line
        if block:
            try:
                quest = parse_quest_block(block)
                quest_id = quest["quest_id"]
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


def load_items(filename="data/items.txt"):
    """
    Load item data from file
    
    Expected format per item (separated by blank lines):
    ITEM_ID: unique_item_name
    NAME: Item Display Name
    TYPE: weapon|armor|consumable
    EFFECT: stat_name:value (e.g., strength:5 or health:20)
    COST: 100
    DESCRIPTION: Item description
    
    Returns: Dictionary of items {item_id: item_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    # TODO: Implement this function
    # Must handle same exceptions as load_quests
    if not os.path.exists(filename):
        raise MissingDataFileError(f"Item file not found: {filename}")
    
    items = {}
    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
        
        # Split file into blocks separated by blank lines
        block = []
        for line in lines:
            if line.strip() == "":
                if block:
                    item = parse_item_block(block)
                    item_id = item["item_id"]
                    items[item_id] = item
                    block = []
            else:
                block.append(line)
        
        # Catch any last block without trailing blank line
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
    quests_file = data_dir + "/quests.txt"
    items_file = data_dir + "/items.txt"
    
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
            "required_level", "prerequisite"]
        for k in required_keys:
            if k not in quest_data:
                raise InvalidDataFormatError(f"Missing required field: {k}")

        return quest_data

    except InvalidDataFormatError:
        # Propagate our own format errors
        raise
    except Exception as e:
        # Wrap any unexpected parsing error
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
            
            item_data[key] = value
        
        # Check required fields
        required_keys = ["item_id", "name", "type", "effect", "cost", "description"]
        for k in required_keys:
            if k not in item_data:
                raise InvalidDataFormatError(f"Missing required field: {k}")
        
        return item_data
    
    except Exception as e:
        if isinstance(e, InvalidDataFormatError):
            raise e
        raise InvalidDataFormatError(f"Failed to parse item block: {e}")


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== GAME DATA MODULE TEST ===")
    
    # Test creating default files
    # create_default_data_files()
    
    # Test loading quests
    # try:
    #     quests = load_quests()
    #     print(f"Loaded {len(quests)} quests")
    # except MissingDataFileError:
    #     print("Quest file not found")
    # except InvalidDataFormatError as e:
    #     print(f"Invalid quest format: {e}")
    
    # Test loading items
    # try:
    #     items = load_items()
    #     print(f"Loaded {len(items)} items")
    # except MissingDataFileError:
    #     print("Item file not found")
    # except InvalidDataFormatError as e:
    #     print(f"Invalid item format: {e}")

}")

