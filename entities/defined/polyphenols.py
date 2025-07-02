"""
Polyphenol entity lexicon. This list includes generic polyphenol categories,
chemical subgroups (flavonoids, stilbenes, etc.), and specific compounds frequently mentioned in biomedical literature.
"""

KNOWN_POLYPHENOLS = set([
    # General classes
    "polyphenol", "polyphenols", "flavonoid", "flavonoids", "phenolic compound", "phenolic compounds",

    # Flavonols
    "quercetin", "kaempferol", "myricetin", "isorhamnetin",

    # Flavan-3-ols
    "catechin", "epicatechin", "epicatechin gallate", "epigallocatechin", "epigallocatechin gallate",  # EGCG
    "gallocatechin", "gallocatechin gallate", "galloylated catechins",

    # Anthocyanins
    "cyanidin", "delphinidin", "malvidin", "pelargonidin", "peonidin", "petunidin",

    # Flavones
    "luteolin", "apigenin", "chrysin", "baicalein",

    # Isoflavones
    "genistein", "daidzein", "glycitein", "formononetin", "biochanin A",

    # Flavanones
    "hesperetin", "naringenin", "eriodictyol",

    # Stilbenes
    "resveratrol", "pterostilbene", "piceatannol",

    # Phenolic acids
    "gallic acid", "ellagic acid", "ferulic acid", "caffeic acid", "chlorogenic acid", "p-coumaric acid", "sinapic acid",
    "vanillic acid", "syringic acid", "protocatechuic acid",

    # Hydroxycinnamic acids
    "cinnamic acid", "o-coumaric acid", "m-coumaric acid",

    # Hydroxybenzoic acids
    "salicylic acid", "gentisic acid",

    # Tannins
    "tannin", "tannins", "proanthocyanidins", "condensed tannins", "hydrolysable tannins",

    # Lignans
    "secoisolariciresinol", "matairesinol", "pinoresinol", "lariciresinol",

    # Other specific compounds
    "curcumin", "oleuropein", "rosmarinic acid", "silymarin", "phloretin", "fisetin", "morin", "rutin", "naringin",

    # Abbreviations and formulas
    "egcg", "ecg", "ec", "gcg", "galloyl", "3,4-dihydroxybenzoic acid", "3,4,5-trihydroxybenzoic acid",
    "C15H14O6", "C14H12O6", "C15H14O5", "C16H14O7", "C13H12O7", "C14H12O7", "C15H12O6", "C13H10O4"
])
