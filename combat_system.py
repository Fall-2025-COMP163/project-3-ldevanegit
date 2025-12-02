"""
COMP 163 - Project 3: Quest Chronicles
Combat System Module - Starter Code

Name: devane, lemanuel

AI Usage: I used Chatgpt and Google Ai to help me with the structure or the code, in addition to assisting me with surveying different logic options and checking for syntax and other uncaught errors.

Handles combat mechanics
"""
import random
import character_manager
from custom_exceptions import (
    InvalidTargetError,
    CombatNotActiveError,
    CharacterDeadError,
    AbilityOnCooldownError
)
from character_manager import is_character_dead, create_character



# ============================================================================
# ENEMY DEFINITIONS
# ============================================================================

def create_enemy(enemy_type):
    """
    Create an enemy based on type
    
    Example enemy types and stats:
    - goblin: health=50, strength=8, magic=2, xp_reward=25, gold_reward=10
    - orc: health=80, strength=12, magic=5, xp_reward=50, gold_reward=25
    - dragon: health=200, strength=25, magic=15, xp_reward=200, gold_reward=100
    
    Returns: Enemy dictionary
    Raises: InvalidTargetError if enemy_type not recognized
    """
    # TODO: Implement enemy creation
    # Return dictionary with: name, health, max_health, strength, magic, xp_reward, gold_reward
    valid_types = ["goblin", "orc", "dragon"]  # all lowercase to match stats dict

    enemy_type_key = enemy_type.lower()
    if enemy_type_key not in valid_types:
        raise InvalidTargetError(f"Invalid enemy type: {enemy_type}")

    enemy_stats = {
        "goblin": {"health": 50, "strength": 8, "magic": 2, "xp_reward": 25, "gold_reward": 10},
        "orc": {"health": 80, "strength": 12, "magic": 5, "xp_reward": 50, "gold_reward": 25},
        "dragon": {"health": 200, "strength": 25, "magic": 15, "xp_reward": 200, "gold_reward": 100}}
    
    
    stats = enemy_stats[enemy_type_key]
    return {
        "name": enemy_type.capitalize(),
        "health": stats["health"],
        "max_health": stats["health"],
        "strength": stats["strength"],
        "magic": stats["magic"],
        "xp_reward": stats["xp_reward"],
        "gold_reward": stats["gold_reward"]}

def get_random_enemy_for_level(character_level):
    """
    Get an appropriate enemy for character's level
    
    Level 1-2: Goblins
    Level 3-5: Orcs
    Level 6+: Dragons
    
    Returns: Enemy dictionary
    """
    # TODO: Implement level-appropriate enemy selection
    # Use if/elif/else to select enemy type
    # Call create_enemy with appropriate type
    if character_level <= 2:
        enemy_type = "goblin"
    elif 3 <= character_level <= 5:
        enemy_type = "orc"
    else:
        enemy_type = "dragon"
    
    return create_enemy(enemy_type)

# ============================================================================
# COMBAT SYSTEM
# ============================================================================

class SimpleBattle:
    """
    Simple turn-based combat system
    
    Manages combat between character and enemy
    """
    
    def __init__(self, character, enemy):
        """Initialize battle with character and enemy"""
        # TODO: Implement initialization
        # Store character and enemy
        # Set combat_active flag
        # Initialize turn counter
        
        # Store character and enemy
        self.character = character
        self.enemy = enemy
        
        # Flag to indicate if battle is ongoing
        self.combat_active = True
        
        # Track whose turn it is: 'player' or 'enemy'
       
        # Optional: store battle log messages
        self.battle_log = []
    
    def start_battle(self):
        """
        Start the combat loop
        
        Returns: Dictionary with battle results:
                {'winner': 'player'|'enemy', 'xp_gained': int, 'gold_gained': int}
        
        Raises: CharacterDeadError if character is already dead
        """
        # TODO: Implement battle loop
        # Check character isn't dead
        # Loop until someone dies
        # Award XP and gold if player wins
        self.character.setdefault('experience', 0)
        self.character.setdefault('gold', 0)
        #dictionary initializes cooldowns
        self.character.setdefault('cooldowns', {})
        if is_character_dead(self.character):
            raise CharacterDeadError(f"{self.character['name']} is already dead!")

        display_battle_log(f"Battle started between {self.character['name']} and {self.enemy['name']}!")

        while self.combat_active:
        # Player's turn
            self.player_turn()
        # Check if battle ended after player acts
            winner = self.check_battle_end()
            if winner:
                break

        # Enemy's turn
            self.enemy_turn()
        # Check if battle ended after enemy acts
            winner = self.check_battle_end()
            if winner:
                break
        results = {'winner': winner, 'xp_gained': 0, 'gold_gained': 0}
    # Battle ended, award rewards if player won
        if winner == "player":
            rewards = get_victory_rewards(self.enemy)
            self.character['experience'] += rewards['xp']
            self.character['gold'] += rewards['gold']
            display_battle_log(f"{self.character['name']} won! Gained {rewards['xp']} XP and {rewards['gold']} gold.")
            #Appends xp and gold won to characterif winner, returns nothing to dictionaryof stats if loser
            return {'winner': 'player', 'xp_gained': rewards['xp'], 'gold_gained': rewards['gold']}
    
        else:
            display_battle_log(f"{self.character['name']} was defeated by {self.enemy['name']}...")
            return {'winner': 'enemy', 'xp_gained': 0, 'gold_gained': 0}
    
    def player_turn(self):
        """
        Handle player's turn
        
        Displays options:
        1. Basic Attack
        2. Special Ability (if available)
        3. Try to Run
        
        Raises: CombatNotActiveError if called outside of battle
        """
        # TODO: Implement player turn
        # Check combat is active
        # Display options
        # Get player choice
        # Execute chosen action
        if not self.combat_active:
            raise CombatNotActiveError("Cannot act, combat is not active!")

    # Display current stats
        self.display_combat_stats(self.character, self.enemy)

    # Choose action
        print("\nChoose an action:")
        print("1. Basic Attack")
        print("2. Special Ability")
        print("3. Try to Run")

        choice = input("Enter choice (1-3): ").strip()

        if choice == "1":
            damage = self.calculate_damage(self.character, self.enemy)
            self.apply_damage(self.enemy, damage)
            self.display_battle_log(f"{self.character['name']} dealt {damage} damage to {self.enemy['name']}!")
        elif choice == "2":
        # Call special ability function
            result = use_special_ability(self.character, self.enemy)
            self.display_battle_log(result)
        elif choice == "3":
            escaped = self.attempt_escape()
            if escaped:
                self.display_battle_log(f"{self.character['name']} successfully escaped!")
                self.combat_active = False
            else:
                self.display_battle_log(f"{self.character['name']} failed to escape!")
        else:
            self.display_battle_log("Invalid choice! Turn skipped.")
        # Show updated stats after action
        self.display_combat_stats(self.character, self.enemy, self.combat_active)
        #decraments cooldowns every turn
        for ability in self.character['cooldowns']:
            if self.character['cooldowns'][ability] > 0:
                self.character['cooldowns'][ability] -= 1
    
    def enemy_turn(self):
        """
        Handle enemy's turn - simple AI
        
        Enemy always attacks
        
        Raises: CombatNotActiveError if called outside of battle
        """
        # TODO: Implement enemy turn
        # Check combat is active
        # Calculate damage
        # Apply to character
        if not self.combat_active:
            raise CombatNotActiveError("Cannot act, combat is not active!")

        damage = self.calculate_damage(self.enemy, self.character)
        self.apply_damage(self.character, damage)
        self.display_battle_log(f"{self.enemy['name']} attacks and deals {damage} damage to {self.character['name']}!")
        
        # Show updated stats after attack
        self.display_combat_stats(self.character, self.enemy, self.combat_active)

    def calculate_damage(self, attacker, defender):
        """
        Calculate damage from attack
        
        Damage formula: attacker['strength'] - (defender['strength'] // 4)
        Minimum damage: 1
        
        Returns: Integer damage amount
        """
        # TODO: Implement damage calculation
        damage = attacker.get('strength', 0) - (defender.get('strength', 0) // 4)
        return max(damage, 1)
    
    def apply_damage(self, target, damage):
        """
        Apply damage to a character or enemy
        
        Reduces health, prevents negative health
        """
        # TODO: Implement damage application
        target['health'] -= damage
        if target['health'] < 0:
            target['health'] = 0
        display_battle_log(f"{target['name']} takes {damage} damage! (HP: {target['health']}/{target['max_health']})")
    
    def check_battle_end(self):
        """
        Check if battle is over
        
        Returns: 'player' if enemy dead, 'enemy' if character dead, None if ongoing
        """
        # TODO: Implement battle end check
        if self.enemy['health'] <= 0:
            self.combat_active = False
            return 'player'
        elif self.character['health'] <= 0:
            self.combat_active = False
            return 'enemy'
        return None
    
    def attempt_escape(self):
        """
        Try to escape from battle
        
        50% success chance
        
        Returns: True if escaped, False if failed
        """
        # TODO: Implement escape attempt
        # Use random number or simple calculation
        # If successful, set combat_active to False
        success = random.random() < 0.5  # 50% chance
        if success:
            self.combat_active = False
        
        return success

# ============================================================================
# SPECIAL ABILITIES
# ============================================================================

def use_special_ability(character, enemy):
    """
    Use character's class-specific special ability
    
    Example abilities by class:
    - Warrior: Power Strike (2x strength damage)
    - Mage: Fireball (2x magic damage)
    - Rogue: Critical Strike (3x strength damage, 50% chance)
    - Cleric: Heal (restore 30 health)
    
    Returns: String describing what happened
    Raises: AbilityOnCooldownError if ability was used recently
    """
    if character['cooldowns'].get('special', 0) > 0:
        raise AbilityOnCooldownError(f"{character['name']}'s special ability is on cooldown!")
    character['cooldowns']['special'] = 2

    char_class = character['class'].lower()

    if char_class == 'warrior':
        return warrior_power_strike(character, enemy)
    elif char_class == 'mage':
        return mage_fireball(character, enemy)
    elif char_class == 'rogue':
        return rogue_critical_strike(character, enemy)
    elif char_class == 'cleric':
        return cleric_heal(character)
    else:
        return f"{character['name']} has no special ability!"
    # Set cooldown (2 turns)

    

    

def warrior_power_strike(character, enemy):
    """Warrior special ability"""
    damage = max(character['strength'] * 2 - (enemy['strength'] // 4), 1)
    enemy['health'] = max(enemy['health'] - damage, 0)
    return f"{character['name']} used Power Strike and dealt {damage} damage to {enemy['name']}!"

def mage_fireball(character, enemy):
    """Mage special ability"""
    damage = max(character['magic'] * 2 - (enemy['strength'] // 4), 1)
    enemy['health'] = max(enemy['health'] - damage, 0)
    return f"{character['name']} cast Fireball and dealt {damage} damage to {enemy['name']}!"

def rogue_critical_strike(character, enemy):
    """Rogue special ability"""
    if random.random() < 0.5:
        damage = max(character['strength'] * 3 - (enemy['strength'] // 4), 1)
        enemy['health'] = max(enemy['health'] - damage, 0)
        return f"{character['name']} landed a Critical Strike and dealt {damage} damage to {enemy['name']}!"
    else:
        return f"{character['name']} missed the Critical Strike!"


def cleric_heal(character):
    """Cleric special ability"""
    heal_amount = min(30, character['max_health'] - character['health'])
    character['health'] += heal_amount
    return f"{character['name']} healed for {heal_amount} HP!"

# ============================================================================
# COMBAT UTILITIES
# ============================================================================

def can_character_fight(character,combat_active=False):
    """
    Check if character is in condition to fight
    
    Returns: True if health > 0 and not in battle
    """
    # TODO: Implement fight check
    if character['health'] <= 0:
        return False  # Character is dead
    if combat_active:
        return False  # Already in a battle
    return True  # Can fight

def get_victory_rewards(enemy):
    """
    Calculate rewards for defeating enemy
    
    Returns: Dictionary with 'xp' and 'gold'
    """
    # TODO: Implement reward calculation
    return {'xp': enemy['xp_reward'], 'gold': enemy['gold_reward']}

def display_combat_stats(character, enemy, combat_active=True):
    """
    Display current combat status
    
    Shows both character and enemy health/stats
    """
    # TODO: Implement status display
    if combat_active == True:
        status = 'Active'
    else:
        status = 'Inactive'
    print(f"\nCombat Status: {status}")
    print(f"\n{character['name']}: HP={character['health']}/{character['max_health']}")
    print(f"{enemy['name']}: HP={enemy['health']}/{enemy['max_health']}")
    

def display_battle_log(message):
    """
    Display a formatted battle message
    """
    # TODO: Implement battle log display
    print(f">>> {message}")
    

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== COMBAT SYSTEM TEST ===")
    
    # Create a test character
    test_char = {
        'name': 'Hero',
        'class': 'Warrior',
        'health': 120,
        'max_health': 120,
        'strength': 15,
        'magic': 5,
        'experience': 0,
        'gold': 0,
        'cooldowns': {}}

    # Get a random enemy for character level 1
    enemy = get_random_enemy_for_level(character_level=1)
    print(f"Encountered enemy: {enemy['name']} (HP: {enemy['health']})")

    # Start a simple battle
    battle = SimpleBattle(test_char, enemy)
    try:
        result = battle.start_battle()
        print("\n=== BATTLE RESULT ===")
        print(f"Winner: {result['winner']}")
        print(f"XP gained: {result['xp_gained']}")
        print(f"Gold gained: {result['gold_gained']}")
        print(f"Character HP after battle: {test_char['health']}/{test_char['max_health']}")
        print(f"Character Gold: {test_char['gold']}, Experience: {test_char['experience']}")
    except CharacterDeadError as e:
        print(f"Cannot start battle: {e}")
    except Exception as e:
        print(f"Unexpected error during battle: {e}")
