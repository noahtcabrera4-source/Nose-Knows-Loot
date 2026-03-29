import streamlit as st
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

# W = Weapon, A = Armor, C = Accessory, G = Gear
POWERS = [
    ("Brutal", 2000, ["W"]), ("Cleave", 2000, ["W"]), ("Entangle", 1000, ["W"]), 
    ("Keen", 2000, ["W"]), ("Long", 1000, ["W"]), ("Thrown", 2000, ["W"]),
    ("Bane: Niche", 500, ["W", "A", "C", "G"]), ("Bane: Specific", 2000, ["W", "A", "C", "G"]), 
    ("Bane: General", 5000, ["W", "A", "C", "G"]), 
    ("Armor +1", 100, ["A", "C", "G"]), ("Armor +2", 5000, ["A", "C", "G"]), ("Armor +3", 50000, ["A", "C", "G"]),
    ("Protection +1", 1000, ["W", "A", "C", "G"]), ("Protection +2", 10000, ["W", "A", "C", "G"]), 
    ("Protection +3", 100000, ["W", "A", "C", "G"]),
    ("Trinket +1", 200, ["W", "A", "C", "G"]), ("Trinket +2", 2500, ["W", "A", "C", "G"]), 
    ("Trinket +3", 10000, ["W", "A", "C", "G"]),
    ("Weapon +1", 100, ["W"]), ("Weapon +2", 1250, ["W"]), ("Weapon +3", 5000, ["W"]),
    ("Benediction", 50000, ["W", "A", "C", "G"]), ("Blasting", 5000, ["W", "A", "C", "G"]), 
    ("Precision", 10000, ["W", "A", "C", "G"]), ("Soul Eater", 50000, ["W", "A", "C", "G"]), 
    ("Vicious", 25000, ["W", "A", "C", "G"]), ("Vorpal", 50000, ["W", "A", "C", "G"]),
    ("Blinking", 2000, ["A", "C", "G"]), ("Climbing", 500, ["A", "C", "G"]), 
    ("Clinging", 2500, ["A", "C", "G"]), ("Displacement", 1000, ["A", "C", "G"]), 
    ("Flying", 5000, ["A", "C", "G"]), ("Jumping I", 500, ["A", "C", "G"]), 
    ("Jumping II", 2500, ["A", "C", "G"]), ("Jumping III", 12500, ["A", "C", "G"]), 
    ("Levitation", 500, ["A", "C", "G"]), ("Swiftness I", 250, ["A", "C", "G"]), 
    ("Swiftness II", 1000, ["A", "C", "G"]), ("Swiftness III", 5000, ["A", "C", "G"]), 
    ("Waterwalk", 500, ["A", "C", "G"]), ("Webwalk", 500, ["A", "C", "G"]), 
    ("Prot: Niche", 500, ["W", "A", "C", "G"]), ("Prot: Specific", 2000, ["W", "A", "C", "G"]), 
    ("Prot: General", 5000, ["W", "A", "C", "G"]), ("Bravery", 150, ["W", "A", "C", "G"]),
    ("Clarity", 150, ["W", "A", "C", "G"]), ("Repulsing", 150, ["W", "A", "C", "G"]), 
    ("Resistance", 2500, ["W", "A", "C", "G"]), ("Nightvision", 100, ["W", "A", "C", "G"]), 
    ("Echolocation", 250, ["W", "A", "C", "G"]), ("Sense Life", 10000, ["W", "A", "C", "G"]),
    ("Sense Valuables", 10000, ["W", "A", "C", "G"]), ("Tremors", 1000, ["W", "A", "C", "G"]), 
    ("Telepathy", 10000, ["W", "A", "C", "G"]), ("True-Seeing", 20000, ["W", "A", "C", "G"]),
    ("Strike I", 1000, ["W"]), ("Strike II", 2500, ["W"]), ("Strike III", 8000, ["W"]), 
    ("After-Image I", 500, ["W", "A", "C", "G"]), ("After-Image II", 2500, ["W", "A", "C", "G"]),
    ("Ambassador", 1250, ["W", "A", "C", "G"]), ("Aqua Lung", 5000, ["W", "A", "C", "G"]), 
    ("Darkness I", 500, ["W", "A", "C", "G"]), ("Darkness II", 1250, ["W", "A", "C", "G"]), 
    ("Darkness III", 5000, ["W", "A", "C", "G"]), ("Burning I", 4000, ["W"]), 
    ("Burning II", 15000, ["W"]), ("Burning III", 64000, ["W"]), 
    ("Holding", 200, ["A", "C", "G"]), ("Infinite", 1000, ["W", "A", "C", "G"]), 
    ("Invisibility I", 5000, ["W", "A", "C", "G"]), ("Invisibility II", 50000, ["W", "A", "C", "G"]), 
    ("Lifesteal I", 1000, ["W"]), ("Lifesteal II", 12500, ["W"]), ("Lifesteal III", 50000, ["W"]),
    ("Loyalty", 1000, ["W"]), ("Manasteal I", 5000, ["W"]), ("Manasteal II", 20000, ["W"]),
    ("Manasteal III", 50000, ["W"]), ("Moonlit I", 500, ["W", "A", "C", "G"]), 
    ("Moonlit II", 1250, ["W", "A", "C", "G"]), ("Moonlit III", 5000, ["W", "A", "C", "G"]), 
    ("Radiant I", 2000, ["W", "A", "C", "G"]), ("Radiant II", 5000, ["W", "A", "C", "G"]), 
    ("Radiant III", 20000, ["W", "A", "C", "G"]), ("Warning", 7500, ["W", "A", "C", "G"])
]

CURSES = [
    ("Anger", -250), ("Cowardice", -500), ("Doom", -750), ("Gullibility", -500), 
    ("Vulnerability -1", -100), ("Vulnerability -2", -5000), ("Vulnerability -3", -5000), 
    ("Weakness -1", -100), ("Weakness -2", -1250), ("Weakness -3", -500)
]

# --- Helper Functions ---
def roll(dice_str):
    parts = dice_str.split('d')
    n = int(parts[0]) if parts[0] else 1
    t = int(parts[1])
    return sum(random.randint(1, t) for _ in range(n))

def generate_scroll(level):
    spell = random.choice(SPELLS)
    total_mana = random.randint(level, level * 2)
    delivery = random.choice(DELIVERIES)
    mana_left = max(0, total_mana - delivery['base_cost'])
    
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

    d_val = delivery['start'] + (d_mana * delivery['per_mana']) if delivery['per_mana'] > 0 else delivery['start']
    d_str = f"{delivery['name']} {d_val}{delivery['unit']}".strip()
    dmg_str = f"{dmg_mana + 1}d6 damage" if has_dmg else ""
    eff_str = "Effect" if (not has_dmg or effect_mana > 0) else ""
    
    parts = [p for p in [d_str, dmg_str, eff_str] if p]
    return f"📜 Scroll: {spell} ({', '.join(parts)})"

def get_power_for_item(level, category_tag):
    target_gold = 100 * (2 ** (level - 1))
    valid_powers = [p for p in POWERS if category_tag in p[2]]
    eligible = [p for p in valid_powers if (target_gold/4) <= p[1] <= (target_gold*4)]
    if not eligible: eligible = [min(valid_powers, key=lambda x: abs(x[1] - target_gold))]
    
    p_name, p_cost, _ = random.choice(eligible)
    c_name, c_val = None, 0
    if p_cost > target_gold:
        for cn, cv in sorted(CURSES, key=lambda x: x[1], reverse=True):
            if p_cost + cv <= target_gold:
                c_name, c_val = cn, cv
                break
    return p_name, p_cost, c_name, c_val

def get_gold_result(dice, level):
    active_dice = dice
    if dice == "2d1000" and level < 5:
        active_dice = "5d100"
        st.toast("Jackpot downgraded: 2d1000 locked until Level 5!")
    base = roll(active_dice)
    return f"💰 **{base * level:,} Gold** \n({base} on {active_dice} × Lvl {level})"

# --- App Interface ---
st.set_page_config(page_title="NoseKnowsLoot", page_icon="🔮")
st.title("NoseKnowsLoot")

level = st.number_input("Character Level", min_value=1, value=1)
budget = 100 * (2 ** (level - 1))
st.caption(f"Power Budget: **{budget:,}g**")

if st.button("Roll for Loot", type="primary", use_container_width=True):
    d66 = (random.randint(1, 6), random.randint(1, 6))
    item, category = "", None
    
    # Logic with explicit categorization
    if d66[0] == 1:
        if d66[1] <= 3: 
            item, category = random.choice(["Battleaxe", "Greataxe", "Longbow", "Gauntlet"]), "W"
        elif d66[1] == 4: item, category = "Light Armor", "A"
        else: item = get_gold_result("10d10", level)

    elif d66[0] == 2:
        if d66[1] <= 3: item, category = random.choice(["Handgun", "Shotgun", "Warhammer", "Flail"]), "W"
        elif d66[1] == 4: item, category = "Leather Satchel", "G"
        elif d66[1] == 5: item, category = "Medium Armor", "A"
        else: item = get_gold_result("5d100", level)

    elif d66[0] == 3:
        if d66[1] <= 3: item, category = random.choice(["Spear", "Longsword", "Greatsword", "Tower Shield"]), "W"
        elif d66[1] <= 5: item, category = "Arcane Trinket", "G"
        else: item = get_gold_result("10d10", level)

    elif d66[0] == 4:
        if d66[1] == 1: item, category = random.choice(["Lute", "Sacbut"]), "G"
        elif d66[1] == 2: item = generate_scroll(level) # No Category
        elif d66[1] == 3: item, category = "Heavy Cloak", "C"
        elif d66[1] == 4: item = f"✨ Pixie Dust (d{random.randint(1,4)} doses)" # No Category
        elif d66[1] == 5: item, category = "Golden Needle", None # Explicitly None
        elif d66[1] == 6: item, category = "Heavy Armor", "A"

    elif d66[0] == 5:
        if d66[1] == 1: item, category = "Formal Clothing", "C"
        elif d66[1] == 2: 
            num_spells = math.ceil(level / 2)
            item = f"📖 Spellbook ({', '.join(random.sample(SPELLS, num_spells))})"
        elif d66[1] == 3: item, category = "Gold Medallion", "C"
        elif d66[1] in [4, 5]: item, category = "Mystic Trinket", "G"
        else: item = get_gold_result("2d1000", level)

    else:
        if d66[1] == 1: item = "📜 Scroll, Protection" # No Category
        elif d66[1] == 2: item, category = "Golden Needle", None # Explicitly None
        elif d66[1] == 3: item, category = "Engraved Bracers", "A"
        elif d66[1] == 5: item, category = "Signet Ring", "C"
        else: item = get_gold_result("2d1000", level)

    st.divider()
    if category:
        pn, pc, cn, cc = get_power_for_item(level, category)
        st.subheader(f"Found: {item}")
        cat_names = {"W": "Weapon", "A": "Armor", "C": "Accessory", "G": "Gear"}
        st.caption(f"Category: {cat_names[category]}")
        
        c1, c2 = st.columns(2)
        with c1: st.success(f"**Boon:** {pn} (+{pc:,}g)")
        with c2: 
            if cn: st.error(f"**Curse:** {cn} ({cc:,}g)")
            else: st.info("No Curse")
        st.markdown(f"**Final Value:** `{pc + cc:,}g` / Budget: `{budget:,}g`")
    else:
        # Items with no category (Needles, Scrolls, Dust) output here
        st.subheader(item)
        if "Scroll" in item or "Spellbook" in item or "Dust" in item or "Needle" in item:
            st.caption("Static Item: No additional powers or budget math.")
