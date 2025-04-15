import random
from faker import Faker

# Initialize Faker
fake = Faker()

# Define genre keywords that might appear in titles
genre_keywords = {
    'Mystery/Thriller': [
        "Shadow", "Secrets", "Murder", "Whisper", "Conspiracy", "Detective", "Darkness", "Crime", 
        "Deception", "Revenge", "Case", "Hunt", "Clue", "Hidden", "Silent", "Twisted", "Intrigue",
        "Pursuit", "Vanished", "Code", "Fatal", "Betrayal", "Evidence", "Unsolved"
    ],
    'Science Fiction': [
        "Galactic", "Future", "Robot", "Quantum", "Starship", "Artificial", "Alien", "Dystopia", 
        "Time", "Cyber", "Technocracy", "Singularity", "Parallel", "Cosmos", "Neural", 
        "Clones", "Terraform", "Nano", "Exoplanet", "Android", "Asteroid", "Colonization", "Genetic", "Dimension"
    ],
    'Fantasy': [
        "Dragon", "Enchanted", "Wizard", "Sword", "Kingdom", "Spell", "Magic", "Sorcery", "Elf", 
        "Prophecy", "Curse", "Legend", "Realm", "Portal", "Mystic", "Witch", "Knight", "Quest", "Oracle",
        "Forbidden", "Ancient", "Crystal", "Beast", "Wanderer"
    ],
    'Horror': [
        "Haunted", "Nightmare", "Ghost", "Blood", "Cursed", "Evil", "Shadow", "Terror", "Darkness",
        "Possessed", "Screams", "Macabre", "Paranormal", "Phantom", "Vampire", "Ghoul", "Horror", 
        "Demonic", "Fear", "Supernatural", "Whispering", "Haunting", "Wicked", "Underworld"
    ],
    'Romance': [
        "Love", "Heart", "Passion", "Forever", "Desire", "Kiss", "Soulmate", "Happily", 
        "Euphoria", "Embrace", "Affection", "Romantic", "Beloved", "Dreams", "Together", "Promise",
        "Attraction", "Enchantment", "Devotion", "Adoration", "Flames", "Whispered", "Cherished"
    ],
    'Literary Fiction': [
        "Truth", "Life", "Memory", "Soul", "Family", "Silence", "Words", "Path", "Vision", "Voice",
        "Solitude", "Journey", "Reflection", "Sorrow", "Identity", "Destiny", "River", "Wisdom", 
        "Loss", "Redemption", "Meaning", "Home", "Burden", "Legacy"
    ],
    'Biography & Autobiography': [
        "Life", "Memoirs", "Journey", "Reflections", "Story", "Legacy", "Chronicles", 
        "Revealed", "Lessons", "Spotlight", "Unveiled", "Inside", "Personal", "Witness", 
        "Rise", "Fall", "Struggle", "Success", "Footsteps", "Odds", "Scenes", "Shadows", 
        "Triumph", "Moments"
    ],
    'Memoir': [
        "Journey", "Experience", "Lessons", "Reflections", "Path", 
        "Road", "Looking", "Voices", "Eyes", "Remembering", 
        "Unspoken", "Ashes", "Chapters", "Tale", "Survival", 
        "Time", "Pages", "Boundaries", "Resilience", "Finding", 
        "Glimpse", "Fire", "Rain", "Truth"
    ],
    'Self-Help': [
        "Success", "Mindset", "Habits", "Growth", "Happiness", "Better", "Wellbeing", 
        "Unstoppable", "Improvement", "Productivity", "Resilience", "Mastering", 
        "Confidence", "Potential", "Clarity", "Barriers", "Transform", 
        "Balance", "Peace", "Fear", "Power", "Goals", "Rituals", "Intelligence"
    ],
    'History': [
        "Rise", "Fall", "Legacy", "Revolution", "Ancient", "Empire", "Story",
        "Chronicles", "Battle", "Change", "Turning", "Journey", "Heroes", "Villains", 
        "Civilizations", "Past", "Present", "Wars", "Power", "Timelines", "Legends", 
        "Origins", "Peace", "Conflict"
    ],
    'Science & Technology': [
        "Discovery", "Innovation", "Frontiers", "Evolution", "Science", "Technology", "Principles",
        "Breakthrough", "Invention", "Revolution", "Future", "Understanding", "Code", "Digital",
        "Theory", "Systems", "Analysis", "Research", "Quantum", "Data", "Network", "Progress", "Engine", "Method"
    ],
    'Philosophy': [
        "Thinking", "Wisdom", "Reality", "Knowledge", "Existence", "Meaning", "Truth",
        "Reason", "Understanding", "Ethics", "Consciousness", "Essence", "Questions",
        "Perception", "Logic", "Argument", "Concepts", "Morality", "Virtues", "Thought", 
        "Principles", "Mind", "Freedom", "Values"
    ],
    'Politics & Economics': [
        "Power", "State", "Market", "Economy", "Democracy", "Policy", "Nation",
        "Government", "Capital", "Reform", "Crisis", "Freedom", "Rights", "Leadership",
        "Justice", "System", "Social", "Wealth", "Revolution", "Influence", "Global", 
        "Political", "Strategy", "Institutions"
    ],
    'Business & Finance': [
        "Success", "Strategy", "Market", "Business", "Leadership", "Management", "Innovation",
        "Entrepreneur", "Investing", "Financial", "Fortune", "Growth", "Value", "Enterprise",
        "Money", "Assets", "Profit", "Career", "Achievement", "Corporate", "Planning", 
        "Wealth", "Potential", "Analysis"
    ],
    'Psychology': [
        "Mind", "Behavior", "Thinking", "Emotion", "Cognitive", "Psychological", "Consciousness",
        "Memory", "Perception", "Identity", "Self", "Personality", "Mental", "Understanding",
        "Patterns", "Disorders", "Healing", "Therapy", "Development", "Insight", 
        "Awareness", "Subconscious", "Response", "Analysis"
    ],
    'Travel & Exploration': [
        "Journey", "Discovery", "Adventure", "Wanderlust", "Expedition", "Travelogue", "Voyages",
        "Exploring", "Destination", "Traveler", "Wonders", "Paradise", "Odyssey", "Escape",
        "Hidden", "Roads", "Passport", "Wilderness", "Nomadic", "Exotic", "Trails", 
        "Cultures", "Horizons", "Landscapes"
    ],
    'Poetry': [
        "Verses", "Sonnets", "Stanzas", "Rhythm", "Words", "Song", "Lyrical", "Voice",
        "Soul", "Whispers", "Fragments", "Echoes", "Emotion", "Expression", "Lines",
        "Feelings", "Cadence", "Metaphor", "Silent", "Heart", "Wind", "Stillness", "Eternal", "Light"
    ],
    'Graphic Novels & Comics': [
        "Heroes", "Villains", "Adventures", "Origins", "Legacy", "Ultimate", "Amazing",
        "Legend", "Saga", "Tales", "Chronicles", "Guardians", "Defenders", "Avengers",
        "Secrets", "Powers", "Nemesis", "Mission", "Justice", "Vengeance", "Rebirth", 
        "Crisis", "Epic", "Worlds"
    ],
    'Children Books': [
        "Little", "Adventures", "Magic", "Wonderful", "Curious", "Friendly", "Amazing",
        "Brave", "Tiny", "Discovery", "Happy", "Journey", "Wonder", "Imagination", "Fun",
        "Animal", "Secret", "Friend", "Adventure", "Mystery", "School", "Magical", "First", "Day"
    ],
    'Cooking': [
        "Delicious", "Flavors", "Cooking", "Recipes", "Mastering", "Culinary", "Secrets",
        "Savory", "Sweet", "Chef", "Gourmet", "Traditional", "Farm", "Table", "Kitchen", 
        "Baking", "Spices", "Herbs", "Cuisine", "Taste", "Home", "Dish", "Feast", "Joy"
    ]
}

def generate_title(genre):
    """
    Generate a book title appropriate for the given genre.
    
    Args:
        genre (str): The book's genre
    
    Returns:
        str: A generated title
    """
    # Get keywords for this genre
    keywords = genre_keywords.get(genre, ["Book", "Story", "Tale"])
    
    # Helper lists for title patterns
    verbs = ["Find", "Discover", "Master", "Conquer", "Remember", "Unlock", "Pursue", "Create", "Build", "Embrace", "Survive"]
    prepositions = ["Beyond", "Under", "Above", "Between", "Within", "Before", "After", "Against", "Without", "Through"]
    places = ["City", "Forest", "Night", "Sky", "Mountains", "Sea", "Desert", "River", "Castle", "Village", 
              "Island", "Empire", "Kingdom", "Valley", "Palace", "Garden", "Tower", "Academy", "Sanctuary"]
    time_periods = ["Century", "Era", "Age", "Dynasty", "Generation", "Millennium", "Season", "Year", "Day", "Night"]
    adjectives = ["Hidden", "Lost", "Final", "Ultimate", "Secret", "Perfect", "Ancient", "Forgotten", "Endless", "Impossible"]
    
    # Generate title using various patterns
    title_type = random.randint(1, 12)
    
    if title_type == 1:
        # "The X of Y" format
        title = f"The {random.choice(keywords)} of {fake.first_name()}s"
    elif title_type == 2:
        # Adjective + Noun format
        title = f"The {random.choice(keywords)} {random.choice(keywords)}"
    elif title_type == 3:
        # Word + "and the" + keyword
        title = f"{random.choice(keywords)} and the {random.choice(keywords)}"
    elif title_type == 4:
        # Simple phrase with a keyword and year
        title = f"{random.choice(keywords)}: {random.randint(1800, 2022)}"
    elif title_type == 5:
        # "When X meets Y" format
        keywords_list = list(keywords)
        if len(keywords_list) > 1:
            keyword1 = random.choice(keywords_list)
            keywords_list.remove(keyword1)
            keyword2 = random.choice(keywords_list)
            title = f"When {keyword1} Meets {keyword2}"
        else:
            title = f"The {random.choice(keywords)} Effect"
    elif title_type == 6:
        # Keyword + "in the" + place format
        title = f"{random.choice(keywords)} in the {random.choice(places)}"
    elif title_type == 7:
        # "X: A Y Story" format
        title = f"{random.choice(keywords)}: A {random.choice(keywords)} Story"
    elif title_type == 8:
        # Single strong keyword with an adjective
        title = f"The {random.choice(adjectives)} {random.choice(keywords)}"
    elif title_type == 9:
        # How-to style
        title = f"How to {random.choice(verbs)} {random.choice(keywords)}"
    elif title_type == 10:
        # Character-based title with possession
        title = f"{fake.first_name()}'s {random.choice(keywords)}"
    elif title_type == 11:
        # Time period title
        title = f"{random.choice(keywords)} of the {random.choice(adjectives)} {random.choice(time_periods)}"
    else:  # title_type == 12
        # Location with preposition
        title = f"{random.choice(keywords)} {random.choice(prepositions)} {random.choice(places)}"
    
    return title.title()  # Return in title case