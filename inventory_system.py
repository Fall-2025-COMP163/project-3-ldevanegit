"""
COMP 163 - Project 3: Quest Chronicles
Inventory System Module - Starter Code

Name: Devane, Lemanuel

AI Usage: I used Chatgpt and Google Ai to help me with the structure or the code, in addition to assisting me with surveying different logic options and checking for syntax and other uncaught errors.

This module handles inventory management, item usage, and equipment.
"""

from custom_exceptions import (
    InventoryFullError,
    ItemNotFoundError,
    InsufficientResourcesError,
    InvalidItemTypeError
)

# Maximum inventory size
MAX_INVENTORY_SIZE = 20

# ============================================================================
# INVENTORY MANAGEMENT
# ============================================================================

def add_item_to_inventory(character, item_id):
    """
    Add an item to character's inventory
    
    Args:
        character: Character dictionary
        item_id: Unique item identifier
    
    Returns: True if added successfully
    Raises: InventoryFullError if inventory is at max capacity
    """
    inventory = character.setdefault("inventory", [])

    if len(inventory) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory is full!")

    inventory.append(item_id)
    return True

def remove_item_from_inventory(character, item_id):
    """
    Remove an item from character's inventory
    
    Args:
        character: Character dictionary
        item_id: Item to remove
    
    Returns: True if removed successfully
    Raises: ItemNotFoundError if item not in inventory
    """
    inventory = character.setdefault("inventory", [])

    if item_id not in inventory:
        raise ItemNotFoundError(f"Item '{item_id}' not found!")

    inventory.remove(item_id)
    return True

def has_item(character, item_id):
    """
    Check if character has a specific item
    
    Returns: True if item in inventory, False otherwise
    """
    return True if item_id in character.get("inventory", []) else False


def count_item(character, item_id):
    """
    Count how many of a specific item the character has
    
    Returns: Integer count of item
    """
    # TODO: Implement item counting
    # Use list.count() method
    return character.get("inventory", []).count(item_id)

def get_inventory_space_remaining(character):
    """
    Calculate how many more items can fit in inventory
    
    Returns: Integer representing available slots
    """
    return MAX_INVENTORY_SIZE - len(character.get("inventory", []))

def clear_inventory(character):
    """
    Remove all items from inventory
    
    Returns: List of removed items
    """
    # TODO: Implement inventory clearing
    # Save current inventory before clearing
    removed_items = character.get("inventory", []).copy()
    character["inventory"] = []
    return removed_items

# ============================================================================
# ITEM USAGE
# ============================================================================

def use_item(character, item_id, item_data):
    """
    Use a consumable item from inventory
    
    Args:
        character: Character dictionary
        item_id: Item to use
        item_data: Item information dictionary from game_data
    
    Item types and effects:
    - consumable: Apply effect and remove from inventory
    - weapon/armor: Cannot be "used", only equipped
    
    Returns: String describing what happened
    Raises: 
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'consumable'
    """
    if item_id not in character.get("inventory", []):
        raise ItemNotFoundError(f"Item '{item_id}' not found!")

    if item_data["type"] != "consumable":
        raise InvalidItemTypeError("Item is not consumable!")

    # Parse effect
    parsed = parse_item_effect(item_data["effect"])
    stat_name = parsed[0]
    value = parsed[1]

    # Apply effect
    apply_stat_effect(character, stat_name, value)

    # Remove potion
    remove_item_from_inventory(character, item_id)
    # Return result string, if value positive you get a buff, elif you get nerfed, else no effect
    if value > 0:
        return (f"Used {item_id}! {stat_name} increased by {value}.")
    elif value < 0:
        return (f"Used {item_id}! {stat_name} decreased by {abs(value)}.")
    else:
        return (f"Used {item_id}! No effect.")

def equip_weapon(character, item_id, item_data):
    """
    Equip a weapon
    
    Args:
        character: Character dictionary
        item_id: Weapon to equip
        item_data: Item information dictionary
    
    Weapon effect format: "strength:5" (adds 5 to strength)
    
    If character already has weapon equipped:
    - Unequip current weapon (remove bonus)
    - Add old weapon back to inventory
    
    Returns: String describing equipment change
    Raises:
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'weapon'
    """
    if item_id not in character.get("inventory", []):
        raise ItemNotFoundError("Weapon not in inventory!")

    if item_data["type"] != "weapon":
        raise InvalidItemTypeError("Item is not a weapon!")

    # Unequip current weapon if exists
    if character.get("equipped_weapon") is not None:
        unequip_weapon(character,item_data_dict)

    # Apply weapon stats
    parsed = parse_item_effect(item_data["effect"])
    stat_name = parsed[0]
    value = parsed[1]
    apply_stat_effect(character, stat_name, value)

    # Equip weapon
    character["equipped_weapon"] = item_id
    remove_item_from_inventory(character, item_id)

    return (f"Equipped weapon: {item_id}")


def equip_armor(character, item_id, item_data):
    """
    Equip armor
    
    Args:
        character: Character dictionary
        item_id: Armor to equip
        item_data: Item information dictionary
    
    Armor effect format: "max_health:10" (adds 10 to max_health)
    
    If character already has armor equipped:
    - Unequip current armor (remove bonus)
    - Add old armor back to inventory
    
    Returns: String describing equipment change
    Raises:
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'armor'
    """
    if item_id not in character.get("inventory", []):
        raise ItemNotFoundError("Armor not in inventory!")

    if item_data["type"] != "armor":
        raise InvalidItemTypeError("Item is not armor!")

    # Unequip current armor if exists
    if character.get("equipped_armor") is not None:
        unequip_armor(character,item_data_dict)

    # Apply armor stats
    parsed = parse_item_effect(item_data["effect"])
    stat_name = parsed[0]
    value = parsed[1]
    apply_stat_effect(character, stat_name, value)

    # Equip armor
    character["equipped_armor"] = item_id
    remove_item_from_inventory(character, item_id)

    return (f"Equipped armor: {item_id}")


def unequip_weapon(character, item_data_dict):
    """
    Remove equipped weapon and return it to inventory
    
    Returns: Item ID that was unequipped, or None if no weapon equipped
    Raises: InventoryFullError if inventory is full
    """
    # TODO: Implement weapon unequipping
    if character.get("equipped_weapon") is None:
        return None

    weapon_id = character["equipped_weapon"]
    weapon_data = item_data_dict[weapon_id]

    # Remove weapon stat bonus
    parsed = parse_item_effect(weapon_data["effect"])
    stat_name = parsed[0]
    value = parsed[1]
    apply_stat_effect(character, stat_name, -value)

    # Check inventory space
    if len(character.get("inventory", [])) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("No space to unequip weapon!")

    # Return weapon to inventory
    character["inventory"].append(weapon_id)
    character["equipped_weapon"] = None

    return weapon_id

def unequip_armor(character,item_data_dict):
    """
    Remove equipped armor and return it to inventory
    
    Returns: Item ID that was unequipped, or None if no armor equipped
    Raises: InventoryFullError if inventory is full
    """
    if character.get("equipped_armor") is None:
        return None

    armor_id = character["equipped_armor"]
    armor_data = item_data_dict[armor_id]

    # Remove armor stat bonus
    parsed = parse_item_effect(armor_data["effect"])
    stat_name = parsed[0]
    value = parsed[1]
    apply_stat_effect(character, stat_name, -value)

    # Check inventory space
    if len(character.get("inventory", [])) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("No space to unequip armor!")

    # Return armor to inventory
    character["inventory"].append(armor_id)
    character["equipped_armor"] = None

    return armor_id
# ============================================================================
# SHOP SYSTEM
# ============================================================================

def purchase_item(character, item_id, item_data):
    """
    Purchase an item from a shop
    
    Args:
        character: Character dictionary
        item_id: Item to purchase
        item_data: Item information with 'cost' field
    
    Returns: True if purchased successfully
    Raises:
        InsufficientResourcesError if not enough gold
        InventoryFullError if inventory is full
    """
    cost = item_data["cost"]
    #check for funds and inventory space
    if character["gold"] < cost:
        raise InsufficientResourcesError("Not enough gold!")

    if len(character.get("inventory", [])) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory full!")

    character["gold"] -= cost
    character["inventory"].append(item_id)
    return True

def sell_item(character, item_id, item_data):
    """
    Sell an item for half its purchase cost
    
    Args:
        character: Character dictionary
        item_id: Item to sell
        item_data: Item information with 'cost' field
    
    Returns: Amount of gold received
    Raises: ItemNotFoundError if item not in inventory
    """
    #check if item in inventory
    if item_id not in character.get("inventory", []):
        raise ItemNotFoundError("Item not in inventory!")

    sell_price = item_data["cost"] // 2
    #gives gold for sell price and removes item from inventory
    character["gold"] += sell_price
    character["inventory"].remove(item_id)

    return sell_price

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_item_effect(effect_string):
    """
    Parse item effect string into stat name and value
    
    Args:
        effect_string: String in format "stat_name:value"
    
    Returns: Tuple of (stat_name, value)
    Example: "health:20" → ("health", 20)
    """
    parts = effect_string.split(":")   # example: ["health", "20"]

    stat_name = parts[0]
    value = int(parts[1])

    return (stat_name, value)

def apply_stat_effect(character, stat_name, value):
    """
    Apply a stat modification to character
    
    Valid stats: health, max_health, strength, magic
    
    Note: health cannot exceed max_health
    """
    character[stat_name] += value

    # Clamp health
    if stat_name == "health":
        if character["health"] > character["max_health"]:
            character["health"] = character["max_health"]
        elif character["health"] < 0:
            character["health"] = 0

def display_inventory(character, item_data_dict):
    """
    Display character's inventory in formatted way
    
    Args:
        character: Character dictionary
        item_data_dict: Dictionary of all item data
    
    Shows item names, types, and quantities
    """
    inv = character.get("inventory", [])
    if not inv:
        print("Inventory empty.")
        return

    counted = {}
    for item in inv:
        counted[item] = counted.get(item, 0) + 1

    for item_id, qty in counted.items():
        item = item_data_dict[item_id]
        print(f"{item['name']} (x{qty}) - {item['type']}")


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== INVENTORY SYSTEM TEST ===")
    #ChatGPT helped me with structuring the code to formulate test my functions in case there were no test cases to use
    
    # Test character
    test_char = {
        "inventory": [],
        "gold": 100,
        "health": 50,
        "max_health": 80,
        "strength": 5,
        "magic": 3,
        "equipped_weapon": None,
        "equipped_armor": None
    }

    # Test item data dictionary
    item_data_dict = {
        "health_potion": {
            "name": "Health Potion",
            "type": "consumable",
            "effect": "health:20",
            "cost": 10
        },
        "iron_sword": {
            "name": "Iron Sword",
            "type": "weapon",
            "effect": "strength:5",
            "cost": 50
        },
        "leather_armor": {
            "name": "Leather Armor",
            "type": "armor",
            "effect": "max_health:10",
            "cost": 40
        }
    }

    # --- Test adding items ---
    print("\nAdding items to inventory...")
    add_item_to_inventory(test_char, "health_potion")
    add_item_to_inventory(test_char, "iron_sword")
    add_item_to_inventory(test_char, "leather_armor")
    display_inventory(test_char, item_data_dict)

    # --- Test using a consumable ---
    print("\nUsing a health potion...")
    try:
        result = use_item(test_char, "health_potion", item_data_dict["health_potion"])
        print(result)
    except (ItemNotFoundError, InvalidItemTypeError) as e:
        print(e)
    display_inventory(test_char, item_data_dict)
    print(f"Health: {test_char['health']}/{test_char['max_health']}")

    # --- Test equipping weapon ---
    print("\nEquipping iron sword...")
    try:
        result = equip_weapon(test_char, "iron_sword", item_data_dict["iron_sword"])
        print(result)
    except (ItemNotFoundError, InvalidItemTypeError) as e:
        print(e)
    display_inventory(test_char, item_data_dict)
    print(f"Strength: {test_char['strength']}")

    # --- Test equipping armor ---
    print("\nEquipping leather armor...")
    try:
        result = equip_armor(test_char, "leather_armor", item_data_dict["leather_armor"])
        print(result)
    except (ItemNotFoundError, InvalidItemTypeError) as e:
        print(e)
    display_inventory(test_char, item_data_dict)
    print(f"Max Health: {test_char['max_health']}")

    # --- Test unequipping weapon ---
    print("\nUnequipping weapon...")
    try:
        unequipped = unequip_weapon(test_char,item_data_dict)
        print(f"Unequipped: {unequipped}")
    except InventoryFullError as e:
        print(e)
    display_inventory(test_char, item_data_dict)
    print(f"Strength: {test_char['strength']}")

    # --- Test unequipping armor ---
    print("\nUnequipping armor...")
    try:
        unequipped = unequip_armor(test_char,item_data_dict)
        print(f"Unequipped: {unequipped}")
    except InventoryFullError as e:
        print(e)
    display_inventory(test_char, item_data_dict)
    print(f"Max Health: {test_char['max_health']}")

    # --- Test purchase and sell ---
    print("\nPurchasing and selling items...")
    try:
        purchase_item(test_char, "health_potion", item_data_dict["health_potion"])
        print("Purchased health potion.")
        sell_price = sell_item(test_char, "health_potion", item_data_dict["health_potion"])
        print(f"Sold health potion for {sell_price} gold.")
    except (InventoryFullError, InsufficientResourcesError, ItemNotFoundError) as e:
        print(e)
    display_inventory(test_char, item_data_dict)
    print(f"Gold: {test_char['gold']}")
