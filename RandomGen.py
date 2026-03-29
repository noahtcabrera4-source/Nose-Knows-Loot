import random
import math

# --- Data Tables ---
SPELLS = [
    "Adhere (Acid)", "Amplify", "Animate", "Apoplex (Fire)", "Aqua", "Babble", "Beast", "Bless", "Blink",
    "Burn (Fire)", "Charm", "Color", "Confuse", "Control", "Cure", "Disintegrate (Shock)", "Dispel",
    "Enchant", "Enflesh (Acid)", "Erupt (Fire)", "Exalt", "Fade", "Fear", "Fog", "Forge", "Freeze (Cold)",
    "Frostburn (Cold)", "Gas (Poison)", "Goop (Acid)", "Guide", "Gust", "Hold", "Hymn", "Junk", "Kinesis (Blunt)",
    "Knock", "Leech (Poison)", "Levitate", "Life", "Light (Fire)", "Mend", "Mirage", "Moon (Cold)", "Morph",
    "Mute", "Polymorph", "Portal", "Raise", "Rust (Acid)", "Shade", "Shrink", "Sleep", "Speak", "Sprout (Blunt)",
    "Tempo", "Terraform (Blunt)", "Truth", "Ward", "Zap (Shock)"
]

DELIVERIES = [
    {"name": "Aura", "base_cost": 2, "per_mana": 5, "unit": "ft radius", "start": 10},
    {"name": "Cone", "base_cost": 2, "per_mana": 5, "unit": "ft length", "start": 15},
    {"name": "Cube", "base_cost": 1, "per_mana": 5, "unit": "ft cube", "start": 5},
    {"name": "Imbue", "base_cost": 0, "per_mana": 1, "unit": "target(s)", "start": 1},
    {"name": "Glyph", "base_cost": 2, "per_mana": 0, "unit": "", "start": 0},
    {"name": "Line", "base_cost": 2, "per_mana": 10, "unit": "ft length", "start": 30},
    {"name": "Remote", "base_cost": 0, "per_mana": 1, "unit": "target(s)", "start": 1},
    {"name": "Sphere", "base_cost": 2, "per_mana": 5, "unit": "ft radius", "start": 5},
    {"name": "Touch", "base_cost": 0, "per_mana": 0, "unit": "", "start": 0}
]

POWERS = [
    ("Brutal", 2000), ("Cleave", 2000), ("Entangle", 1000), ("Keen", 2000), ("Long", 1000), ("Thrown", 2000),
    ("Bane: Niche", 500), ("Bane: Specific", 2000), ("Bane: General", 5000), ("Armor +1", 100), ("Armor +2", 5000),
    ("Armor +3", 50000), ("Protection +1", 1000), ("Protection +2", 10000), ("Protection +3", 100000),
    ("Trinket +1", 200), ("Trinket +2", 2500), ("Trinket +3", 10000), ("Weapon +1", 100), ("Weapon +2", 1250),
    ("Weapon +3", 5000), ("Benediction", 50000), ("Blasting", 5000), ("Precision", 10000), ("Soul Eater", 50000),
    ("Vicious", 25000), ("Vorpal", 50000), ("Blinking", 2000), ("Climbing", 500), ("Clinging", 2500),
    ("Displacement", 1000), ("Flying", 5000), ("Jumping I", 500), ("Jumping II", 2500), ("Jumping III", 12500),
    ("Levitation", 500), ("Swiftness I", 250), ("Swiftness II", 1000), ("Swiftness III", 5000), ("Waterwalk", 500),
    ("Webwalk", 500), ("Prot: Niche", 500), ("Prot: Specific", 2000), ("Prot: General", 5000), ("Bravery", 150),
    ("Clarity", 150), ("Repulsing", 150), ("Resistance", 2500), ("Nightvision", 100), ("Echolocation", 250),
    ("Sense Life", 10000), ("Sense Valuables", 10000), ("Tremors", 1000), ("Telepathy", 10000), ("True-Seeing", 20000),
    ("Strike I", 1000), ("Strike II", 2500), ("Strike III", 8000), ("After-Image I", 500), ("After-Image II", 2500),
    ("Ambassador", 1250), ("Aqua Lung", 5000), ("Darkness I", 500), ("Darkness II", 1250), ("Darkness III", 5000),
    ("Burning I", 4000), ("Burning II", 15000), ("Burning III", 64000), ("Holding", 200), ("Infinite", 1000),
    ("Invisibility I", 5000), ("Invisibility II", 50000), ("Lifesteal I", 1000), ("Lifesteal II", 12500),
    ("Lifesteal III", 50000), ("Loyalty", 1000), ("Manasteal I", 5000), ("Manasteal II", 20000),
    ("Manasteal III", 50000), ("Moonlit I", 500), ("Moonlit II", 1250), ("Moonlit III", 5000), ("Radiant I", 2000),
    ("Radiant II", 5000), ("Radiant III", 20000), ("Warning", 7500)
]

CURSES = [
    ("Anger", -250), ("Cowardice", -500), ("Doom", -750), ("Gullibility", -500), ("Vulnerability -1", -100),
    ("Vulnerability -2", -5000), ("Vulnerability -3", -5000), ("Weakness -1", -100), ("Weakness -2", -1250), ("Weakness -3", -500)
]

# --- Helper Functions ---
def roll(dice_str):
    if 'd' not in dice_str: return 0
    parts = dice_str.split('d')
    n = int(parts[0]) if parts[0] else 1
    t = int(parts[1])
    return sum(random.randint(1, t) for _ in range(n))

def generate_scroll(level):
    spell = random.choice(SPELLS)
    total_mana = random.randint(level, level * 2)
    delivery = random.choice(DELIVERIES)
    
    mana_left = total_mana - delivery['base_cost']
    if mana_left < 0: mana_left = 0
    
    # Distribute mana between Delivery, Damage, and Effect
    d_mana = random.randint(0, mana_left)
    mana_left -= d_mana
    
    dmg_mana = 0
    effect_mana = 0
    has_dmg = "(" in spell
    
    if has_dmg:
        dmg_mana = random.randint(0, mana_left)
        effect_mana = mana_left - dmg_mana
    else:
        effect_mana = mana_left

    # Construct Description
    d_val = delivery['start'] + (d_mana * delivery['per_mana']) if delivery['per_mana'] > 0 else delivery['start']
    d_str = f"{delivery['name']} {d_val}{delivery['unit']}".strip()
    
    dmg_str = f"{dmg_mana + 1}d6 damage" if has_dmg else ""
    eff_str = "Effect" if (not has_dmg or effect_mana > 0) else ""
    
    parts = [p for p in [d_str, dmg_str, eff_str] if p]
    return f"Scroll, {spell} ({', '.join(parts)}) [Total Mana: {total_mana}]"

def get_power_for_level(level):
    target_gold = 100 * (2 ** (level - 1))
    eligible = [p for p in POWERS if (target_gold/4) <= p[1] <= (target_gold*4)]
    if not eligible: eligible = [min(POWERS, key=lambda x: abs(x[1] - target_gold))]
    
    p_name, p_cost = random.choice(eligible)
    c_name, c_val = None, 0
    if p_cost > target_gold:
        for cn, cv in sorted(CURSES, key=lambda x: x[1], reverse=True):
            if p_cost + cv <= target_gold:
                c_name, c_val = cn, cv
                break
    return p_name, p_cost, c_name, c_val

def generate_loot(level):
    d66 = (random.randint(1, 6), random.randint(1, 6))
    item = ""
    is_eq = False
    budget = 100 * (2 ** (level - 1))

    # --- Loot Logic ---
    if d66[0] == 1:
        if d66[1] == 1: item, is_eq = random.choice(["Handaxe", "Battleaxe", "Halberd", "Greataxe"]), True
        elif d66[1] == 2: item, is_eq = random.choice(["Shortbow", "Longbow"]), True
        elif d66[1] == 3: item, is_eq = random.choice(["Caestus", "Gauntlet", "Katar"]), True
        elif d66[1] == 4: item, is_eq = "Light Armor", True
        else: return f"Gold: {roll('d100') * level} ({roll('d100')} x Lvl {level})"

    elif d66[0] == 2:
        if d66[1] == 1: item, is_eq = random.choice(["Hand Crossbow", "Light Crossbow"]), True
        elif d66[1] == 2: item, is_eq = random.choice(["Handgun", "Rifle", "Shotgun"]), True
        elif d66[1] == 3: item, is_eq = random.choice(["Club", "Flail", "Greatclub", "Mace", "Maul", "Warhammer"]), True
        elif d66[1] == 4: item, is_eq = "Leather Satchel", True
        elif d66[1] == 5: item, is_eq = "Medium Armor", True
        else: return f"Gold: {roll('d1000') * level} ({roll('d1000')} x Lvl {level})"

    elif d66[0] == 3:
        if d66[1] == 1: item, is_eq = random.choice(["Javelin", "Spear", "Staff", "Poleblade"]), True
        elif d66[1] == 2: item, is_eq = random.choice(["Buckler", "Standard Shield"]), True
        elif d66[1] == 3: item, is_eq = random.choice(["Dagger", "Shortsword", "Longsword", "Greatsword"]), True
        elif d66[1] == 4: item, is_eq = "Arcane Trinket", True
        elif d66[1] == 5: item, is_eq = "Divine Trinket", True
        else: return f"Gold: {roll('5d10') * level} ({roll('5d10')} x Lvl {level})"

    elif d66[0] == 4:
        if d66[1] == 1: item, is_eq = random.choice(["Lute", "Drum", "Flute", "Harp", "Trumpet"]), True
        elif d66[1] == 2: item = generate_scroll(level)
        elif d66[1] == 3: item, is_eq = "Heavy Cloak", True
        elif d66[1] == 4 or 5: item = f"Pixie Dust (d{random.randint(1,4)} doses)"
        else: item, is_eq = "Heavy Armor", True

    elif d66[0] == 5:
        if d66[1] == 1: item, is_eq = "Common Clothing" if random.randint(1,6) < 6 else "Formal Clothing", True
        elif d66[1] == 2: 
            num_spells = math.ceil(level / 2)
            item = f"Spellbook ({', '.join(random.sample(SPELLS, num_spells))})"
        elif d66[1] == 3: item, is_eq = "Gold Medallion", True
        elif d66[1] == 4: item, is_eq = "Occult Trinket", True
        elif d66[1] == 5: item, is_eq = "Primal Trinket", True
        else: return f"Gold: {roll('2d10') * level} ({roll('2d10')} x Lvl {level})"

    else: # Category 6
        if d66[1] == 1: item = "Scroll, Protection"
        elif d66[1] == 2: item, is_eq = "Golden Needle", True
        elif d66[1] == 3: item, is_eq = "Engraved Bracers", True
        elif d66[1] == 4: return f"Gold: {roll('d100') * level} ({roll('d100')} x Lvl {level})"
        elif d66[1] == 5: item, is_eq = "Signet Ring", True
        else: return f"Gold: {roll('5d10') * level} ({roll('5d10')} x Lvl {level})"

    # --- Output formatting ---
    if is_eq:
        pn, pc, cn, cc = get_power_for_level(level)
        res = f"ITEM: {item}\n >> Power: {pn} (+{pc}g)\n"
        if cn: res += f" >> Curse: {cn} ({cc}g)\n"
        res += f" >> TOTAL VALUE: {pc + cc}g (Budget: {budget}g)"
        return res
    return f"ITEM: {item}"

# --- Main Loop ---
print("=== LEGENDARY LOOT GENERATOR ===")
while True:
    val = input("\nEnter Character Level (or 'q' to quit): ")
    if val.lower() == 'q': break
    try:
        lvl = int(val)
        print("-" * 50)
        print(generate_loot(lvl))
        print("-" * 50)
    except ValueError:
        print("Please enter a valid number.")
    