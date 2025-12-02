"""
COMP 163 - Project 3: Quest Chronicles
Quest Handler Module - Starter Code

Name: Devane, Lemanuel

AI Usage: I used Chatgpt and Google Ai to help me with the structure or the code, in addition to assisting me with surveying different logic options and checking for syntax and other uncaught errors.

This module handles quest management, dependencies, and completion.
"""

from custom_exceptions import (
    QuestNotFoundError,
    QuestRequirementsNotMetError,
    QuestAlreadyCompletedError,
    QuestNotActiveError,
    InsufficientLevelError
)

# ============================================================================
# QUEST MANAGEMENT
# ============================================================================

def accept_quest(character, quest_id, quest_data_dict):
    """
    Accept a new quest
    
    Args:
        character: Character dictionary
        quest_id: Quest to accept
        quest_data_dict: Dictionary of all quest data
    
    Requirements to accept quest:
    - Character level >= quest required_level
    - Prerequisite quest completed (if any)
    - Quest not already completed
    - Quest not already active
    
    Returns: True if quest accepted
    Raises:
        QuestNotFoundError if quest_id not in quest_data_dict
        InsufficientLevelError if character level too low
        QuestRequirementsNotMetError if prerequisite not completed
        QuestAlreadyCompletedError if quest already done
    """
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest '{quest_id}' not found!")
    
    quest = quest_data_dict[quest_id]

    if quest_id in character.get('completed_quests', []):
        raise QuestAlreadyCompletedError(f"Quest '{quest_id}' already completed!")
    
    if quest_id in character.get('active_quests', []):
        raise QuestNotActiveError(f"Quest '{quest_id}' is already active!")
    
    if character['level'] < quest['required_level']:
        raise InsufficientLevelError(f"Level {quest['required_level']} required for this quest!")
    
    prereq = quest.get('prerequisite', None)
    if prereq and prereq.upper() != 'NONE' and prereq not in character.get('completed_quests', []):
        raise QuestRequirementsNotMetError(f"Prerequisite quest '{prereq}' not completed!")

    character.setdefault('active_quests', []).append(quest_id)
    return True

def complete_quest(character, quest_id, quest_data_dict):
    """
    Complete an active quest and grant rewards
    
    Args:
        character: Character dictionary
        quest_id: Quest to complete
        quest_data_dict: Dictionary of all quest data
    
    Rewards:
    - Experience points (reward_xp)
    - Gold (reward_gold)
    
    Returns: Dictionary with reward information
    Raises:
        QuestNotFoundError if quest_id not in quest_data_dict
        QuestNotActiveError if quest not in active_quests"""
    
    character.setdefault('experience', 0)
    character.setdefault('gold', 0)
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest '{quest_id}' not found!")
    
    if quest_id not in character.get('active_quests', []):
        raise QuestNotActiveError(f"Quest '{quest_id}' is not active!")

    quest = quest_data_dict[quest_id]
    character['active_quests'].remove(quest_id)
    character.setdefault('completed_quests', []).append(quest_id)
    
    # Grant rewards
    character['experience'] += quest.get('reward_xp', 0)
    character['gold'] += quest.get('reward_gold', 0)
    
    return {'xp_gained': quest.get('reward_xp', 0), 'gold_gained': quest.get('reward_gold', 0)}

def abandon_quest(character, quest_id):
    """
    Remove a quest from active quests without completing it
    
    Returns: True if abandoned
    Raises: QuestNotActiveError if quest not active
    """
    if quest_id not in character.get('active_quests', []):
        raise QuestNotActiveError(f"Quest '{quest_id}' is not active!")
    
    character['active_quests'].remove(quest_id)
    return True

def get_active_quests(character, quest_data_dict):
    """
    Get full data for all active quests
    
    Returns: List of quest dictionaries for active quests
    """
    return [quest_data_dict[qid] for qid in character.get('active_quests', []) if qid in quest_data_dict]

def get_completed_quests(character, quest_data_dict):
    """
    Get full data for all completed quests
    
    Returns: List of quest dictionaries for completed quests
    """
    return [quest_data_dict[qid] for qid in character.get('completed_quests', []) if qid in quest_data_dict]



def get_available_quests(character, quest_data_dict):
    """
    Get quests that character can currently accept
    
    Available = meets level req + prerequisite done + not completed + not active
    
    Returns: List of quest dictionaries
    """
    available = []
    for qid, quest in quest_data_dict.items():
        if can_accept_quest(character, qid, quest_data_dict):
            available.append(quest)
    return available

# ============================================================================
# QUEST TRACKING
# ============================================================================

def is_quest_completed(character, quest_id):
    """
    Check if a specific quest has been completed
    
    Returns: True if completed, False otherwise
    """
    return quest_id in character.get('completed_quests', [])

def is_quest_active(character, quest_id):
    """
    Check if a specific quest is currently active
    
    Returns: True if active, False otherwise
    """
    return quest_id in character.get('active_quests', [])

def can_accept_quest(character, quest_id, quest_data_dict):
    """
    Check if character meets all requirements to accept quest
    
    Returns: True if can accept, False otherwise
    Does NOT raise exceptions - just returns boolean
    """
    if quest_id not in quest_data_dict:
        return False
    quest = quest_data_dict[quest_id]
    if quest_id in character.get('completed_quests', []):
        return False
    if quest_id in character.get('active_quests', []):
        return False
    if character['level'] < quest['required_level']:
        return False
    prereq = quest.get('prerequisite', None)
    if prereq is not None and prereq not in character.get('completed_quests', []):
        return False
    return True

def get_quest_prerequisite_chain(quest_id, quest_data_dict):
    """
    Get the full chain of prerequisites for a quest
    
    Returns: List of quest IDs in order [earliest_prereq, ..., quest_id]
    Example: If Quest C requires Quest B, which requires Quest A:
             Returns ["quest_a", "quest_b", "quest_c"]
    
    Raises: QuestNotFoundError if quest doesn't exist
    """
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest '{quest_id}' not found!")
    
    chain = []
    current = quest_id
    while current is not None:
        chain.insert(0, current)
        prereq = quest_data_dict[current].get('prerequisite', None)
        if prereq is None:
            break
        current = prereq
    return chain

# ============================================================================
# QUEST STATISTICS
# ============================================================================

def get_quest_completion_percentage(character, quest_data_dict):
    """
    Calculate what percentage of all quests have been completed
    
    Returns: Float between 0 and 100
    """
    total = len(quest_data_dict)
    completed = len(character.get('completed_quests', []))
    if total == 0:
        return 0.0
    return (completed / total) * 100

def get_total_quest_rewards_earned(character, quest_data_dict):
    """
    Calculate total XP and gold earned from completed quests
    
    Returns: Dictionary with 'total_xp' and 'total_gold'
    """
    total_xp = sum(quest_data_dict[qid].get('reward_xp', 0) for qid in character.get('completed_quests', []) if qid in quest_data_dict)
    total_gold = sum(quest_data_dict[qid].get('reward_gold', 0) for qid in character.get('completed_quests', []) if qid in quest_data_dict)
    return {'total_xp': total_xp, 'total_gold': total_gold}

def get_quests_by_level(quest_data_dict, min_level, max_level):
    """
    Get all quests within a level range
    
    Returns: List of quest dictionaries
    """
    return [q for q in quest_data_dict.values() if min_level <= q.get('required_level', 0) <= max_level]



# ============================================================================
# DISPLAY FUNCTIONS
# ============================================================================

def display_quest_info(quest_data):
    """
    Display formatted quest information
    
    Shows: Title, Description, Rewards, Requirements
    """
    # TODO: Implement quest display
    print(f"\n=== {quest_data['title']} ===")
    print(f"Description: {quest_data['description']}")
    # ... etc
    print(f"Required Level: {quest_data.get('required_level', 'N/A')}")
    print(f"Rewards: {quest_data.get('reward_xp', 0)} XP, {quest_data.get('reward_gold', 0)} gold")
    prereq = quest_data.get('prerequisite', 'NONE')
    print(f"Prerequisite: {prereq}")
    
def display_quest_list(quest_list):
    """
    Display a list of quests in summary format
    
    Shows: Title, Required Level, Rewards
    """
    # TODO: Implement quest list display
    for quest in quest_list:
        print(f"{quest['title']} (Level {quest.get('required_level', 'N/A')}) - Rewards: {quest.get('reward_xp', 0)} XP, {quest.get('reward_gold', 0)} gold")

def display_character_quest_progress(character, quest_data_dict):
    """
    Display character's quest statistics and progress
    
    Shows:
    - Active quests count
    - Completed quests count
    - Completion percentage
    - Total rewards earned
    """
    # TODO: Implement progress display
    active = len(character.get('active_quests', []))
    completed = len(character.get('completed_quests', []))
    percent = get_quest_completion_percentage(character, quest_data_dict)
    rewards = get_total_quest_rewards_earned(character, quest_data_dict)
    print(f"\nQuest Progress for {character.get('name', 'Unknown')}:")
    print(f"Active Quests: {active}")
    print(f"Completed Quests: {completed}")
    print(f"Completion: {percent:.1f}%")
    print(f"Total Rewards Earned: {rewards['total_xp']} XP, {rewards['total_gold']} gold")

# ============================================================================
# VALIDATION
# ============================================================================

def validate_quest_prerequisites(quest_data_dict):
    """
    Validate that all quest prerequisites exist
    
    Checks that every prerequisite (that's not "NONE") refers to a real quest
    
    Returns: True if all valid
    Raises: QuestNotFoundError if invalid prerequisite found
    """
    for qid, quest in quest_data_dict.items():
        prereq = quest.get('prerequisite', 'NONE')
        if prereq != 'NONE' and prereq not in quest_data_dict:
            raise QuestNotFoundError(f"Prerequisite '{prereq}' for quest '{qid}' not found!")
    return True


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== QUEST HANDLER TEST ===")
    
    # Test data
    test_char = {
        "level": 3,
        "active_quests": [],
        "completed_quests": [],
        "experience": 0,
        "gold": 0
    }
    #
    test_quests = {
        "slime_hunt": {
            "quest_id": "slime_hunt",
            "title": "Slime Hunt",
            "description": "Defeat 3 green slimes.",
            "reward_xp": 40,
            "reward_gold": 10,
            "required_level": 1,
            "prerequisite": "NONE"},
        "wolf_hunt": {
            "quest_id": "wolf_hunt",
            "title": "Wolf Hunt",
            "description": "Hunt down the forest wolf.",
            "reward_xp": 80,
            "reward_gold": 30,
            "required_level": 3,
            "prerequisite": "slime_hunt"}}
    #
    print("\n--- Test 1: Accept 'slime_hunt' ---")
    try:
        accept_quest(test_char, "slime_hunt", test_quests)
        print("PASS: slime_hunt accepted.")
    except Exception as e:
        print(f"Cannot accept: {e}")


