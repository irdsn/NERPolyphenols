##################################################################################################
#                                          FOOD LEXICON                                          #
#                                                                                                #
# This module defines the set of known food-related terms used in biomedical NER tasks.          #
# These terms help detect FOOD entity candidates in PubMed abstracts during preprocessing.       #
# The list can be expanded with domain-specific vocabulary.                                      #
##################################################################################################

##################################################################################################
#                                      KNOWN FOOD ENTITIES                                       #
##################################################################################################

KNOWN_FOODS = set([
    # Common whole foods
    "grape", "grapes", "apple", "apples", "pear", "pears", "banana", "bananas",
    "orange", "oranges", "lemon", "lemons", "lime", "limes", "pineapple", "mango", "kiwi", "papaya",
    "avocado", "cherry", "cherries", "pomegranate", "blueberry", "blueberries", "raspberry", "raspberries",
    "blackberry", "blackberries", "strawberry", "strawberries", "plum", "plums", "apricot", "apricots",
    "peach", "peaches", "nectarine", "nectarines", "fig", "figs", "melon", "watermelon",

    # Dried fruits
    "raisins", "dried figs", "dried prunes", "dried apricots", "dried cranberries",

    # Vegetables
    "onion", "onions", "garlic", "broccoli", "spinach", "lettuce", "cabbage", "brussels sprouts",
    "carrot", "carrots", "tomato", "tomatoes", "pepper", "peppers", "zucchini", "eggplant", "cucumber",
    "beet", "beets", "cauliflower", "artichoke", "asparagus", "kale", "celery", "radish", "turnip",

    # Legumes & grains
    "soy", "soybean", "lentils", "chickpeas", "beans", "peas", "black beans", "kidney beans", "quinoa",
    "barley", "oats", "wheat", "brown rice", "whole grains",

    # Nuts & seeds
    "almond", "almonds", "walnut", "walnuts", "hazelnut", "hazelnuts", "pistachio", "pistachios",
    "cashew", "cashews", "pecan", "pecans", "peanuts", "chia seeds", "flaxseeds", "sunflower seeds",
    "pumpkin seeds", "sesame seeds",

    # Oils & fats
    "olive oil", "extra virgin olive oil", "canola oil", "sunflower oil", "coconut oil", "fish oil",
    "omega-3", "omega-6",

    # Teas and infusions
    "green tea", "black tea", "white tea", "oolong tea", "pu-erh tea", "hibiscus tea", "rooibos", "herbal tea",

    # Cocoa, coffee, wine
    "cocoa", "dark chocolate", "chocolate", "coffee", "espresso", "wine", "red wine", "white wine",
    "grape juice",

    # Others
    "turmeric", "ginger", "cinnamon", "parsley", "basil", "oregano", "thyme", "rosemary", "sage",
    "mint", "curry", "chili", "vinegar", "soy sauce", "tomato sauce", "mustard",

    # Derivatives and generic forms
    "plant extract", "fruit extract", "vegetable extract", "polyphenol-rich food", "polyphenol-rich extract",
    "juice", "infusion", "decoction", "fermented food", "plant-based food", "functional food"
])
