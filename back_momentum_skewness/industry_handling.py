import pandas as pd


def sic_to_industry_five(sic_code: int) -> str:
    """
    Converts a SIC code into the Fama-French 5 industry classification.

    Args:
        sic_code (int): The SIC code to convert.

    Returns:
        str: The Fama-French 5 industry classification.
    """

    # 1 Cnsmr  Consumer Durables, Nondurables, Wholesale, Retail, and Some Services (Laundries, Repair Shops)
    if (100 <= sic_code <= 999 or
        2000 <= sic_code <= 2399 or
        2700 <= sic_code <= 2749 or
        2770 <= sic_code <= 2799 or
        3100 <= sic_code <= 3199 or
        3940 <= sic_code <= 3989 or
        2500 <= sic_code <= 2519 or
        2590 <= sic_code <= 2599 or
        3630 <= sic_code <= 3659 or
        3710 <= sic_code <= 3711 or
        3714 <= sic_code <= 3714 or
        3716 <= sic_code <= 3716 or
        3750 <= sic_code <= 3751 or
        3792 <= sic_code <= 3792 or
        3900 <= sic_code <= 3939 or
        3990 <= sic_code <= 3999 or
        5000 <= sic_code <= 5999 or
        7200 <= sic_code <= 7299 or
        7600 <= sic_code <= 7699):
        return "Cnsmr"
        
    # 2 Manuf  Manufacturing, Energy, and Utilities
    elif (2520 <= sic_code <= 2589 or
          2600 <= sic_code <= 2699 or
          2750 <= sic_code <= 2769 or
          2800 <= sic_code <= 2829 or
          2840 <= sic_code <= 2899 or
          3000 <= sic_code <= 3099 or
          3200 <= sic_code <= 3569 or
          3580 <= sic_code <= 3621 or
          3623 <= sic_code <= 3629 or
          3700 <= sic_code <= 3709 or
          3712 <= sic_code <= 3713 or
          3715 <= sic_code <= 3715 or
          3717 <= sic_code <= 3749 or
          3752 <= sic_code <= 3791 or
          3793 <= sic_code <= 3799 or
          3860 <= sic_code <= 3899 or
          1200 <= sic_code <= 1399 or
          2900 <= sic_code <= 2999 or
          4900 <= sic_code <= 4949):
            return "Manuf"
    
    # 3 HiTec  Business Equipment, Telephone and Television Transmission
    elif (3570 <= sic_code <= 3579 or
          3622 <= sic_code <= 3622 or # Industrial controls
          3660 <= sic_code <= 3692 or
          3694 <= sic_code <= 3699 or
          3810 <= sic_code <= 3839 or
          7370 <= sic_code <= 7372 or # Services - computer programming and data processing
          7373 <= sic_code <= 7373 or # Computer integrated systems design
          7374 <= sic_code <= 7374 or # Services - computer processing, data preparation and processing
          7375 <= sic_code <= 7375 or # Services - information retrieval services
          7376 <= sic_code <= 7376 or # Services - computer facilities management service
          7377 <= sic_code <= 7377 or # Services - computer rental and leasing
          7378 <= sic_code <= 7378 or # Services - computer maintenance and repair
          7379 <= sic_code <= 7379 or # Services - computer related services
          7391 <= sic_code <= 7391 or # Services - R&D labs
          8730 <= sic_code <= 8734 or # Services - research, development, testing labs
          4800 <= sic_code <= 4899):
        return "HiTec"

    # 4 Hlth   Healthcare, Medical Equipment, and Drugs
    elif (2830 <= sic_code <= 2839 or
          3693 <= sic_code <= 3693 or
          3840 <= sic_code <= 3859 or
          8000 <= sic_code <= 8099):
        return "Hlth"
    
    # 5 Other  Other -- Mines, Constr, BldMt, Trans, Hotels, Bus Serv, Entertainment, Finance
    else:
        return "Other"


def sic_to_industry_ten(sic_code: int) -> str:
    """
    Converts a SIC code into the Fama-French 10 industry classification.

    Args:
        sic_code (int): The SIC code to convert.

    Returns:
        str: The Fama-French 10 industry classification.
    """

    # 1 NoDur  Consumer Nondurables -- Food, Tobacco, Textiles, Apparel, Leather, Toys
    if (100 <= sic_code <= 999 or
        2000 <= sic_code <= 2399 or
        2700 <= sic_code <= 2749 or
        2770 <= sic_code <= 2799 or
        3100 <= sic_code <= 3199 or
        3940 <= sic_code <= 3989):
        return "NoDur"

    # 2 Durbl  Consumer Durables -- Cars, TVs, Furniture, Household Appliances
    elif (2500 <= sic_code <= 2519 or
          2590 <= sic_code <= 2599 or
          3630 <= sic_code <= 3659 or
          3710 <= sic_code <= 3711 or
          3714 <= sic_code <= 3714 or
          3716 <= sic_code <= 3716 or
          3750 <= sic_code <= 3751 or
          3792 <= sic_code <= 3792 or
          3900 <= sic_code <= 3939 or
          3990 <= sic_code <= 3999):
        return "Durbl"

    # 3 Manuf  Manufacturing -- Machinery, Trucks, Planes, Chemicals, Off Furn, Paper, Com Printing
    elif (2520 <= sic_code <= 2589 or
          2600 <= sic_code <= 2699 or
          2750 <= sic_code <= 2769 or
          2800 <= sic_code <= 2829 or
          2840 <= sic_code <= 2899 or
          3000 <= sic_code <= 3099 or
          3200 <= sic_code <= 3569 or
          3580 <= sic_code <= 3621 or
          3623 <= sic_code <= 3629 or
          3700 <= sic_code <= 3709 or
          3712 <= sic_code <= 3713 or
          3715 <= sic_code <= 3715 or
          3717 <= sic_code <= 3749 or
          3752 <= sic_code <= 3791 or
          3793 <= sic_code <= 3799 or
          3860 <= sic_code <= 3899):
        return "Manuf"

    # 4 Enrgy  Oil, Gas, and Coal Extraction and Products
    elif (1200 <= sic_code <= 1399 or
          2900 <= sic_code <= 2999):
        return "Enrgy"

    # 5 HiTec  Business Equipment -- Computers, Software, and Electronic Equipment
    elif (3570 <= sic_code <= 3579 or
          3622 <= sic_code <= 3622 or # Industrial controls
          3660 <= sic_code <= 3692 or
          3694 <= sic_code <= 3699 or
          3810 <= sic_code <= 3839 or
          7370 <= sic_code <= 7372 or # Services - computer programming and data processing
          7373 <= sic_code <= 7373 or # Computer integrated systems design
          7374 <= sic_code <= 7374 or # Services - computer processing, data preparation and processing
          7375 <= sic_code <= 7375 or # Services - information retrieval services
          7376 <= sic_code <= 7376 or # Services - computer facilities management service
          7377 <= sic_code <= 7377 or # Services - computer rental and leasing
          7378 <= sic_code <= 7378 or # Services - computer maintenance and repair
          7379 <= sic_code <= 7379 or # Services - computer related services
          7391 <= sic_code <= 7391 or # Services - R&D labs
          8730 <= sic_code <= 8734): # Services - research, development, testing labs
        return "HiTec"
    
    # 6 Telcm  Telephone and Television Transmission
    elif 4800 <= sic_code <= 4899:
        return "Telcm"
    
    # 7 Shops  Wholesale, Retail, and Some Services (Laundries, Repair Shops)
    elif (5000 <= sic_code <= 5999 or
          7200 <= sic_code <= 7299 or
          7600 <= sic_code <= 7699):
        return "Shops"
    
    # 8 Hlth   Healthcare, Medical Equipment, and Drugs
    elif (2830 <= sic_code <= 2839 or
          3693 <= sic_code <= 3693 or
          3840 <= sic_code <= 3859 or
          8000 <= sic_code <= 8099):
        return "Hlth"
    
    # 9 Utils  Utilities
    elif 4900 <= sic_code <= 4949:
        return "Utils"
    
    # 10 Other  Other -- Mines, Constr, BldMt, Trans, Hotels, Bus Serv, Entertainment, Finance
    else:
        return "Other"


def sic_to_industry_twelve(sic_code: int) -> str:
    """
    Converts a SIC code into the Fama-French 12 industry classification.

    Args:
        sic_code (int): The SIC code to convert.

    Returns:
        str: The Fama-French 12 industry classification.
    """

    # 1 NoDur  Consumer Nondurables -- Food, Tobacco, Textiles, Apparel, Leather, Toys
    if (100 <= sic_code <= 999 or
        2000 <= sic_code <= 2399 or
        2700 <= sic_code <= 2749 or
        2770 <= sic_code <= 2799 or
        3100 <= sic_code <= 3199 or
        3940 <= sic_code <= 3989):
        return "NoDur"
    
    # 2 Durbl  Consumer Durables -- Cars, TVs, Furniture, Household Appliances
    elif (2500 <= sic_code <= 2519 or
          2590 <= sic_code <= 2599 or
          3630 <= sic_code <= 3659 or
          3710 <= sic_code <= 3711 or
          3714 <= sic_code <= 3714 or
          3716 <= sic_code <= 3716 or
          3750 <= sic_code <= 3751 or
          3792 <= sic_code <= 3792 or
          3900 <= sic_code <= 3939 or
          3990 <= sic_code <= 3999):
        return "Durbl"
    
    # 3 Manuf  Manufacturing -- Machinery, Trucks, Planes, Off Furn, Paper, Com Printing
    elif (2520 <= sic_code <= 2589 or
          2600 <= sic_code <= 2699 or
          2750 <= sic_code <= 2769 or
          3000 <= sic_code <= 3099 or
          3200 <= sic_code <= 3569 or
          3580 <= sic_code <= 3629 or
          3700 <= sic_code <= 3709 or
          3712 <= sic_code <= 3713 or
          3715 <= sic_code <= 3715 or
          3717 <= sic_code <= 3749 or
          3752 <= sic_code <= 3791 or
          3793 <= sic_code <= 3799 or
          3830 <= sic_code <= 3839 or
          3860 <= sic_code <= 3899):
        return "Manuf"
    
    # 4 Enrgy  Oil, Gas, and Coal Extraction and Products
    elif (1200 <= sic_code <= 1399 or
          2900 <= sic_code <= 2999):
        return "Enrgy"
    
    # 5 Chems  Chemicals and Allied Products
    elif (2800 <= sic_code <= 2829 or
          2840 <= sic_code <= 2899):
        return "Chems"
    
    # 6 BusEq  Business Equipment -- Computers, Software, and Electronic Equipment
    elif (3570 <= sic_code <= 3579 or
          3660 <= sic_code <= 3692 or
          3694 <= sic_code <= 3699 or
          3810 <= sic_code <= 3829 or
          7370 <= sic_code <= 7379):
        return "BusEq"
    
    # 7 Telcm  Telephone and Television Transmission
    elif 4800 <= sic_code <= 4899:
        return "Telcm"
    
    # 8 Utils  Utilities
    elif 4900 <= sic_code <= 4949:
        return "Utils"
    
    # 9 Shops  Wholesale, Retail, and Some Services (Laundries, Repair Shops)
    elif (5000 <= sic_code <= 5999 or
          7200 <= sic_code <= 7299 or
          7600 <= sic_code <= 7699):
        return "Shops"

    # 10 Hlth   Healthcare, Medical Equipment, and Drugs
    elif (2830 <= sic_code <= 2839 or
          3693 <= sic_code <= 3693 or
          3840 <= sic_code <= 3859 or
          8000 <= sic_code <= 8099):
        return "Hlth"
    
    # 11 Money  Finance
    elif 6000 <= sic_code <= 6999:
        return "Money"
    
    # 12 Other  Other -- Mines, Constr, BldMt, Trans, Hotels, Bus Serv, Entertainment
    else:
        return "Other"
    

def sic_to_industry_seventeen(sic_code: int) -> str:
    """
    Converts a SIC code into the Fama-French 17 industry classification.

    Args:
        sic_code (int): The SIC code to convert.

    Returns:
        str: The Fama-French 17 industry classification.
    """

    # 1 Food   Food
    if (100 <= sic_code <= 199 or # Agricultural production - crops
        200 <= sic_code <= 299 or # Agricultural production - livestock
        700 <= sic_code <= 799 or # Agricultural services
        900 <= sic_code <= 999 or # Fishing, hunting & trapping
        2000 <= sic_code <= 2009 or # Food and kindred products
        2010 <= sic_code <= 2019 or # Meat products
        2020 <= sic_code <= 2029 or # Dairy products
        2030 <= sic_code <= 2039 or # Canned & preserved fruits & vegetables
        2040 <= sic_code <= 2046 or # Flour and other grain mill products
        2047 <= sic_code <= 2047 or # Dog and cat food
        2048 <= sic_code <= 2048 or # Prepared feeds for animals
        2050 <= sic_code <= 2059 or # Bakery products
        2060 <= sic_code <= 2063 or # Sugar and confectionery products
        2064 <= sic_code <= 2068 or # Candy and other confectionery
        2070 <= sic_code <= 2079 or # Fats and oils
        2080 <= sic_code <= 2080 or # Beverages
        2082 <= sic_code <= 2082 or # Malt beverages
        2083 <= sic_code <= 2083 or # Malt
        2084 <= sic_code <= 2084 or # Wine
        2085 <= sic_code <= 2085 or # Distilled and blended liquors
        2086 <= sic_code <= 2086 or # Bottled-canned soft drinks
        2087 <= sic_code <= 2087 or # Flavoring syrup
        2090 <= sic_code <= 2092 or # Misc food preparations and kindred products
        2095 <= sic_code <= 2095 or # Roasted coffee
        2096 <= sic_code <= 2096 or # Potato chips
        2097 <= sic_code <= 2097 or # Manufactured ice
        2098 <= sic_code <= 2099 or # Misc food preparations
        5140 <= sic_code <= 5149 or # Wholesale - groceries & related products
        5150 <= sic_code <= 5159 or # Wholesale - farm product raw materials
        5180 <= sic_code <= 5182 or # Wholesale - beer, wine & distilled alcoholic beverages
        5191 <= sic_code <= 5191): # Wholesale - farm supplies
        return "Food"
    
    # 2 Mines  Mining and Minerals
    elif (1000 <= sic_code <= 1009 or # Metal mining
          1010 <= sic_code <= 1019 or # Iron ores
          1020 <= sic_code <= 1029 or # Copper ores
          1030 <= sic_code <= 1039 or # Lead and zinc ores
          1040 <= sic_code <= 1049 or # Gold & silver ores
          1060 <= sic_code <= 1069 or # Ferroalloy ores
          1080 <= sic_code <= 1089 or # Metal mining services
          1090 <= sic_code <= 1099 or # Misc metal ores
          1200 <= sic_code <= 1299 or # Bituminous coal
          1400 <= sic_code <= 1499 or # Mining and quarrying nonmetallic minerals
          5050 <= sic_code <= 5052): # Wholesale - metals and minerals, except petroleum
        return "Mines"

    # 3 Oil    Oil and Petroleum Products
    elif (1300 <= sic_code <= 1300 or # Oil and gas extraction
          1310 <= sic_code <= 1319 or # Crude petroleum & natural gas
          1320 <= sic_code <= 1329 or # Natural gas liquids
          1380 <= sic_code <= 1380 or # Oil and gas field services
          1381 <= sic_code <= 1381 or # Drilling oil & gas wells
          1382 <= sic_code <= 1382 or # Oil & gas field exploration services
          1389 <= sic_code <= 1389 or # Misc oil & gas field services
          2900 <= sic_code <= 2912 or # Petroleum refining
          5170 <= sic_code <= 5172): # Wholesale - petroleum and petroleum products
        return "Oil"

    # 4 Clths  Textiles, Apparel & Footwear
    elif (2200 <= sic_code <= 2269 or # Textile mill products
          2270 <= sic_code <= 2279 or # Floor covering mills
          2280 <= sic_code <= 2284 or # Yarn and thread mills
          2290 <= sic_code <= 2295 or # Misc textile goods
          2296 <= sic_code <= 2296 or # Tire cord and fabric
          2297 <= sic_code <= 2297 or # Non-woven fabrics
          2298 <= sic_code <= 2298 or # Cordage and twine
          2299 <= sic_code <= 2299 or # Misc textile products
          2300 <= sic_code <= 2390 or # Apparel and other finished products
          2391 <= sic_code <= 2392 or # Curtains, home furnishings
          2393 <= sic_code <= 2395 or # Textile bags, canvas products
          2396 <= sic_code <= 2396 or # Automotive trimmings, apparel findings & related products
          2397 <= sic_code <= 2399 or # Misc textile products
          3020 <= sic_code <= 3021 or # Rubber and plastics footwear
          3100 <= sic_code <= 3111 or # Leather tanning and finishing
          3130 <= sic_code <= 3131 or # Boot & shoe cut stock & findings
          3140 <= sic_code <= 3149 or # Footwear, except rubber
          3150 <= sic_code <= 3151 or # Leather gloves and mittens
          3963 <= sic_code <= 3965 or # Fasteners, buttons, needles, pins
          5130 <= sic_code <= 5139): # Wholesale - apparel, piece goods & notions
        return "Clths"

    # 5 Durbl  Consumer Durables
    elif (2510 <= sic_code <= 2519 or # Household furniture
          2590 <= sic_code <= 2599 or # Misc furniture and fixtures
          3060 <= sic_code <= 3069 or # Fabricated rubber products
          3070 <= sic_code <= 3079 or # Misc rubber products (?)
          3080 <= sic_code <= 3089 or # Misc plastic products
          3090 <= sic_code <= 3099 or # Misc rubber and plastic products (?)
          3630 <= sic_code <= 3639 or # Household appliances
          3650 <= sic_code <= 3651 or # Household audio visual equipment
          3652 <= sic_code <= 3652 or # Phonograph records
          3860 <= sic_code <= 3861 or # Photographic equipment  (Kodak etc, but also Xerox)
          3870 <= sic_code <= 3873 or # Watches, clocks and parts
          3910 <= sic_code <= 3911 or # Jewelry, precious metals
          3914 <= sic_code <= 3914 or # Silverware
          3915 <= sic_code <= 3915 or # Jewelers' findings and materials
          3930 <= sic_code <= 3931 or # Musical instruments
          3940 <= sic_code <= 3949 or # Toys
          3960 <= sic_code <= 3962 or # Costume jewelry and novelties
          5020 <= sic_code <= 5023 or # Wholesale - furniture and home furnishings
          5064 <= sic_code <= 5064 or # Wholesale - electrical appliance, TV and radio sets
          5094 <= sic_code <= 5094 or # Wholesale - jewelry, watches, precious stones & metals
          5099 <= sic_code <= 5099): # Wholesale - durable goods
        return "Durbl"

    # 6 Chems  Chemicals
    elif (2800 <= sic_code <= 2809 or # Chemicals and allied products
          2810 <= sic_code <= 2819 or # Industrial inorganic chemicals
          2820 <= sic_code <= 2829 or # Plastic material & synthetic resin/rubber
          2860 <= sic_code <= 2869 or # Industrial organic chemicals
          2870 <= sic_code <= 2879 or # Agriculture chemicals
          2890 <= sic_code <= 2899 or # Misc chemical products
          5160 <= sic_code <= 5169): # Wholesale - chemicals & allied products
        return "Chems"
    
    # 7 Cnsum  Drugs, Soap, Perfumes, Tobacco
    elif (2100 <= sic_code <= 2199 or # Tobacco products
          2830 <= sic_code <= 2830 or # Drugs
          2831 <= sic_code <= 2831 or # Biological products
          2833 <= sic_code <= 2833 or # Medicinal chemicals
          2834 <= sic_code <= 2834 or # Pharmaceutical preparations
          2840 <= sic_code <= 2843 or # Soap & other detergents
          2844 <= sic_code <= 2844 or # Perfumes, cosmetics and other toilet preparations
          5120 <= sic_code <= 5122 or # Wholesale - drugs & drug proprietaries
          5194 <= sic_code <= 5194): # Wholesale - tobacco and tobacco products
        return "Cnsum"
    
    # 8 Cnstr  Construction and Construction Materials
    elif (800 <= sic_code <= 899 or # Forestry
          1500 <= sic_code <= 1511 or # Build construction - general contractors
          1520 <= sic_code <= 1529 or # General building contractors - residential
          1530 <= sic_code <= 1539 or # Operative builders
          1540 <= sic_code <= 1549 or # General building contractors - non-residential
          1600 <= sic_code <= 1699 or # Heavy construction - not building contractors
          1700 <= sic_code <= 1799 or # Construction - special contractors
          2400 <= sic_code <= 2439 or # Lumber and wood products
          2440 <= sic_code <= 2449 or # Wood containers
          2450 <= sic_code <= 2459 or # Wood buildings & mobile homes
          2490 <= sic_code <= 2499 or # Misc wood products
          2850 <= sic_code <= 2859 or # Paints
          2950 <= sic_code <= 2952 or # Paving & roofing materials
          3200 <= sic_code <= 3200 or # Stone, clay, glass, concrete, etc
          3210 <= sic_code <= 3211 or # Flat glass
          3240 <= sic_code <= 3241 or # Cement, hydraulic
          3250 <= sic_code <= 3259 or # Structural clay products
          3261 <= sic_code <= 3261 or # Vitreous china plumbing fixtures
          3264 <= sic_code <= 3264 or # Porcelain electrical supplies
          3270 <= sic_code <= 3275 or # Concrete, gypsum & plaster products
          3280 <= sic_code <= 3281 or # Cut stone and stone products
          3290 <= sic_code <= 3293 or # Abrasive and asbestos products
          3420 <= sic_code <= 3429 or # Cutlery, hand tools and general hardware
          3430 <= sic_code <= 3433 or # Heating equipment & plumbing fixtures
          3440 <= sic_code <= 3441 or # Fabricated structural metal products
          3442 <= sic_code <= 3442 or # Metal doors, frames
          3446 <= sic_code <= 3446 or # Architectural or ornamental metal work
          3448 <= sic_code <= 3448 or # Prefabricated metal buildings and components
          3449 <= sic_code <= 3449 or # Misc structural metal work
          3450 <= sic_code <= 3451 or # Screw machine products
          3452 <= sic_code <= 3452 or # Bolts, nuts, screws, rivets and washers
          5030 <= sic_code <= 5039 or # Wholesale - lumber and construction materials
          5070 <= sic_code <= 5078 or # Wholesale - hardware, plumbing & heating equipment
          5198 <= sic_code <= 5198 or # Wholesale - Paints, varnishes, and supplies
          5210 <= sic_code <= 5211 or # Retail - lumber & other building materials
          5230 <= sic_code <= 5231 or # Retail - paint, glass & wallpaper stores
          5250 <= sic_code <= 5251): # Retail - hardware stores
        return "Cnstr"

    # 9 Steel  Steel Works Etc
    elif (3300 <= sic_code <= 3300 or # Primary metal industries
          3310 <= sic_code <= 3317 or # Blast furnaces & steel works
          3320 <= sic_code <= 3325 or # Iron & steel foundries
          3330 <= sic_code <= 3339 or # Primary smelting & refining of nonferrous metals
          3340 <= sic_code <= 3341 or # Secondary smelting & refining of nonferrous metals
          3350 <= sic_code <= 3357 or # Rolling, drawing & extruding of nonferrous metals
          3360 <= sic_code <= 3369 or # Nonferrous foundries and casting
          3390 <= sic_code <= 3399): # Misc primary metal products
        return "Steel"

    # 10 FabPr  Fabricated Products
    elif (3410 <= sic_code <= 3412 or # Metal cans and shipping containers
          3443 <= sic_code <= 3443 or # Fabricated plate work
          3444 <= sic_code <= 3444 or # Sheet metal work
          3460 <= sic_code <= 3469 or # Metal forgings and stampings
          3470 <= sic_code <= 3479 or # Coating, engraving and allied services
          3480 <= sic_code <= 3489 or # Ordnance & accessories
          3490 <= sic_code <= 3499): # Misc fabricated metal products
        return "FabPr"
    
    # 11 Machn  Machinery and Business Equipment
    elif (3510 <= sic_code <= 3519 or # Engines & turbines
          3520 <= sic_code <= 3529 or # Farm and garden machinery and equipment
          3530 <= sic_code <= 3530 or # Construction, mining & material handling machinery & equipment
          3531 <= sic_code <= 3531 or # Construction machinery & equipment
          3532 <= sic_code <= 3532 or # Mining machinery & equipment, except oil field
          3533 <= sic_code <= 3533 or # Oil & gas field machinery & equipment
          3534 <= sic_code <= 3534 or # Elevators & moving stairways
          3535 <= sic_code <= 3535 or # Conveyors & conveying equipment
          3536 <= sic_code <= 3536 or # Cranes, hoists and monorail systems
          3540 <= sic_code <= 3549 or # Metalworking machinery & equipment
          3550 <= sic_code <= 3559 or # Special industry machinery
          3560 <= sic_code <= 3569 or # General industrial machinery & equipment
          3570 <= sic_code <= 3579 or # Computer & office equipment
          3580 <= sic_code <= 3580 or # Refrigeration & service industry machinery
          3581 <= sic_code <= 3581 or # Automatic vending machines
          3582 <= sic_code <= 3582 or # Commercial laundry and dry-cleaning machines
          3585 <= sic_code <= 3585 or # Air conditioning, warm air heating and refrigeration equipment
          3586 <= sic_code <= 3586 or # Measuring and dispensing pumps
          3589 <= sic_code <= 3589 or # Service industry machinery
          3590 <= sic_code <= 3599 or # Misc industrial and commercial equipment and machinery
          3600 <= sic_code <= 3600 or # Electronic & other electrical equipment
          3610 <= sic_code <= 3613 or # Electric transmission and distribution equipment
          3620 <= sic_code <= 3621 or # Electrical industrial apparatus
          3622 <= sic_code <= 3622 or # Industrial controls
          3623 <= sic_code <= 3629 or # Electrical industrial apparatus
          3670 <= sic_code <= 3679 or # Electronic components & accessories
          3680 <= sic_code <= 3680 or # Computers
          3681 <= sic_code <= 3681 or # Computers - mini
          3682 <= sic_code <= 3682 or # Computers - mainframe
          3683 <= sic_code <= 3683 or # Computers - terminals
          3684 <= sic_code <= 3684 or # Computers - disk & tape drives
          3685 <= sic_code <= 3685 or # Computers - optical scanners
          3686 <= sic_code <= 3686 or # Computers - graphics
          3687 <= sic_code <= 3687 or # Computers - office automation systems
          3688 <= sic_code <= 3688 or # Computers - peripherals
          3689 <= sic_code <= 3689 or # Computers - equipment
          3690 <= sic_code <= 3690 or # Misc electrical machinery and equipment
          3691 <= sic_code <= 3692 or # Storage batteries
          3693 <= sic_code <= 3693 or # X-ray, electromedical app
          3694 <= sic_code <= 3694 or # Electrical equipment for internal combustion engines
          3695 <= sic_code <= 3695 or # Magnetic and optical recording media
          3699 <= sic_code <= 3699 or # Misc electrical machinery, equipment and supplies
          3810 <= sic_code <= 3810 or # Search, detection, navigation, guidance
          3811 <= sic_code <= 3811 or # Engr lab and research equipment
          3812 <= sic_code <= 3812 or # Search, detection, navigation, guidance
          3820 <= sic_code <= 3820 or # Measuring and controlling equipment
          3821 <= sic_code <= 3821 or # Laboratory apparatus and furniture
          3822 <= sic_code <= 3822 or # Automatic controls for regulating residential & commercial environments & appliances
          3823 <= sic_code <= 3823 or # Industrial measurement instruments & related products
          3824 <= sic_code <= 3824 or # Totalizing fluid meters & counting devices
          3825 <= sic_code <= 3825 or # Instruments for measuring & testing of electricity & electrical instruments
          3826 <= sic_code <= 3826 or # Lab analytical instruments
          3827 <= sic_code <= 3827 or # Optical instruments and lenses
          3829 <= sic_code <= 3829 or # Misc measuring and controlling devices
          3830 <= sic_code <= 3839 or # Optical instruments and lenses
          3950 <= sic_code <= 3955 or # Pens, pencils & other artists' supplies
          5060 <= sic_code <= 5060 or # Wholesale - electrical goods
          5063 <= sic_code <= 5063 or # Wholesale - electrical apparatus and equipment
          5065 <= sic_code <= 5065 or # Wholesale - electronic parts & equipment
          5080 <= sic_code <= 5080 or # Wholesale - machinery, equipment & supplies
          5081 <= sic_code <= 5081): # Wholesale - machinery & equipment (?)
        return "Machn"
    
    # 12 Cars   Automobiles
    elif (3710 <= sic_code <= 3710 or # Motor vehicles and motor vehicle equipment
          3711 <= sic_code <= 3711 or # Motor vehicles & passenger car bodies
          3714 <= sic_code <= 3714 or # Motor vehicle parts & accessories
          3716 <= sic_code <= 3716 or # Motor homes
          3750 <= sic_code <= 3751 or # Motorcycles, bicycles and parts
          3792 <= sic_code <= 3792 or # Travel trailers and campers
          5010 <= sic_code <= 5015 or # Wholesale - automotive vehicles & automotive parts & supplies
          5510 <= sic_code <= 5521 or # Retail - automotive dealers
          5530 <= sic_code <= 5531 or # Retail - automotive and home supply stores
          5560 <= sic_code <= 5561 or # Retail - recreation vehicle dealers
          5570 <= sic_code <= 5571 or # Retail - motorcycle dealers
          5590 <= sic_code <= 5599): # Retail - automotive dealers
        return "Cars"

    # 13 Trans  Transportation
    elif (3713 <= sic_code <= 3713 or # Truck & bus bodies
          3715 <= sic_code <= 3715 or # Truck trailers
          3720 <= sic_code <= 3720 or # Aircraft & parts
          3721 <= sic_code <= 3721 or # Aircraft
          3724 <= sic_code <= 3724 or # Aircraft engines & engine parts
          3725 <= sic_code <= 3725 or # Aircraft parts
          3728 <= sic_code <= 3728 or # Misc aircraft parts & auxiliary equipment
          3730 <= sic_code <= 3731 or # Ship building and repairing
          3732 <= sic_code <= 3732 or # Boat building and repairing
          3740 <= sic_code <= 3743 or # Railroad Equipment
          3760 <= sic_code <= 3769 or # Guided missiles and space vehicles
          3790 <= sic_code <= 3790 or # Misc transmission equipment
          3795 <= sic_code <= 3795 or # Tanks and tank components
          3799 <= sic_code <= 3799 or # Misc transmission equipment
          4000 <= sic_code <= 4013 or # Railroads, line-haul operating
          4100 <= sic_code <= 4100 or # Local & suburban transit & interurban highway passenger transportation
          4110 <= sic_code <= 4119 or # Local & suburban passenger transportation
          4120 <= sic_code <= 4121 or # Taxicabs
          4130 <= sic_code <= 4131 or # Intercity & rural bus transportation (Greyhound)
          4140 <= sic_code <= 4142 or # Bus charter service
          4150 <= sic_code <= 4151 or # School buses
          4170 <= sic_code <= 4173 or # Motor vehicle terminals & service facilities
          4190 <= sic_code <= 4199 or # Misc transit and passenger transportation
          4200 <= sic_code <= 4200 or # Trucking & warehousing
          4210 <= sic_code <= 4219 or # Trucking & courier services, except air
          4220 <= sic_code <= 4229 or # Public warehousing and storage
          4230 <= sic_code <= 4231 or # Terminal & joint terminal maintenance
          4400 <= sic_code <= 4499 or # Water transport
          4500 <= sic_code <= 4599 or # Air transportation
          4600 <= sic_code <= 4699 or # Pipelines, except natural gas
          4700 <= sic_code <= 4700 or # Transportation services
          4710 <= sic_code <= 4712 or # Freight forwarding
          4720 <= sic_code <= 4729 or # Arrangement of passenger transportation
          4730 <= sic_code <= 4739 or # Arrangement of transportation of freight and cargo
          4740 <= sic_code <= 4742 or # Rental of railroad cars
          4780 <= sic_code <= 4780 or # Misc services incidental to transportation
          4783 <= sic_code <= 4783 or # Packing and crating
          4785 <= sic_code <= 4785 or # Motor vehicle inspection
          4789 <= sic_code <= 4789): # Misc transportation services
        return "Trans"
    
    # 14 Utils  Utilities
    elif (4900 <= sic_code <= 4900 or # Electric, gas & sanitary services
          4910 <= sic_code <= 4911 or # Electric services
          4920 <= sic_code <= 4922 or # Natural gas transmission
          4923 <= sic_code <= 4923 or # Natural gas transmission & distribution
          4924 <= sic_code <= 4925 or # Natural gas distribution
          4930 <= sic_code <= 4931 or # Electric and other services combined
          4932 <= sic_code <= 4932 or # Gas and other services combined
          4939 <= sic_code <= 4939 or # Misc combination utilities
          4940 <= sic_code <= 4942): # Water supply
        return "Utils"

    # 15 Rtail  Retail Stores
    elif (5260 <= sic_code <= 5261 or # Retail - nurseries, lawn & garden supply stores
          5270 <= sic_code <= 5271 or # Retail - mobile home dealers
          5300 <= sic_code <= 5300 or # Retail - general merchandise stores
          5310 <= sic_code <= 5311 or # Retail - department stores
          5320 <= sic_code <= 5320 or # Retail - general merchandise stores (?)
          5330 <= sic_code <= 5331 or # Retail - variety stores
          5334 <= sic_code <= 5334 or # Retail - catalog showroom
          5390 <= sic_code <= 5399 or # Retail - Misc general merchandise stores
          5400 <= sic_code <= 5400 or # Retail - food stores
          5410 <= sic_code <= 5411 or # Retail - grocery stores
          5412 <= sic_code <= 5412 or # Retail - convenience stores
          5420 <= sic_code <= 5421 or # Retail - meat & fish markets
          5430 <= sic_code <= 5431 or # Retail - fruit and vegetable markets
          5440 <= sic_code <= 5441 or # Retail - candy, nut & confectionary stores
          5450 <= sic_code <= 5451 or # Retail - dairy products stores
          5460 <= sic_code <= 5461 or # Retail - bakeries
          5490 <= sic_code <= 5499 or # Retail - Misc food stores
          5540 <= sic_code <= 5541 or # Retail - gasoline service stations
          5550 <= sic_code <= 5551 or # Retail - boat dealers
          5600 <= sic_code <= 5699 or # Retail - apparel & accessory stores
          5700 <= sic_code <= 5700 or # Retail - home furniture and equipment stores
          5710 <= sic_code <= 5719 or # Retail - home furnishings stores
          5720 <= sic_code <= 5722 or # Retail - household appliance stores
          5730 <= sic_code <= 5733 or # Retail - radio, TV and consumer electronic stores
          5734 <= sic_code <= 5734 or # Retail - computer and computer software stores
          5735 <= sic_code <= 5735 or # Retail - record and tape stores
          5736 <= sic_code <= 5736 or # Retail - musical instrument stores
          5750 <= sic_code <= 5750 or # Retail - (?)
          5800 <= sic_code <= 5813 or # Retail - eating places
          5890 <= sic_code <= 5890 or # Eating and drinking places
          5900 <= sic_code <= 5900 or # Retail - Misc
          5910 <= sic_code <= 5912 or # Retail - drug & proprietary stores
          5920 <= sic_code <= 5921 or # Retail - liquor stores
          5930 <= sic_code <= 5932 or # Retail - used merchandise stores
          5940 <= sic_code <= 5940 or # Retail - Misc
          5941 <= sic_code <= 5941 or # Retail - sporting goods stores & bike shops
          5942 <= sic_code <= 5942 or # Retail - book stores
          5943 <= sic_code <= 5943 or # Retail - stationery stores
          5944 <= sic_code <= 5944 or # Retail - jewelry stores
          5945 <= sic_code <= 5945 or # Retail - hobby, toy and game shops
          5946 <= sic_code <= 5946 or # Retail - camera and photographic supply stores
          5947 <= sic_code <= 5947 or # Retail - gift, novelty & souvenir shops
          5948 <= sic_code <= 5948 or # Retail - luggage & leather goods stores
          5949 <= sic_code <= 5949 or # Retail - sewing & needlework stores
          5960 <= sic_code <= 5963 or # Retail - non-store retailers (catalogs, etc)
          5980 <= sic_code <= 5989 or # Retail - fuel dealers & ice stores (Penn Central Co)
          5990 <= sic_code <= 5990 or # Retail - Misc retail stores
          5992 <= sic_code <= 5992 or # Retail - florists
          5993 <= sic_code <= 5993 or # Retail - tobacco stores and stands
          5994 <= sic_code <= 5994 or # Retail - newsdealers and news stands
          5995 <= sic_code <= 5995 or # Retail - optical goods stores
          5999 <= sic_code <= 5999): # Misc retail stores
        return "Rtail"

    # 16 Finan  Banks, Insurance Companies, and Other Financials
    elif (6010 <= sic_code <= 6019 or # Federal reserve banks
          6020 <= sic_code <= 6020 or # Commercial banks
          6021 <= sic_code <= 6021 or # National commercial banks
          6022 <= sic_code <= 6022 or # State commercial banks - Fed Res System
          6023 <= sic_code <= 6023 or # State commercial banks - not Fed Res System
          6025 <= sic_code <= 6025 or # National commercial banks - Fed Res System
          6026 <= sic_code <= 6026 or # National commercial banks - not Fed Res System 
          6028 <= sic_code <= 6029 or # Misc commercial banks
          6030 <= sic_code <= 6036 or # Savings institutions
          6040 <= sic_code <= 6049 or # Trust companies, non-deposit
          6050 <= sic_code <= 6059 or # Functions closely related to banking
          6060 <= sic_code <= 6062 or # Credit unions
          6080 <= sic_code <= 6082 or # Foreign banks
          6090 <= sic_code <= 6099 or # Functions related to depository banking
          6100 <= sic_code <= 6100 or # Non-depository credit institutions
          6110 <= sic_code <= 6111 or # Federal credit agencies
          6112 <= sic_code <= 6112 or # FNMA
          6120 <= sic_code <= 6129 or # S&Ls 
          6140 <= sic_code <= 6149 or # Personal credit institutions (Beneficial)
          6150 <= sic_code <= 6159 or # Business credit institutions
          6160 <= sic_code <= 6163 or # Mortgage bankers
          6172 <= sic_code <= 6172 or # Finance lessors
          6199 <= sic_code <= 6199 or # Financial services
          6200 <= sic_code <= 6299 or # Security and commodity brokers, dealers, exchanges & services
          6300 <= sic_code <= 6300 or # Insurance
          6310 <= sic_code <= 6312 or # Life insurance
          6320 <= sic_code <= 6324 or # Accident and health insurance
          6330 <= sic_code <= 6331 or # Fire, marine & casualty insurance
          6350 <= sic_code <= 6351 or # Surety insurance
          6360 <= sic_code <= 6361 or # Title insurance
          6370 <= sic_code <= 6371 or # Pension, health & welfare funds
          6390 <= sic_code <= 6399 or # Misc insurance carriers
          6400 <= sic_code <= 6411 or # Insurance agents, brokers & service
          6500 <= sic_code <= 6500 or # Real estate
          6510 <= sic_code <= 6510 or # Real estate operators and lessors
          6512 <= sic_code <= 6512 or # Operators - non-resident buildings
          6513 <= sic_code <= 6513 or # Operators - apartment buildings
          6514 <= sic_code <= 6514 or # Operators - other than apartment
          6515 <= sic_code <= 6515 or # Operators - residential mobile home
          6517 <= sic_code <= 6519 or # Lessors of railroad & real property
          6530 <= sic_code <= 6531 or # Real estate agents and managers
          6532 <= sic_code <= 6532 or # Real estate dealers
          6540 <= sic_code <= 6541 or # Title abstract offices
          6550 <= sic_code <= 6553 or # Land subdividers & developers
          6611 <= sic_code <= 6611 or # Combined real estate, insurance, etc
          6700 <= sic_code <= 6700 or # Holding & other investment offices
          6710 <= sic_code <= 6719 or # Holding offices
          6720 <= sic_code <= 6722 or # Management investment offices, open-end
          6723 <= sic_code <= 6723 or # Management investment offices, closed-end
          6724 <= sic_code <= 6724 or # Unit investment trusts
          6725 <= sic_code <= 6725 or # Face-amount certificate offices
          6726 <= sic_code <= 6726 or # Unit investment trusts, closed-end
          6730 <= sic_code <= 6733 or # Trusts
          6790 <= sic_code <= 6790 or # Misc investing
          6792 <= sic_code <= 6792 or # Oil royalty traders
          6794 <= sic_code <= 6794 or # Patent owners & lessors
          6795 <= sic_code <= 6795 or # Mineral royalty traders
          6798 <= sic_code <= 6798 or # REIT
          6799 <= sic_code <= 6799): # Investors, NEC
        return "Finan"
    
    # 17 Other  Other
    elif (2520 <= sic_code <= 2549 or # Office furniture and fixtures
          2600 <= sic_code <= 2639 or # Paper and allied products
          2640 <= sic_code <= 2659 or # Paperboard containers, boxes, drums, tubs
          2661 <= sic_code <= 2661 or # Building paper and board mills
          2670 <= sic_code <= 2699 or # Paper and allied products
          2700 <= sic_code <= 2709 or # Printing publishing and allied
          2710 <= sic_code <= 2719 or # Newspapers: publishing-printing
          2720 <= sic_code <= 2729 or # Periodicals: publishing-printing
          2730 <= sic_code <= 2739 or # Books: publishing-printing
          2740 <= sic_code <= 2749 or # Misc publishing
          2750 <= sic_code <= 2759 or # Commercial printing
          2760 <= sic_code <= 2761 or # Manifold business forms
          2770 <= sic_code <= 2771 or # Greeting card
          2780 <= sic_code <= 2789 or # Bookbinding
          2790 <= sic_code <= 2799 or # Service industries for the print trade
          2835 <= sic_code <= 2835 or # In vitro, in vivo diagnostic substances
          2836 <= sic_code <= 2836 or # Biological products, except diagnostic substances
          2990 <= sic_code <= 2999 or # Misc products of petroleum & coal
          3000 <= sic_code <= 3000 or # Rubber & misc plastic products
          3010 <= sic_code <= 3011 or # Tires and inner tubes
          3041 <= sic_code <= 3041 or # Rubber & plastic hose & belting
          3050 <= sic_code <= 3053 or # Gaskets, hoses, etc
          3160 <= sic_code <= 3161 or # Luggage
          3170 <= sic_code <= 3171 or # Handbags and purses
          3172 <= sic_code <= 3172 or # Personal leather goods, except handbags and purses
          3190 <= sic_code <= 3199 or # Leather goods
          3220 <= sic_code <= 3221 or # Glass containers
          3229 <= sic_code <= 3229 or # Pressed and blown glass
          3230 <= sic_code <= 3231 or # Glass products
          3260 <= sic_code <= 3260 or # Pottery and related products
          3262 <= sic_code <= 3263 or # China and earthenware table articles
          3269 <= sic_code <= 3269 or # Pottery products
          3295 <= sic_code <= 3299 or # Misc nonmetallic mineral products
          3537 <= sic_code <= 3537 or # Industrial trucks, tractors, trailers & stackers
          3640 <= sic_code <= 3644 or # Electric lighting & wiring equipment
          3645 <= sic_code <= 3645 or # Residential electric lighting fixtures
          3646 <= sic_code <= 3646 or # Commercial, industrial and institutional electric lighting fixtures
          3647 <= sic_code <= 3647 or # Vehicular lighting equipment
          3648 <= sic_code <= 3649 or # Misc lighting equipment
          3660 <= sic_code <= 3660 or # Communications equipment
          3661 <= sic_code <= 3661 or # Telephone and telegraph apparatus
          3662 <= sic_code <= 3662 or # Communications equipment
          3663 <= sic_code <= 3663 or # Radio & TV broadcasting & communications equipment
          3664 <= sic_code <= 3664 or # Search, navigation, guidance systems
          3665 <= sic_code <= 3665 or # Training equipment & simulators
          3666 <= sic_code <= 3666 or # Alarm & signaling products
          3669 <= sic_code <= 3669 or # Communication equipment
          3840 <= sic_code <= 3849 or # Surgical, medical, and dental instruments and supplies
          3850 <= sic_code <= 3851 or # Ophthalmic goods
          3991 <= sic_code <= 3991 or # Brooms and brushes
          3993 <= sic_code <= 3993 or # Signs & advertising specialties
          3995 <= sic_code <= 3995 or # Burial caskets
          3996 <= sic_code <= 3996 or # Hard surface floor coverings
          4810 <= sic_code <= 4813 or # Telephone communications
          4820 <= sic_code <= 4822 or # Telegraph and other message communication
          4830 <= sic_code <= 4839 or # Radio & TV broadcasters
          4840 <= sic_code <= 4841 or # Cable and other pay TV services
          4890 <= sic_code <= 4890 or # Communication services (Comsat)
          4891 <= sic_code <= 4891 or # Cable TV operators
          4892 <= sic_code <= 4892 or # Telephone interconnect
          4899 <= sic_code <= 4899 or # Misc communication services
          4950 <= sic_code <= 4959 or # Sanitary services
          4960 <= sic_code <= 4961 or # Steam & air conditioning supplies
          4970 <= sic_code <= 4971 or # Irrigation systems
          4991 <= sic_code <= 4991 or # Cogeneration - SM power producer
          5040 <= sic_code <= 5042 or # Wholesale - professional and commercial equipment and supplies
          5043 <= sic_code <= 5043 or # Wholesale - photographic equipment & supplies
          5044 <= sic_code <= 5044 or # Wholesale - office equipment
          5045 <= sic_code <= 5045 or # Wholesale - computers & peripheral equipment & software
          5046 <= sic_code <= 5046 or # Wholesale - commercial equipment
          5047 <= sic_code <= 5047 or # Wholesale - medical, dental & hospital equipment
          5048 <= sic_code <= 5048 or # Wholesale - ophthalmic goods
          5049 <= sic_code <= 5049 or # Wholesale - professional equipment and supplies
          5082 <= sic_code <= 5082 or # Wholesale - construction and mining machinery &equipment
          5083 <= sic_code <= 5083 or # Wholesale - farm and garden machinery & equipment
          5084 <= sic_code <= 5084 or # Wholesale - industrial machinery & equipment
          5085 <= sic_code <= 5085 or # Wholesale - industrial supplies
          5086 <= sic_code <= 5087 or # Wholesale - service establishment machinery & equipment (?)
          5088 <= sic_code <= 5088 or # Wholesale - transportation equipment, except motor vehicles
          5090 <= sic_code <= 5090 or # Wholesale - Misc durable goods
          5091 <= sic_code <= 5092 or # Wholesale - sporting goods & toys
          5093 <= sic_code <= 5093 or # Wholesale - scrap and waste materials
          5100 <= sic_code <= 5100 or # Wholesale - nondurable goods
          5110 <= sic_code <= 5113 or # Wholesale - paper and paper products
          5199 <= sic_code <= 5199 or # Wholesale - nondurable goods
          7000 <= sic_code <= 7000 or # Hotels & other lodging places
          7010 <= sic_code <= 7011 or # Hotels & motels
          7020 <= sic_code <= 7021 or # Rooming and boarding houses
          7030 <= sic_code <= 7033 or # Camps and recreational vehicle parks
          7040 <= sic_code <= 7041 or # Membership hotels and lodging
          7200 <= sic_code <= 7200 or # Services - personal
          7210 <= sic_code <= 7212 or # Services - laundry, cleaning & garment services
          7213 <= sic_code <= 7213 or # Services - linen supply
          7215 <= sic_code <= 7216 or # Services - coin-operated cleaners, dry cleaners
          7217 <= sic_code <= 7217 or # Services - carpet & upholstery cleaning
          7218 <= sic_code <= 7218 or # Services - industrial launderers
          7219 <= sic_code <= 7219 or # Services - Misc laundry & garment services
          7220 <= sic_code <= 7221 or # Services - photographic studios, portrait
          7230 <= sic_code <= 7231 or # Services - beauty shops
          7240 <= sic_code <= 7241 or # Services - barber shops
          7250 <= sic_code <= 7251 or # Services - shoe repair shops & shoeshine parlors
          7260 <= sic_code <= 7269 or # Services - funeral service & crematories
          7290 <= sic_code <= 7290 or # Services – Misc
          7291 <= sic_code <= 7291 or # Services - tax return
          7299 <= sic_code <= 7299 or # Services - Misc
          7300 <= sic_code <= 7300 or # Services - business services
          7310 <= sic_code <= 7319 or # Services - advertising
          7320 <= sic_code <= 7323 or # Services - consumer credit reporting agencies, collection services
          7330 <= sic_code <= 7338 or # Services - mailing, reproduction, commercial art & photography
          7340 <= sic_code <= 7342 or # Services - services to dwellings & other buildings
          7349 <= sic_code <= 7349 or # Services - building cleaning & maintenance
          7350 <= sic_code <= 7351 or # Services - Misc equipment rental and leasing
          7352 <= sic_code <= 7352 or # Services - medical equipment rental and leasing
          7353 <= sic_code <= 7353 or # Services - heavy construction equipment rental and leasing
          7359 <= sic_code <= 7359 or # Services - equipment rental and leasing
          7360 <= sic_code <= 7369 or # Services - personnel supply services
          7370 <= sic_code <= 7372 or # Services - computer programming and data processing
          7373 <= sic_code <= 7373 or # Computer integrated systems design
          7374 <= sic_code <= 7374 or # Services - computer processing, data preparation and processing
          7375 <= sic_code <= 7375 or # Services - information retrieval services
          7376 <= sic_code <= 7376 or # Services - computer facilities management service
          7377 <= sic_code <= 7377 or # Services - computer rental and leasing
          7378 <= sic_code <= 7378 or # Services - computer maintenance and repair
          7379 <= sic_code <= 7379 or # Services - computer related services
          7380 <= sic_code <= 7380 or # Services - Misc business services
          7381 <= sic_code <= 7382 or # Services - security
          7383 <= sic_code <= 7383 or # Services - news syndicates
          7384 <= sic_code <= 7384 or # Services - photofinishing labs
          7385 <= sic_code <= 7385 or # Services - telephone interconnect systems
          7389 <= sic_code <= 7390 or # Services - Misc business services
          7391 <= sic_code <= 7391 or # Services - R&D labs
          7392 <= sic_code <= 7392 or # Services - management consulting & P.R.
          7393 <= sic_code <= 7393 or # Services - detective and protective (ADT)
          7394 <= sic_code <= 7394 or # Services - equipment rental & leasing
          7395 <= sic_code <= 7395 or # Services - photofinishing labs (School pictures) services
          7397 <= sic_code <= 7397 or # Services - commercial testing labs
          7399 <= sic_code <= 7399 or # Services - business services
          7500 <= sic_code <= 7500 or # Services - auto repair, services & parking
          7510 <= sic_code <= 7519 or # Services - truck, auto, trailer rental and leasing
          7520 <= sic_code <= 7523 or # Services - automobile parking
          7530 <= sic_code <= 7539 or # Services - automotive repair shops
          7540 <= sic_code <= 7549 or # Services - automotive services, except repair (car washes)
          7600 <= sic_code <= 7600 or # Services - Misc repair services
          7620 <= sic_code <= 7620 or # Services - Electrical repair shops
          7622 <= sic_code <= 7622 or # Services - Radio and TV repair shops
          7623 <= sic_code <= 7623 or # Services - Refrigeration and air conditioning service & repair shops
          7629 <= sic_code <= 7629 or # Services - Electrical & electronic repair shops
          7630 <= sic_code <= 7631 or # Services - Watch, clock and jewelry repair
          7640 <= sic_code <= 7641 or # Services - Reupholster & furniture repair
          7690 <= sic_code <= 7699 or # Services - Misc repair shops & related services
          7800 <= sic_code <= 7829 or # Services - motion picture production and distribution
          7830 <= sic_code <= 7833 or # Services - motion picture theaters
          7840 <= sic_code <= 7841 or # Services - video rental
          7900 <= sic_code <= 7900 or # Services - amusement and recreation
          7910 <= sic_code <= 7911 or # Services - dance studios
          7920 <= sic_code <= 7929 or # Services - bands, entertainers
          7930 <= sic_code <= 7933 or # Services - bowling centers
          7940 <= sic_code <= 7949 or # Services - professional sports
          7980 <= sic_code <= 7980 or # Amusement and recreation services (?)
          7990 <= sic_code <= 7999 or # Services - Misc entertainment
          8000 <= sic_code <= 8099 or # Services - health
          8100 <= sic_code <= 8199 or # Services - legal
          8200 <= sic_code <= 8299 or # Services - educational
          8300 <= sic_code <= 8399 or # Services - social services
          8400 <= sic_code <= 8499 or # Services - museums, art galleries, botanical and zoological gardens
          8600 <= sic_code <= 8699 or # Services - membership organizations
          8700 <= sic_code <= 8700 or # Services - engineering, accounting, research, management
          8710 <= sic_code <= 8713 or # Services - engineering, accounting, surveying
          8720 <= sic_code <= 8721 or # Services - accounting, auditing, bookkeeping
          8730 <= sic_code <= 8734 or # Services - research, development, testing labs
          8740 <= sic_code <= 8748 or # Services - management, public relations, consulting
          8800 <= sic_code <= 8899 or # Services - private households
          8900 <= sic_code <= 8910 or # Services - Misc
          8911 <= sic_code <= 8911 or # Services - Misc engineering & architect
          8920 <= sic_code <= 8999): # Services - Misc
        return "Other"
    
    # Unclassified
    else:
        return "Unclassified"


def sic_to_industry_thirty(sic_code: int) -> str:
    """
    Converts a SIC code into the Fama-French 30 industry classification.

    Args:
        sic_code (int): The SIC code to convert.

    Returns:
        str: The Fama-French 30 industry classification.
    """

    # 1 Food   Food Products
    if (100 <= sic_code <= 199 or # Agricultural production - crops
        2000 <= sic_code <= 2009 or # Food and kindred products
        2010 <= sic_code <= 2019 or # Meat products
        2020 <= sic_code <= 2029 or # Dairy products
        2030 <= sic_code <= 2039 or # Canned & preserved fruits & vegetables
        2040 <= sic_code <= 2046 or # Flour and other grain mill products
        2048 <= sic_code <= 2048 or # Prepared feeds for animals
        2050 <= sic_code <= 2059 or # Bakery products
        2060 <= sic_code <= 2063 or # Sugar and confectionery products
        2064 <= sic_code <= 2068 or # Candy and other confectionery
        2070 <= sic_code <= 2079 or # Fats and oils
        2086 <= sic_code <= 2086 or # Bottled-canned soft drinks
        2087 <= sic_code <= 2087 or # Flavoring syrup
        2090 <= sic_code <= 2092 or # Misc food preparations and kindred products
        2095 <= sic_code <= 2095 or # Roasted coffee
        2096 <= sic_code <= 2096 or # Potato chips
        2097 <= sic_code <= 2097 or # Manufactured ice
        2098 <= sic_code <= 2099): # Misc food preparations
        return "Food"
    
    # 2 Beer   Beer & Liquor
    elif (2080 <= sic_code <= 2080 or # Beverages
          2082 <= sic_code <= 2082 or # Malt beverages
          2083 <= sic_code <= 2083 or # Malt
          2084 <= sic_code <= 2084 or # Wine
          2085 <= sic_code <= 2085): # Distilled and blended liquors
        return "Beer"

    # 3 Smoke  Tobacco Products
    elif (2100 <= sic_code <= 2199): # Tobacco products
        return "Smoke"

    # 4 Games  Recreation
    elif (920 <= sic_code <= 999 or # Fishing, hunting & trapping
          3650 <= sic_code <= 3651 or # Household audio visual equipment
          3652 <= sic_code <= 3652 or # Phonograph records
          3732 <= sic_code <= 3732 or # Boat building and repairing
          3930 <= sic_code <= 3931 or # Musical instruments
          3940 <= sic_code <= 3949 or # Toys
          7800 <= sic_code <= 7829 or # Services - motion picture production and distribution
          7830 <= sic_code <= 7833 or # Services - motion picture theaters
          7840 <= sic_code <= 7841 or # Services - video rental
          7900 <= sic_code <= 7900 or # Services - amusement and recreation
          7910 <= sic_code <= 7911 or # Services - dance studios
          7920 <= sic_code <= 7929 or # Services - bands, entertainers
          7930 <= sic_code <= 7933 or # Services - bowling centers
          7940 <= sic_code <= 7949 or # Services - professional sports
          7980 <= sic_code <= 7980 or # Amusement and recreation services (?)
          7990 <= sic_code <= 7999): # Services - Misc entertainment
        return "Games"
    
    # 5 Books  Printing and Publishing
    elif (2700 <= sic_code <= 2709 or # Printing publishing and allied
          2710 <= sic_code <= 2719 or # Newspapers: publishing-printing
          2720 <= sic_code <= 2729 or # Periodicals: publishing-printing
          2730 <= sic_code <= 2739 or # Books: publishing-printing
          2740 <= sic_code <= 2749 or # Misc publishing
          2750 <= sic_code <= 2759 or # Commercial printing
          2770 <= sic_code <= 2771 or # Greeting card
          2780 <= sic_code <= 2789 or # Bookbinding
          2790 <= sic_code <= 2799 or # Service industries for the print trade
          3993 <= sic_code <= 3993): # Signs & advertising specialties
        return "Books"
    
    # 6 Hshld  Consumer Goods
    elif (2047 <= sic_code <= 2047 or # Dog and cat food
          2391 <= sic_code <= 2392 or # Curtains, home furnishings
          2510 <= sic_code <= 2519 or # Household furniture
          2590 <= sic_code <= 2599 or # Misc furniture and fixtures
          2840 <= sic_code <= 2843 or # Soap & other detergents
          2844 <= sic_code <= 2844 or # Perfumes, cosmetics and other toilet preparations
          3160 <= sic_code <= 3161 or # Luggage
          3170 <= sic_code <= 3171 or # Handbags and purses
          3172 <= sic_code <= 3172 or # Personal leather goods, except handbags and purses
          3190 <= sic_code <= 3199 or # Leather goods
          3229 <= sic_code <= 3229 or # Pressed and blown glass
          3260 <= sic_code <= 3260 or # Pottery and related products
          3262 <= sic_code <= 3263 or # China and earthenware table articles
          3269 <= sic_code <= 3269 or # Pottery products
          3230 <= sic_code <= 3231 or # Glass products
          3630 <= sic_code <= 3639 or # Household appliances
          3750 <= sic_code <= 3751 or # Motorcycles, bicycles and parts  (Harley & Huffy)
          3800 <= sic_code <= 3800 or # Misc instruments, photo goods & watches
          3860 <= sic_code <= 3861 or # Photographic equipment  (Kodak etc, but also Xerox)
          3870 <= sic_code <= 3873 or # Watches, clocks and parts
          3910 <= sic_code <= 3911 or # Jewelry, precious metals
          3914 <= sic_code <= 3914 or # Silverware
          3915 <= sic_code <= 3915 or # Jewelers' findings and materials
          3960 <= sic_code <= 3962 or # Costume jewelry and novelties
          3991 <= sic_code <= 3991 or # Brooms and brushes
          3995 <= sic_code <= 3995): # Burial caskets
        return "Hshld"
    
    # 7 Clths  Apparel
    elif (2300 <= sic_code <= 2390 or # Apparel and other finished products
          3020 <= sic_code <= 3021 or # Rubber and plastics footwear
          3100 <= sic_code <= 3111 or # Leather tanning and finishing
          3130 <= sic_code <= 3131 or # Boot & shoe cut stock & findings
          3140 <= sic_code <= 3149 or # Footwear, except rubber
          3150 <= sic_code <= 3151 or # Leather gloves and mittens
          3963 <= sic_code <= 3965): # Fasteners, buttons, needles, pins
        return "Clths"
    
    # 8 Hlth   Healthcare, Medical Equipment, Pharmaceutical Products
    elif (2830 <= sic_code <= 2830 or # Drugs
          2831 <= sic_code <= 2831 or # Biological products
          2833 <= sic_code <= 2833 or # Medicinal chemicals
          2834 <= sic_code <= 2834 or # Pharmaceutical preparations
          2835 <= sic_code <= 2835 or # In vitro, in vivo diagnostic substances
          2836 <= sic_code <= 2836 or # Biological products, except diagnostic substances
          3693 <= sic_code <= 3693 or # X-ray, electromedical app
          3840 <= sic_code <= 3849 or # Surgical, medical, and dental instruments and supplies
          3850 <= sic_code <= 3851 or # Ophthalmic goods
          8000 <= sic_code <= 8099): # Services - health
        return "Hlth"
        
    # 9 Chems  Chemicals
    elif (2800 <= sic_code <= 2809 or # Chemicals and allied products
          2810 <= sic_code <= 2819 or # Industrial inorganic chemicals
          2820 <= sic_code <= 2829 or # Plastic material & synthetic resin/rubber
          2850 <= sic_code <= 2859 or # Paints
          2860 <= sic_code <= 2869 or # Industrial organic chemicals
          2870 <= sic_code <= 2879 or # Agriculture chemicals
          2890 <= sic_code <= 2899): # Misc chemical products
        return "Chems"
    
    # 10 Txtls  Textiles
    elif (2200 <= sic_code <= 2269 or # Textile mill products
          2270 <= sic_code <= 2279 or # Floor covering mills
          2280 <= sic_code <= 2284 or # Yarn and thread mills
          2290 <= sic_code <= 2295 or # Misc textile goods
          2297 <= sic_code <= 2297 or # Non-woven fabrics
          2298 <= sic_code <= 2298 or # Cordage and twine
          2299 <= sic_code <= 2299 or # Misc textile products
          2393 <= sic_code <= 2395 or # Textile bags, canvas products
          2397 <= sic_code <= 2399): # Misc textile products
        return "Txtls"
    
    # 11 Cnstr  Construction and Construction Materials
    elif (800 <= sic_code <= 899 or # Forestry
          1500 <= sic_code <= 1511 or # Build construction - general contractors
          1520 <= sic_code <= 1529 or # General building contractors - residential
          1530 <= sic_code <= 1539 or # Operative builders
          1540 <= sic_code <= 1549 or # General building contractors - non-residential
          1600 <= sic_code <= 1699 or # Heavy construction - not building contractors
          1700 <= sic_code <= 1799 or # Construction - special contractors
          2400 <= sic_code <= 2439 or # Lumber and wood products
          2450 <= sic_code <= 2459 or # Wood buildings & mobile homes
          2490 <= sic_code <= 2499 or # Misc wood products
          2660 <= sic_code <= 2661 or # Building paper and board mills
          2950 <= sic_code <= 2952 or # Paving & roofing materials
          3200 <= sic_code <= 3200 or # Stone, clay, glass, concrete, etc
          3210 <= sic_code <= 3211 or # Flat glass
          3240 <= sic_code <= 3241 or # Cement, hydraulic
          3250 <= sic_code <= 3259 or # Structural clay products
          3261 <= sic_code <= 3261 or # Vitreous china plumbing fixtures
          3264 <= sic_code <= 3264 or # Porcelain electrical supplies
          3270 <= sic_code <= 3275 or # Concrete, gypsum & plaster products
          3280 <= sic_code <= 3281 or # Cut stone and stone products
          3290 <= sic_code <= 3293 or # Abrasive and asbestos products
          3295 <= sic_code <= 3299 or # Misc nonmetallic mineral products
          3420 <= sic_code <= 3429 or # Cutlery, hand tools and general hardware
          3430 <= sic_code <= 3433 or # Heating equipment & plumbing fixtures
          3440 <= sic_code <= 3441 or # Fabricated structural metal products
          3442 <= sic_code <= 3442 or # Metal doors, frames
          3446 <= sic_code <= 3446 or # Architectural or ornamental metal work
          3448 <= sic_code <= 3448 or # Prefabricated metal buildings and components
          3449 <= sic_code <= 3449 or # Misc structural metal work
          3450 <= sic_code <= 3451 or # Screw machine products
          3452 <= sic_code <= 3452 or # Bolts, nuts, screws, rivets and washers
          3490 <= sic_code <= 3499 or # Misc fabricated metal products
          3996 <= sic_code <= 3996): # Hard surface floor coverings
        return "Cnstr"
    
    # 12 Steel  Steel Works Etc
    elif (3300 <= sic_code <= 3300 or # Primary metal industries
          3310 <= sic_code <= 3317 or # Blast furnaces & steel works
          3320 <= sic_code <= 3325 or # Iron & steel foundries
          3330 <= sic_code <= 3339 or # Primary smelting & refining of nonferrous metals
          3340 <= sic_code <= 3341 or # Secondary smelting & refining of nonferrous metals
          3350 <= sic_code <= 3357 or # Rolling, drawing & extruding of nonferrous metals
          3360 <= sic_code <= 3369 or # Nonferrous foundries and casting
          3370 <= sic_code <= 3379 or # Steel works etc
          3390 <= sic_code <= 3399): # Misc primary metal products
        return "Steel"

    # 13 FabPr  Fabricated Products and Machinery
    elif (3400 <= sic_code <= 3400 or # Fabricated metal, except machinery and trans eq
          3443 <= sic_code <= 3443 or # Fabricated plate work
          3444 <= sic_code <= 3444 or # Sheet metal work
          3460 <= sic_code <= 3469 or # Metal forgings and stampings
          3470 <= sic_code <= 3479 or # Coating, engraving and allied services
          3510 <= sic_code <= 3519 or # Engines & turbines
          3520 <= sic_code <= 3529 or # Farm and garden machinery and equipment
          3530 <= sic_code <= 3530 or # Construction, mining & material handling machinery & equipment
          3531 <= sic_code <= 3531 or # Construction machinery & equipment
          3532 <= sic_code <= 3532 or # Mining machinery & equipment, except oil field
          3533 <= sic_code <= 3533 or # Oil & gas field machinery & equipment
          3534 <= sic_code <= 3534 or # Elevators & moving stairways
          3535 <= sic_code <= 3535 or # Conveyors & conveying equipment
          3536 <= sic_code <= 3536 or # Cranes, hoists and monorail systems
          3538 <= sic_code <= 3538 or # Machinery
          3540 <= sic_code <= 3549 or # Metalworking machinery & equipment
          3550 <= sic_code <= 3559 or # Special industry machinery
          3560 <= sic_code <= 3569 or # General industrial machinery & equipment
          3580 <= sic_code <= 3580 or # Refrigeration & service industry machinery
          3581 <= sic_code <= 3581 or # Automatic vending machines
          3582 <= sic_code <= 3582 or # Commercial laundry and dry-cleaning machines
          3585 <= sic_code <= 3585 or # Air conditioning, warm air heating and refrigeration equipment
          3586 <= sic_code <= 3586 or # Measuring and dispensing pumps
          3589 <= sic_code <= 3589 or # Service industry machinery
          3590 <= sic_code <= 3599): # Misc industrial and commercial equipment and machinery
        return "FabPr"
    
    # 14 ElcEq  Electrical Equipment
    elif (3600 <= sic_code <= 3600 or # Electronic & other electrical equipment
          3610 <= sic_code <= 3613 or # Electric transmission and distribution equipment
          3620 <= sic_code <= 3621 or # Electrical industrial apparatus
          3623 <= sic_code <= 3629 or # Electrical industrial apparatus
          3640 <= sic_code <= 3644 or # Electric lighting & wiring equipment
          3645 <= sic_code <= 3645 or # Residential electric lighting fixtures
          3646 <= sic_code <= 3646 or # Commercial, industrial and institutional electric lighting fixtures
          3648 <= sic_code <= 3649 or # Misc lighting equipment
          3660 <= sic_code <= 3660 or # Communications equipment
          3690 <= sic_code <= 3690 or # Misc electrical machinery and equipment
          3691 <= sic_code <= 3692 or # Storage batteries
          3699 <= sic_code <= 3699): # Misc electrical machinery, equipment and supplies
        return "ElcEq"
    
    # 15 Autos  Automobiles and Trucks
    elif (3710 <= sic_code <= 3710 or # Motor vehicles and motor vehicle equipment
          3711 <= sic_code <= 3711 or # Motor vehicles & passenger car bodies
          3713 <= sic_code <= 3713 or # Truck & bus bodies
          3714 <= sic_code <= 3714 or # Motor vehicle parts & accessories
          3715 <= sic_code <= 3715 or # Truck trailers
          3716 <= sic_code <= 3716 or # Motor homes
          3792 <= sic_code <= 3792 or # Travel trailers and campers
          3790 <= sic_code <= 3791 or # Misc transportation equipment
          3799 <= sic_code <= 3799): # Misc transportation equipment
        return "Autos"
    
    # 16 Carry  Aircraft, ships, and railroad equipment
    elif (3720 <= sic_code <= 3720 or # Aircraft & parts
          3721 <= sic_code <= 3721 or # Aircraft
          3723 <= sic_code <= 3724 or # Aircraft engines & engine parts
          3725 <= sic_code <= 3725 or # Aircraft parts
          3728 <= sic_code <= 3729 or # Misc aircraft parts & auxiliary equipment
          3730 <= sic_code <= 3731 or # Ship building and repairing
          3740 <= sic_code <= 3743): # Railroad Equipment
        return "Carry"
    
    # 17 Mines  Precious Metals, Non-Metallic, and Industrial Metal Mining
    elif (1000 <= sic_code <= 1009 or # Metal mining
          1010 <= sic_code <= 1019 or # Iron ores
          1020 <= sic_code <= 1029 or # Copper ores
          1030 <= sic_code <= 1039 or # Lead and zinc ores
          1040 <= sic_code <= 1049 or # Gold & silver ores
          1050 <= sic_code <= 1059 or # Bauxite and other aluminum ores
          1060 <= sic_code <= 1069 or # Ferroalloy ores
          1070 <= sic_code <= 1079 or # Mining
          1080 <= sic_code <= 1089 or # Metal mining services
          1090 <= sic_code <= 1099 or # Misc metal ores
          1100 <= sic_code <= 1119 or # Anthracite mining
          1400 <= sic_code <= 1499): # Mining and quarrying nonmetallic minerals
        return "Mines"
    
    # 18 Coal   Coal
    elif (1200 <= sic_code <= 1299): # Bituminous coal
        return "Coal"

    # 19 Oil    Petroleum and Natural Gas
    elif (1300 <= sic_code <= 1300 or # Oil and gas extraction
          1310 <= sic_code <= 1319 or # Crude petroleum & natural gas
          1320 <= sic_code <= 1329 or # Natural gas liquids
          1330 <= sic_code <= 1339 or # Petroleum and natural gas
          1370 <= sic_code <= 1379 or # Petroleum and natural gas
          1380 <= sic_code <= 1380 or # Oil and gas field services
          1381 <= sic_code <= 1381 or # Drilling oil & gas wells
          1382 <= sic_code <= 1382 or # Oil & gas field exploration services
          1389 <= sic_code <= 1389 or # Misc oil & gas field services
          2900 <= sic_code <= 2912 or # Petroleum refining
          2990 <= sic_code <= 2999): # Misc products of petroleum & coal
        return "Oil"
    
    # 20 Util   Utilities
    elif (4900 <= sic_code <= 4900 or # Electric, gas & sanitary services
          4910 <= sic_code <= 4911 or # Electric services
          4920 <= sic_code <= 4922 or # Natural gas transmission
          4923 <= sic_code <= 4923 or # Natural gas transmission & distribution
          4924 <= sic_code <= 4925 or # Natural gas distribution
          4930 <= sic_code <= 4931 or # Electric and other services combined
          4932 <= sic_code <= 4932 or # Gas and other services combined
          4939 <= sic_code <= 4939 or # Misc combination utilities
          4940 <= sic_code <= 4942): # Water supply
        return "Util"
    
    # 21 Telcm  Communication
    elif (4800 <= sic_code <= 4800 or # Communications
          4810 <= sic_code <= 4813 or # Telephone communications
          4820 <= sic_code <= 4822 or # Telegraph and other message communication
          4830 <= sic_code <= 4839 or # Radio & TV broadcasters
          4840 <= sic_code <= 4841 or # Cable and other pay TV services
          4880 <= sic_code <= 4889 or # Communications
          4890 <= sic_code <= 4890 or # Communication services (Comsat)
          4891 <= sic_code <= 4891 or # Cable TV operators
          4892 <= sic_code <= 4892 or # Telephone interconnect
          4899 <= sic_code <= 4899): # Misc communication services
        return "Telcm"

    # 22 Servs  Personal and Business Services
    elif (7020 <= sic_code <= 7021 or # Rooming and boarding houses
          7030 <= sic_code <= 7033 or # Camps and recreational vehicle parks
          7200 <= sic_code <= 7200 or # Services - personal
          7210 <= sic_code <= 7212 or # Services - laundry, cleaning & garment services
          7214 <= sic_code <= 7214 or # Services - diaper service
          7215 <= sic_code <= 7216 or # Services - coin-operated cleaners, dry cleaners
          7217 <= sic_code <= 7217 or # Services - carpet & upholstery cleaning
          7218 <= sic_code <= 7218 or # Services - industrial launderers
          7219 <= sic_code <= 7219 or # Services - Misc laundry & garment services
          7220 <= sic_code <= 7221 or # Services - photographic studios, portrait
          7230 <= sic_code <= 7231 or # Services - beauty shops
          7240 <= sic_code <= 7241 or # Services - barber shops
          7250 <= sic_code <= 7251 or # Services - shoe repair shops & shoeshine parlors
          7260 <= sic_code <= 7269 or # Services - funeral service & crematories
          7270 <= sic_code <= 7290 or # Services – Misc
          7291 <= sic_code <= 7291 or # Services - tax return
          7292 <= sic_code <= 7299 or # Services - Misc
          7300 <= sic_code <= 7300 or # Services - business services
          7310 <= sic_code <= 7319 or # Services - advertising
          7320 <= sic_code <= 7329 or # Services - consumer credit reporting agencies, collection services
          7330 <= sic_code <= 7339 or # Services - mailing, reproduction, commercial art & photography
          7340 <= sic_code <= 7342 or # Services - services to dwellings & other buildings
          7349 <= sic_code <= 7349 or # Services - building cleaning & maintenance
          7350 <= sic_code <= 7351 or # Services - Misc equipment rental and leasing
          7352 <= sic_code <= 7352 or # Services - medical equipment rental and leasing
          7353 <= sic_code <= 7353 or # Services - heavy construction equipment rental and leasing
          7359 <= sic_code <= 7359 or # Services - equipment rental and leasing
          7360 <= sic_code <= 7369 or # Services - personnel supply services
          7370 <= sic_code <= 7372 or # Services - computer programming and data processing
          7374 <= sic_code <= 7374 or # Services - computer processing, data preparation and processing
          7375 <= sic_code <= 7375 or # Services - information retrieval services
          7376 <= sic_code <= 7376 or # Services - computer facilities management service
          7377 <= sic_code <= 7377 or # Services - computer rental and leasing
          7378 <= sic_code <= 7378 or # Services - computer maintenance and repair
          7379 <= sic_code <= 7379 or # Services - computer related services
          7380 <= sic_code <= 7380 or # Services - Misc business services
          7381 <= sic_code <= 7382 or # Services - security
          7383 <= sic_code <= 7383 or # Services - news syndicates
          7384 <= sic_code <= 7384 or # Services - photofinishing labs
          7385 <= sic_code <= 7385 or # Services - telephone interconnect systems
          7389 <= sic_code <= 7390 or # Services - Misc business services
          7391 <= sic_code <= 7391 or # Services - R&D labs
          7392 <= sic_code <= 7392 or # Services - management consulting & P.R.
          7393 <= sic_code <= 7393 or # Services - detective and protective (ADT)
          7394 <= sic_code <= 7394 or # Services - equipment rental & leasing
          7395 <= sic_code <= 7395 or # Services - photofinishing labs (School pictures)
          7396 <= sic_code <= 7396 or # Services - trading stamp services
          7397 <= sic_code <= 7397 or # Services - commercial testing labs
          7399 <= sic_code <= 7399 or # Services - business services
          7500 <= sic_code <= 7500 or # Services - auto repair, services & parking
          7510 <= sic_code <= 7519 or # Services - truck, auto, trailer rental & leasing
          7520 <= sic_code <= 7529 or # Services - automobile parking
          7530 <= sic_code <= 7539 or # Services - automotive repair shops
          7540 <= sic_code <= 7549 or # Services - automotive services, except repair (car washes)
          7600 <= sic_code <= 7600 or # Services - Misc repair services
          7620 <= sic_code <= 7620 or # Services - Electrical repair shops
          7622 <= sic_code <= 7622 or # Services - Radio and TV repair shops
          7623 <= sic_code <= 7623 or # Services - Refrigeration and air conditioning service & repair shops
          7629 <= sic_code <= 7629 or # Services - Electrical & electronic repair shops
          7630 <= sic_code <= 7631 or # Services - Watch, clock and jewelry repair
          7640 <= sic_code <= 7641 or # Services - Reupholster & furniture repair
          7690 <= sic_code <= 7699 or # Services - Misc repair shops & related services
          8100 <= sic_code <= 8199 or # Services - legal
          8200 <= sic_code <= 8299 or # Services - educational
          8300 <= sic_code <= 8399 or # Services - social services
          8400 <= sic_code <= 8499 or # Services - museums, art galleries, botanical and zoological gardens
          8600 <= sic_code <= 8699 or # Services - membership organizations
          8700 <= sic_code <= 8700 or # Services - engineering, accounting, research, management
          8710 <= sic_code <= 8713 or # Services - engineering, accounting, surveying
          8720 <= sic_code <= 8721 or # Services - accounting, auditing, bookkeeping
          8730 <= sic_code <= 8734 or # Services - research, development, testing labs
          8740 <= sic_code <= 8748 or # Services - management, public relations, consulting
          8800 <= sic_code <= 8899 or # Services - private households
          8900 <= sic_code <= 8910 or # Services - Misc
          8911 <= sic_code <= 8911 or # Services - Misc engineering & architect
          8920 <= sic_code <= 8999): # Services - Misc
        return "Servs"

    # 23 BusEq  Business Equipment
    elif (3570 <= sic_code <= 3579 or # Computer & office equipment
          3622 <= sic_code <= 3622 or # Industrial controls
          3661 <= sic_code <= 3661 or # Telephone and telegraph apparatus
          3662 <= sic_code <= 3662 or # Communications equipment
          3663 <= sic_code <= 3663 or # Radio & TV broadcasting & communications equipment
          3664 <= sic_code <= 3664 or # Search, navigation, guidance systems
          3665 <= sic_code <= 3665 or # Training equipment & simulators
          3666 <= sic_code <= 3666 or # Alarm & signaling products
          3669 <= sic_code <= 3669 or # Communication equipment
          3670 <= sic_code <= 3679 or # Electronic components & accessories
          3680 <= sic_code <= 3680 or # Computers
          3681 <= sic_code <= 3681 or # Computers - mini
          3682 <= sic_code <= 3682 or # Computers - mainframe
          3683 <= sic_code <= 3683 or # Computers - terminals
          3684 <= sic_code <= 3684 or # Computers - disk & tape drives
          3685 <= sic_code <= 3685 or # Computers - optical scanners
          3686 <= sic_code <= 3686 or # Computers - graphics
          3687 <= sic_code <= 3687 or # Computers - office automation systems
          3688 <= sic_code <= 3688 or # Computers - peripherals
          3689 <= sic_code <= 3689 or # Computers - equipment
          3695 <= sic_code <= 3695 or # Magnetic and optical recording media
          3810 <= sic_code <= 3810 or # Search, detection, navigation, guidance
          3811 <= sic_code <= 3811 or # Engr lab and research equipment
          3812 <= sic_code <= 3812 or # Search, detection, navigation, guidance
          3820 <= sic_code <= 3820 or # Measuring and controlling equipment
          3821 <= sic_code <= 3821 or # Laboratory apparatus and furniture
          3822 <= sic_code <= 3822 or # Automatic controls for regulating residential & commercial environments & appliances
          3823 <= sic_code <= 3823 or # Industrial measurement instruments & related products
          3824 <= sic_code <= 3824 or # Totalizing fluid meters & counting devices
          3825 <= sic_code <= 3825 or # Instruments for measuring & testing of electricity & electrical instruments
          3826 <= sic_code <= 3826 or # Lab analytical instruments
          3827 <= sic_code <= 3827 or # Optical instruments and lenses
          3829 <= sic_code <= 3829 or # Misc measuring and controlling devices
          3830 <= sic_code <= 3839 or # Optical instruments and lenses
          7373 <= sic_code <= 7373): # Computer integrated systems design
        return "BusEq"

    # 24 Paper  Business Supplies and Shipping Containers
    elif (2440 <= sic_code <= 2449 or # Wood containers
          2520 <= sic_code <= 2549 or # Office furniture and fixtures
          2600 <= sic_code <= 2639 or # Paper and allied products
          2640 <= sic_code <= 2659 or # Paperboard containers, boxes, drums, tubs
          2670 <= sic_code <= 2699 or # Paper and allied products
          2760 <= sic_code <= 2761 or # Manifold business forms
          3220 <= sic_code <= 3221 or # Glass containers
          3410 <= sic_code <= 3412 or # Metal cans and shipping containers
          3950 <= sic_code <= 3955): # Pens, pencils & other artists’ supplies
        return "Paper"

    # 25 Trans Transportation
    elif (4000 <= sic_code <= 4013 or # Railroads, line-haul operating
          4040 <= sic_code <= 4049 or # Railway express service
          4100 <= sic_code <= 4100 or # Local & suburban transit & interurban highway passenger transportation
          4110 <= sic_code <= 4119 or # Local & suburban passenger transportation
          4120 <= sic_code <= 4121 or # Taxicabs
          4130 <= sic_code <= 4131 or # Intercity & rural bus transportation (Greyhound)
          4140 <= sic_code <= 4142 or # Bus charter service
          4150 <= sic_code <= 4151 or # School buses
          4170 <= sic_code <= 4173 or # Motor vehicle terminals & service facilities
          4190 <= sic_code <= 4199 or # Misc transit and passenger transportation
          4200 <= sic_code <= 4200 or # Trucking & warehousing
          4210 <= sic_code <= 4219 or # Trucking & courier services, except air
          4220 <= sic_code <= 4229 or # Warehousing and storage
          4230 <= sic_code <= 4231 or # Terminal & joint terminal maintenance
          4240 <= sic_code <= 4249 or # Transportation
          4400 <= sic_code <= 4499 or # Water transport
          4500 <= sic_code <= 4599 or # Air transportation
          4600 <= sic_code <= 4699 or # Pipelines, except natural gas
          4700 <= sic_code <= 4700 or # Transportation services
          4710 <= sic_code <= 4712 or # Freight forwarding
          4720 <= sic_code <= 4729 or # Arrangement of passenger transportation
          4730 <= sic_code <= 4739 or # Arrangement of transportation of freight and cargo
          4740 <= sic_code <= 4749 or # Rental of railroad cars
          4780 <= sic_code <= 4780 or # Misc services incidental to transportation
          4782 <= sic_code <= 4782 or # Inspection and weighing services
          4783 <= sic_code <= 4783 or # Packing and crating
          4784 <= sic_code <= 4784 or # Misc fixed facilities for vehicles
          4785 <= sic_code <= 4785 or # Motor vehicle inspection
          4789 <= sic_code <= 4789): # Misc transportation services
        return "Trans"

    # 26 Whlsl  Wholesale
    elif (5000 <= sic_code <= 5000 or # Wholesale - durable goods
          5010 <= sic_code <= 5015 or # Wholesale - automotive vehicles & automotive parts & supplies
          5020 <= sic_code <= 5023 or # Wholesale - furniture and home furnishings
          5030 <= sic_code <= 5039 or # Wholesale - lumber and construction materials
          5040 <= sic_code <= 5042 or # Wholesale - professional and commercial equipment and supplies
          5043 <= sic_code <= 5043 or # Wholesale - photographic equipment & supplies
          5044 <= sic_code <= 5044 or # Wholesale - office equipment
          5045 <= sic_code <= 5045 or # Wholesale - computers & peripheral equipment & software
          5046 <= sic_code <= 5046 or # Wholesale - commercial equipment
          5047 <= sic_code <= 5047 or # Wholesale - medical, dental & hospital equipment
          5048 <= sic_code <= 5048 or # Wholesale - ophthalmic goods
          5049 <= sic_code <= 5049 or # Wholesale - professional equipment and supplies
          5050 <= sic_code <= 5059 or # Wholesale - metals and minerals, except petroleum
          5060 <= sic_code <= 5060 or # Wholesale - electrical goods
          5063 <= sic_code <= 5063 or # Wholesale - electrical apparatus and equipment
          5064 <= sic_code <= 5064 or # Wholesale - electrical appliance, TV and radio sets
          5065 <= sic_code <= 5065 or # Wholesale - electronic parts & equipment
          5070 <= sic_code <= 5078 or # Wholesale - hardware, plumbing & heating equipment
          5080 <= sic_code <= 5080 or # Wholesale - machinery, equipment & supplies
          5081 <= sic_code <= 5081 or # Wholesale - machinery & equipment (?)
          5082 <= sic_code <= 5082 or # Wholesale - construction and mining machinery &equipment
          5083 <= sic_code <= 5083 or # Wholesale - farm and garden machinery & equipment
          5084 <= sic_code <= 5084 or # Wholesale - industrial machinery & equipment
          5085 <= sic_code <= 5085 or # Wholesale - industrial supplies
          5086 <= sic_code <= 5087 or # Wholesale - service establishment machinery & equipment (?)
          5088 <= sic_code <= 5088 or # Wholesale - transportation equipment, except motor vehicles
          5090 <= sic_code <= 5090 or # Wholesale - Misc durable goods
          5091 <= sic_code <= 5092 or # Wholesale - sporting goods & toys
          5093 <= sic_code <= 5093 or # Wholesale - scrap and waste materials
          5094 <= sic_code <= 5094 or # Wholesale - jewelry, watches, precious stones & metals
          5099 <= sic_code <= 5099 or # Wholesale - durable goods
          5100 <= sic_code <= 5100 or # Wholesale - nondurable goods
          5110 <= sic_code <= 5113 or # Wholesale - paper and paper products
          5120 <= sic_code <= 5122 or # Wholesale - drugs & drug proprietaries
          5130 <= sic_code <= 5139 or # Wholesale - apparel, piece goods & notions
          5140 <= sic_code <= 5149 or # Wholesale - groceries & related products
          5150 <= sic_code <= 5159 or # Wholesale - farm product raw materials
          5160 <= sic_code <= 5169 or # Wholesale - chemicals & allied products
          5170 <= sic_code <= 5172 or # Wholesale - petroleum and petroleum products
          5180 <= sic_code <= 5182 or # Wholesale - beer, wine & distilled alcoholic beverages
          5190 <= sic_code <= 5199): # Wholesale - Misc nondurable goods
        return "Whlsl"
    
    # 27 Rtail  Retail
    elif (5200 <= sic_code <= 5200 or # Retail - retail-building materials, hardware, garden supply
          5210 <= sic_code <= 5219 or # Retail - lumber & other building materials
          5220 <= sic_code <= 5229 or # Retail
          5230 <= sic_code <= 5231 or # Retail - paint, glass & wallpaper
          5250 <= sic_code <= 5251 or # Retail - hardware
          5260 <= sic_code <= 5261 or # Retail - nurseries, lawn & garden
          5270 <= sic_code <= 5271 or # Retail - mobile home dealers
          5300 <= sic_code <= 5300 or # Retail - general merchandise
          5310 <= sic_code <= 5311 or # Retail - department stores
          5320 <= sic_code <= 5320 or # Retail - general merchandise (?)
          5330 <= sic_code <= 5331 or # Retail - variety stores
          5334 <= sic_code <= 5334 or # Retail - catalog showroom
          5340 <= sic_code <= 5349 or # Retail
          5390 <= sic_code <= 5399 or # Retail - Misc general merchandise
          5400 <= sic_code <= 5400 or # Retail - food stores
          5410 <= sic_code <= 5411 or # Retail - grocery stores
          5412 <= sic_code <= 5412 or # Retail - convenience stores
          5420 <= sic_code <= 5429 or # Retail - meat & fish markets
          5430 <= sic_code <= 5439 or # Retail - fruit and vegetable markets
          5440 <= sic_code <= 5449 or # Retail - candy, nut & confectionary stores
          5450 <= sic_code <= 5459 or # Retail - dairy products stores
          5460 <= sic_code <= 5469 or # Retail - bakeries
          5490 <= sic_code <= 5499 or # Retail - Misc food stores
          5500 <= sic_code <= 5500 or # Retail - automotive dealers and gas stations
          5510 <= sic_code <= 5529 or # Retail - automotive dealers
          5530 <= sic_code <= 5539 or # Retail - automotive and home supply stores
          5540 <= sic_code <= 5549 or # Retail - gasoline service stations
          5550 <= sic_code <= 5559 or # Retail - boat dealers
          5560 <= sic_code <= 5569 or # Retail - recreation vehicle dealers
          5570 <= sic_code <= 5579 or # Retail - motorcycle dealers
          5590 <= sic_code <= 5599 or # Retail - automotive dealers
          5600 <= sic_code <= 5699 or # Retail - apparel & accessory stores
          5700 <= sic_code <= 5700 or # Retail - home furniture and equipment stores
          5710 <= sic_code <= 5719 or # Retail - home furnishings stores
          5720 <= sic_code <= 5722 or # Retail - household appliance stores
          5730 <= sic_code <= 5733 or # Retail - radio, TV and consumer electronic stores
          5734 <= sic_code <= 5734 or # Retail - computer and computer software stores
          5735 <= sic_code <= 5735 or # Retail - record and tape stores
          5736 <= sic_code <= 5736 or # Retail - musical instrument stores
          5750 <= sic_code <= 5799 or # Retail
          5900 <= sic_code <= 5900 or # Retail - Misc
          5910 <= sic_code <= 5912 or # Retail - drug & proprietary stores
          5920 <= sic_code <= 5929 or # Retail - liquor stores
          5930 <= sic_code <= 5932 or # Retail - used merchandise stores
          5940 <= sic_code <= 5940 or # Retail - Misc
          5941 <= sic_code <= 5941 or # Retail - sporting goods stores & bike shops
          5942 <= sic_code <= 5942 or # Retail - book stores
          5943 <= sic_code <= 5943 or # Retail - stationery stores
          5944 <= sic_code <= 5944 or # Retail - jewelry stores
          5945 <= sic_code <= 5945 or # Retail - hobby, toy and game shops
          5946 <= sic_code <= 5946 or # Retail - camera and photographic supply stores
          5947 <= sic_code <= 5947 or # Retail - gift, novelty & souvenir shops
          5948 <= sic_code <= 5948 or # Retail - luggage & leather goods stores
          5949 <= sic_code <= 5949 or # Retail - sewing & needlework stores
          5950 <= sic_code <= 5959 or # Retail
          5960 <= sic_code <= 5969 or # Retail - non-store retailers (catalogs, etc)
          5970 <= sic_code <= 5979 or # Retail
          5980 <= sic_code <= 5989 or # Retail - fuel dealers & ice stores (Penn Central Co)
          5990 <= sic_code <= 5990 or # Retail - Misc retail stores
          5992 <= sic_code <= 5992 or # Retail - florists
          5993 <= sic_code <= 5993 or # Retail - tobacco stores and stands
          5994 <= sic_code <= 5994 or # Retail - newsdealers and news stands
          5995 <= sic_code <= 5995 or # Retail - optical goods stores
          5999 <= sic_code <= 5999): # Misc retail stores
        return "Rtail"

    # 28 Meals  Restaurants, Hotels, Motels
    elif (5800 <= sic_code <= 5819 or # Retail - eating places
          5820 <= sic_code <= 5829 or # Restaurants, hotels, motels
          5890 <= sic_code <= 5899 or # Eating and drinking places
          7000 <= sic_code <= 7000 or # Hotels & other lodging places
          7010 <= sic_code <= 7019 or # Hotels & motels
          7040 <= sic_code <= 7049 or # Membership hotels and lodging houses
          7213 <= sic_code <= 7213): # Services - linen supply
        return "Meals"
    
    # 29 Fin    Banking, Insurance, Real Estate, Trading
    elif (6000 <= sic_code <= 6000 or # Depository institutions
          6010 <= sic_code <= 6019 or # Federal reserve banks
          6020 <= sic_code <= 6020 or # Commercial banks
          6021 <= sic_code <= 6021 or # National commercial banks
          6022 <= sic_code <= 6022 or # State commercial banks - Fed Res System
          6023 <= sic_code <= 6024 or # State commercial banks - not Fed Res System
          6025 <= sic_code <= 6025 or # National commercial banks - Fed Res System
          6026 <= sic_code <= 6026 or # National commercial banks - not Fed Res System
          6027 <= sic_code <= 6027 or # National commercial banks, not FDIC
          6028 <= sic_code <= 6029 or # Misc commercial banks
          6030 <= sic_code <= 6036 or # Savings institutions
          6040 <= sic_code <= 6059 or # Banks (?)
          6060 <= sic_code <= 6062 or # Credit unions
          6080 <= sic_code <= 6082 or # Foreign banks
          6090 <= sic_code <= 6099 or # Functions related to depository banking
          6100 <= sic_code <= 6100 or # Non-depository credit institutions
          6110 <= sic_code <= 6111 or # Federal credit agencies
          6112 <= sic_code <= 6113 or # FNMA
          6120 <= sic_code <= 6129 or # S&Ls
          6130 <= sic_code <= 6139 or # Agricultural credit institutions
          6140 <= sic_code <= 6149 or # Personal credit institutions (Beneficial)
          6150 <= sic_code <= 6159 or # Business credit institutions
          6160 <= sic_code <= 6169 or # Mortgage bankers and brokers
          6170 <= sic_code <= 6179 or # Finance lessors
          6190 <= sic_code <= 6199 or # Financial services
          6200 <= sic_code <= 6299 or # Security and commodity brokers, dealers, exchanges & services
          6300 <= sic_code <= 6300 or # Insurance
          6310 <= sic_code <= 6319 or # Life insurance
          6320 <= sic_code <= 6329 or # Accident and health insurance
          6330 <= sic_code <= 6331 or # Fire, marine & casualty insurance
          6350 <= sic_code <= 6351 or # Surety insurance
          6360 <= sic_code <= 6361 or # Title insurance
          6370 <= sic_code <= 6379 or # Pension, health & welfare funds
          6390 <= sic_code <= 6399 or # Misc insurance carriers
          6400 <= sic_code <= 6411 or # Insurance agents, brokers & service
          6500 <= sic_code <= 6500 or # Real estate
          6510 <= sic_code <= 6510 or # Real estate operators and lessors
          6512 <= sic_code <= 6512 or # Operators - non-resident buildings
          6513 <= sic_code <= 6513 or # Operators - apartment buildings
          6514 <= sic_code <= 6514 or # Operators - other than apartment
          6515 <= sic_code <= 6515 or # Operators - residential mobile home
          6517 <= sic_code <= 6519 or # Lessors of railroad & real property
          6520 <= sic_code <= 6529 or # Real estate
          6530 <= sic_code <= 6531 or # Real estate agents and managers
          6532 <= sic_code <= 6532 or # Real estate dealers
          6540 <= sic_code <= 6541 or # Title abstract offices
          6550 <= sic_code <= 6553 or # Land subdividers & developers
          6590 <= sic_code <= 6599 or # Real estate
          6610 <= sic_code <= 6611 or # Combined real estate, insurance, etc
          6700 <= sic_code <= 6700 or # Holding & other investment offices
          6710 <= sic_code <= 6719 or # Holding offices
          6720 <= sic_code <= 6722 or # Management investment offices, open-end
          6723 <= sic_code <= 6723 or # Management investment offices, closed-end
          6724 <= sic_code <= 6724 or # Unit investment trusts
          6725 <= sic_code <= 6725 or # Face-amount certificate offices
          6726 <= sic_code <= 6726 or # Unit investment trusts, closed-end
          6730 <= sic_code <= 6733 or # Trusts
          6740 <= sic_code <= 6779 or # Investment offices
          6790 <= sic_code <= 6791 or # Misc investing
          6792 <= sic_code <= 6792 or # Oil royalty traders
          6793 <= sic_code <= 6793 or # Commodity traders
          6794 <= sic_code <= 6794 or # Patent owners & lessors
          6795 <= sic_code <= 6795 or # Mineral royalty traders
          6798 <= sic_code <= 6798 or # REIT
          6799 <= sic_code <= 6799): # Investors, NEC
        return "Fin"
    
    # 30 Other  Everything Else
    elif (4950 <= sic_code <= 4959 or # Sanitary services
          4960 <= sic_code <= 4961 or # Steam & air conditioning supplies
          4970 <= sic_code <= 4971 or # Irrigation systems
          4990 <= sic_code <= 4991): # Cogeneration - SM power producer
        return "Other"
    
    # Unclassified
    else:
        return "Unclassified"
    

def sic_to_industry_thirty_eight(sic_code: int) -> str:
    """
    Converts a SIC code into the Fama-French 38 industry classification.

    Args:
        sic_code (int): The SIC code to convert.

    Returns:
        str: The Fama-French 38 industry classification.
    """

    # 1 Agric  Agriculture, forestry, and fishing
    if (100 <= sic_code <= 999):
        return "Agric"
    
    # 2 Mines  Mining
    elif (1000 <= sic_code <= 1299):
        return "Mines"
    
    # 3 Oil    Oil and Gas Extraction
    elif (1300 <= sic_code <= 1399):
        return "Oil"
    
    # 4 Stone  Nonmetallic Minerals Except Fuels
    elif (1400 <= sic_code <= 1499):
        return "Stone"
    
    # 5 Cnstr  Construction
    elif (1500 <= sic_code <= 1799):
        return "Cnstr"
    
    # 6 Food   Food and Kindred Products
    elif (2000 <= sic_code <= 2099):
        return "Food"
    
    # 7 Smoke  Tobacco Products
    elif (2100 <= sic_code <= 2199):
        return "Smoke"
    
    # 8 Txtls  Textile Mill Products
    elif (2200 <= sic_code <= 2299):
        return "Txtls"
    
    # 9 Apprl  Apparel and other Textile Products
    elif (2300 <= sic_code <= 2399):
        return "Apprl"
    
    # 10 Wood   Lumber and Wood Products
    elif (2400 <= sic_code <= 2499):
        return "Wood"
    
    # 11 Chair  Furniture and Fixtures
    elif (2500 <= sic_code <= 2599):
        return "Chair"
    
    # 12 Paper  Paper and Allied Products
    elif (2600 <= sic_code <= 2661):
        return "Paper"
    
    # 13 Print  Printing and Publishing
    elif (2700 <= sic_code <= 2799):
        return "Print"
    
    # 14 Chems  Chemicals and Allied Products
    elif (2800 <= sic_code <= 2899):
        return "Chems"
    
    # 15 Ptrlm  Petroleum and Coal Products
    elif (2900 <= sic_code <= 2999):
        return "Ptrlm"
    
    # 16 Rubbr  Rubber and Miscellaneous Plastics Products
    elif (3000 <= sic_code <= 3099):
        return "Rubbr"
    
    # 17 Lethr  Leather and Leather Products
    elif (3100 <= sic_code <= 3199):
        return "Lethr"
    
    # 18 Glass  Stone, Clay and Glass Products
    elif (3200 <= sic_code <= 3299):
        return "Glass"
    
    # 19 Metal  Primary Metal Industries
    elif (3300 <= sic_code <= 3399):
        return "Metal"
    
    # 20 MtlPr  Fabricated Metal Products
    elif (3400 <= sic_code <= 3499):
        return "MtlPr"
    
    # 21 Machn  Machinery, Except Electrical
    elif (3500 <= sic_code <= 3599):
        return "Machn"
    
    # 22 Elctr  Electrical and Electronic Equipment
    elif (3600 <= sic_code <= 3699):
        return "Elctr"
    
    # 23 Cars   Transportation Equipment
    elif (3700 <= sic_code <= 3799):
        return "Cars"
    
    # 24 Instr  Instruments and Related Products
    elif (3800 <= sic_code <= 3879):
        return "Instr"
    
    # 25 Manuf  Miscellaneous Manufacturing Industries
    elif (3900 <= sic_code <= 3999):
        return "Manuf"
    
    # 26 Trans  Transportation
    elif (4000 <= sic_code <= 4799):
        return "Trans"
    
    # 27 Phone  Telephone and Telegraph Communication
    elif (4800 <= sic_code <= 4829):
        return "Phone"
    
    # 28 TV     Radio and Television Broadcasting
    elif (4830 <= sic_code <= 4899):
        return "TV"
    
    # 29 Utils  Electric, Gas, and Water Supply
    elif (4900 <= sic_code <= 4949):
        return "Utils"
    
    # 30 Garbg  Sanitary Services
    elif (4950 <= sic_code <= 4959):
        return "Garbg"
    
    # 31 Steam  Steam Supply
    elif (4960 <= sic_code <= 4969):
        return "Steam"
    
    # 32 Water  Irrigation Systems
    elif (4970 <= sic_code <= 4979):
        return "Water"
    
    # 33 Whlsl  Wholesale
    elif (5000 <= sic_code <= 5199):
        return "Whlsl"
    
    # 34 Rtail  Retail Stores
    elif (5200 <= sic_code <= 5999):
        return "Rtail"
    
    # 35 Money  Finance, Insurance, and Real Estate
    elif (6000 <= sic_code <= 6999):
        return "Money"
    
    # 36 Srvc   Services
    elif (7000 <= sic_code <= 8999):
        return "Srvc"
    
    # 37 Govt   Public Administration
    elif (9000 <= sic_code <= 9999):
        return "Govt"
    
    # 38 Other  Almost Nothing
    else:
        return "Other"


def sic_to_industry_forty_eight(sic_code: int) -> str:
    """
    Converts a SIC code into the Fama-French 48 industry classification.

    Args:
        sic_code (int): The SIC code to convert.

    Returns:
        str: The Fama-French 48 industry classification.
    """

    # 1 Agric  Agriculture
    if (100 <= sic_code <= 199 or # Agricultural production - crops
        200 <= sic_code <= 299 or # Agricultural production - livestock
        700 <= sic_code <= 799 or # Agricultural services
        910 <= sic_code <= 919 or # Commercial fishing
        2048 <= sic_code <= 2048): # Prepared feeds for animals
        return "Agric"
    
    # 2 Food   Food Products
    elif (2000 <= sic_code <= 2009 or # Food and kindred products
          2010 <= sic_code <= 2019 or # Meat products
          2020 <= sic_code <= 2029 or # Dairy products
          2030 <= sic_code <= 2039 or # Canned & preserved fruits & vegetables
          2040 <= sic_code <= 2046 or # Flour and other grain mill products
          2050 <= sic_code <= 2059 or # Bakery products
          2060 <= sic_code <= 2063 or # Sugar and confectionery products
          2070 <= sic_code <= 2079 or # Fats and oils
          2090 <= sic_code <= 2092 or # Misc food preparations and kindred products
          2095 <= sic_code <= 2095 or # Roasted coffee
          2098 <= sic_code <= 2099): # Misc food preparations
        return "Food"
    
    # 3 Soda   Candy & Soda
    elif (2064 <= sic_code <= 2068 or # Candy and other confectionery
          2086 <= sic_code <= 2086 or # Bottled-canned soft drinks
          2087 <= sic_code <= 2087 or # Flavoring syrup
          2096 <= sic_code <= 2096 or # Potato chips
          2097 <= sic_code <= 2097): # Manufactured ice
        return "Soda"
    
    # 4 Beer   Beer & Liquor
    elif (2080 <= sic_code <= 2080 or # Beverages
          2082 <= sic_code <= 2082 or # Malt beverages
          2083 <= sic_code <= 2083 or # Malt
          2084 <= sic_code <= 2084 or # Wine
          2085 <= sic_code <= 2085): # Distilled and blended liquors
        return "Beer"
    
    # 5 Smoke  Tobacco Products
    elif (2100 <= sic_code <= 2199): # Tobacco products
        return "Smoke"

    # 6 Toys   Recreation
    elif (920 <= sic_code <= 999 or # Fishing, hunting & trapping
          3650 <= sic_code <= 3651 or # Household audio visual equipment
          3652 <= sic_code <= 3652 or # Phonograph records
          3732 <= sic_code <= 3732 or # Boat building and repairing
          3930 <= sic_code <= 3931 or # Musical instruments
          3940 <= sic_code <= 3949): # Toys
        return "Toys"

    # 7 Fun    Entertainment
    elif (7800 <= sic_code <= 7829 or # Services - motion picture production and distribution
          7830 <= sic_code <= 7833 or # Services - motion picture theaters
          7840 <= sic_code <= 7841 or # Services - video rental
          7900 <= sic_code <= 7900 or # Services - amusement and recreation
          7910 <= sic_code <= 7911 or # Services - dance studios
          7920 <= sic_code <= 7929 or # Services - bands, entertainers
          7930 <= sic_code <= 7933 or # Services - bowling centers
          7940 <= sic_code <= 7949 or # Services - professional sports
          7980 <= sic_code <= 7980 or # Amusement and recreation services
          7990 <= sic_code <= 7999): # Services - Misc entertainment
        return "Fun"

    # 8 Books  Printing and Publishing
    elif (2700 <= sic_code <= 2709 or # Printing publishing and allied
          2710 <= sic_code <= 2719 or # Newspapers: publishing-printing
          2720 <= sic_code <= 2729 or # Periodicals: publishing-printing
          2730 <= sic_code <= 2739 or # Books: publishing-printing
          2740 <= sic_code <= 2749 or # Misc publishing
          2770 <= sic_code <= 2771 or # Greeting card
          2780 <= sic_code <= 2789 or # Bookbinding
          2790 <= sic_code <= 2799): # Service industries for the print trade
        return "Books"

    # 9 Hshld  Consumer Goods
    elif (2047 <= sic_code <= 2047 or # Dog and cat food
          2391 <= sic_code <= 2392 or # Curtains, home furnishings
          2510 <= sic_code <= 2519 or # Household furniture
          2590 <= sic_code <= 2599 or # Misc furniture and fixtures
          2840 <= sic_code <= 2843 or # Soap & other detergents
          2844 <= sic_code <= 2844 or # Perfumes, cosmetics and other toilet preparations
          3160 <= sic_code <= 3161 or # Luggage
          3170 <= sic_code <= 3171 or # Handbags and purses
          3172 <= sic_code <= 3172 or # Personal leather goods, except handbags and purses
          3190 <= sic_code <= 3199 or # Leather goods
          3229 <= sic_code <= 3229 or # Pressed and blown glass
          3260 <= sic_code <= 3260 or # Pottery and related products
          3262 <= sic_code <= 3263 or # China and earthenware table articles
          3269 <= sic_code <= 3269 or # Pottery products
          3230 <= sic_code <= 3231 or # Glass products
          3630 <= sic_code <= 3639 or # Household appliances
          3750 <= sic_code <= 3751 or # Motorcycles, bicycles and parts
          3800 <= sic_code <= 3800 or # Misc instruments, photo goods & watches
          3860 <= sic_code <= 3861 or # Photographic equipment
          3870 <= sic_code <= 3873 or # Watches, clocks and parts
          3910 <= sic_code <= 3911 or # Jewelry, precious metals
          3914 <= sic_code <= 3914 or # Silverware
          3915 <= sic_code <= 3915 or # Jewelers' findings and materials
          3960 <= sic_code <= 3962 or # Costume jewelry and novelties
          3991 <= sic_code <= 3991 or # Brooms and brushes
          3995 <= sic_code <= 3995): # Burial caskets
        return "Hshld"

    # 10 Clths  Apparel
    elif (2300 <= sic_code <= 2390 or # Apparel and other finished products
          3020 <= sic_code <= 3021 or # Rubber and plastics footwear
          3100 <= sic_code <= 3111 or # Leather tanning and finishing
          3130 <= sic_code <= 3131 or # Boot & shoe cut stock & findings
          3140 <= sic_code <= 3149 or # Footwear, except rubber
          3150 <= sic_code <= 3151 or # Leather gloves and mittens
          3963 <= sic_code <= 3965): # Fasteners, buttons, needles, pins
        return "Clths"

    # 11 Hlth   Healthcare
    elif (8000 <= sic_code <= 8099): # Services - health
        return "Hlth"

    # 12 MedEq  Medical Equipment
    elif (3693 <= sic_code <= 3693 or # X-ray, electromedical app
          3840 <= sic_code <= 3849 or # Surgical, medical, and dental instruments and supplies
          3850 <= sic_code <= 3851): # Ophthalmic goods
        return "MedEq"

    # 13 Drugs  Pharmaceutical Products
    elif (2830 <= sic_code <= 2830 or # Drugs
          2831 <= sic_code <= 2831 or # Biological products
          2833 <= sic_code <= 2833 or # Medicinal chemicals
          2834 <= sic_code <= 2834 or # Pharmaceutical preparations
          2835 <= sic_code <= 2835 or # In vitro, in vivo diagnostic substances
          2836 <= sic_code <= 2836): # Biological products, except diagnostic substances
        return "Drugs"

    # 14 Chems  Chemicals
    elif (2800 <= sic_code <= 2809 or # Chemicals and allied products
          2810 <= sic_code <= 2819 or # Industrial inorganic chemicals
          2820 <= sic_code <= 2829 or # Plastic material & synthetic resin/rubber
          2850 <= sic_code <= 2859 or # Paints
          2860 <= sic_code <= 2869 or # Industrial organic chemicals
          2870 <= sic_code <= 2879 or # Agriculture chemicals
          2890 <= sic_code <= 2899): # Misc chemical products
        return "Chems"

    # 15 Rubbr  Rubber and Plastic Products
    elif (3031 <= sic_code <= 3031 or # Reclaimed rubber
          3041 <= sic_code <= 3041 or # Rubber & plastic hose & belting
          3050 <= sic_code <= 3053 or # Gaskets, hoses, etc
          3060 <= sic_code <= 3069 or # Fabricated rubber products
          3070 <= sic_code <= 3079 or # Misc rubber products (?)
          3080 <= sic_code <= 3089 or # Misc plastic products
          3090 <= sic_code <= 3099): # Misc rubber and plastic products (?)
        return "Rubbr"

    # 16 Txtls  Textiles
    elif (2200 <= sic_code <= 2269 or # Textile mill products
          2270 <= sic_code <= 2279 or # Floor covering mills
          2280 <= sic_code <= 2284 or # Yarn and thread mills
          2290 <= sic_code <= 2295 or # Misc textile goods
          2297 <= sic_code <= 2297 or # Non-woven fabrics
          2298 <= sic_code <= 2298 or # Cordage and twine
          2299 <= sic_code <= 2299 or # Misc textile products
          2393 <= sic_code <= 2395 or # Textile bags, canvas products
          2397 <= sic_code <= 2399): # Misc textile products
        return "Txtls"

    # 17 BldMt  Construction Materials
    elif (800 <= sic_code <= 899 or # Forestry
          2400 <= sic_code <= 2439 or # Lumber and wood products
          2450 <= sic_code <= 2459 or # Wood buildings & mobile homes
          2490 <= sic_code <= 2499 or # Misc wood products
          2660 <= sic_code <= 2661 or # Building paper and board mills
          2950 <= sic_code <= 2952 or # Paving & roofing materials
          3200 <= sic_code <= 3200 or # Stone, clay, glass, concrete, etc
          3210 <= sic_code <= 3211 or # Flat glass
          3240 <= sic_code <= 3241 or # Cement, hydraulic
          3250 <= sic_code <= 3259 or # Structural clay products
          3261 <= sic_code <= 3261 or # Vitreous china plumbing fixtures
          3264 <= sic_code <= 3264 or # Porcelain electrical supplies
          3270 <= sic_code <= 3275 or # Concrete, gypsum & plaster products
          3280 <= sic_code <= 3281 or # Cut stone and stone products
          3290 <= sic_code <= 3293 or # Abrasive and asbestos products
          3295 <= sic_code <= 3299 or # Misc nonmetallic mineral products
          3420 <= sic_code <= 3429 or # Cutlery, hand tools and general hardware
          3430 <= sic_code <= 3433 or # Heating equipment & plumbing fixtures
          3440 <= sic_code <= 3441 or # Fabricated structural metal products
          3442 <= sic_code <= 3442 or # Metal doors, frames
          3446 <= sic_code <= 3446 or # Architectural or ornamental metal work
          3448 <= sic_code <= 3448 or # Prefabricated metal buildings and components
          3449 <= sic_code <= 3449 or # Misc structural metal work
          3450 <= sic_code <= 3451 or # Screw machine products
          3452 <= sic_code <= 3452 or # Bolts, nuts, screws, rivets and washers
          3490 <= sic_code <= 3499 or # Misc fabricated metal products
          3996 <= sic_code <= 3996): # Hard surface floor coverings
        return "BldMt"

    # 18 Cnstr  Construction
    elif (1500 <= sic_code <= 1511 or # Build construction - general contractors
          1520 <= sic_code <= 1529 or # General building contractors - residential
          1530 <= sic_code <= 1539 or # Operative builders
          1540 <= sic_code <= 1549 or # General building contractors - non-residential
          1600 <= sic_code <= 1699 or # Heavy construction - not building contractors
          1700 <= sic_code <= 1799): # Construction - special contractors
        return "Cnstr"

    # 19 Steel  Steel Works Etc
    elif (3300 <= sic_code <= 3300 or # Primary metal industries
          3310 <= sic_code <= 3317 or # Blast furnaces & steel works
          3320 <= sic_code <= 3325 or # Iron & steel foundries
          3330 <= sic_code <= 3339 or # Primary smelting & refining of nonferrous metals
          3340 <= sic_code <= 3341 or # Secondary smelting & refining of nonferrous metals
          3350 <= sic_code <= 3357 or # Rolling, drawing & extruding of nonferrous metals
          3360 <= sic_code <= 3369 or # Nonferrous foundries and casting
          3370 <= sic_code <= 3379 or # Steel works etc
          3390 <= sic_code <= 3399): # Misc primary metal products
        return "Steel"

    # 20 FabPr  Fabricated Products
    elif (3400 <= sic_code <= 3400 or # Fabricated metal, except machinery and trans eq
          3443 <= sic_code <= 3443 or # Fabricated plate work
          3444 <= sic_code <= 3444 or # Sheet metal work
          3460 <= sic_code <= 3469 or # Metal forgings and stampings
          3470 <= sic_code <= 3479): # Coating, engraving and allied services
        return "FabPr"

    # 21 Mach   Machinery
    elif (3510 <= sic_code <= 3519 or # Engines & turbines
          3520 <= sic_code <= 3529 or # Farm and garden machinery and equipment
          3530 <= sic_code <= 3530 or # Construction, mining & material handling machinery & equipment
          3531 <= sic_code <= 3531 or # Construction machinery & equipment
          3532 <= sic_code <= 3532 or # Mining machinery & equipment, except oil field
          3533 <= sic_code <= 3533 or # Oil & gas field machinery & equipment
          3534 <= sic_code <= 3534 or # Elevators & moving stairways
          3535 <= sic_code <= 3535 or # Conveyors & conveying equipment
          3536 <= sic_code <= 3536 or # Cranes, hoists and monorail systems
          3538 <= sic_code <= 3538 or # Machinery
          3540 <= sic_code <= 3549 or # Metalworking machinery & equipment
          3550 <= sic_code <= 3559 or # Special industry machinery
          3560 <= sic_code <= 3569 or # General industrial machinery & equipment
          3580 <= sic_code <= 3580 or # Refrigeration & service industry machinery
          3581 <= sic_code <= 3581 or # Automatic vending machines
          3582 <= sic_code <= 3582 or # Commercial laundry and dry-cleaning machines
          3585 <= sic_code <= 3585 or # Air conditioning, warm air heating and refrigeration equipment
          3586 <= sic_code <= 3586 or # Measuring and dispensing pumps
          3589 <= sic_code <= 3589 or # Service industry machinery
          3590 <= sic_code <= 3599): # Misc industrial and commercial equipment and machinery
        return "Mach"

    # 22 ElcEq  Electrical Equipment
    elif (3600 <= sic_code <= 3600 or # Electronic & other electrical equipment
          3610 <= sic_code <= 3613 or # Electric transmission and distribution equipment
          3620 <= sic_code <= 3621 or # Electrical industrial apparatus
          3623 <= sic_code <= 3629 or # Electrical industrial apparatus
          3640 <= sic_code <= 3644 or # Electric lighting & wiring equipment
          3645 <= sic_code <= 3645 or # Residential electric lighting fixtures
          3646 <= sic_code <= 3646 or # Commercial, industrial and institutional electric lighting fixtures
          3648 <= sic_code <= 3649 or # Misc lighting equipment
          3660 <= sic_code <= 3660 or # Communications equipment
          3690 <= sic_code <= 3690 or # Misc electrical machinery and equipment
          3691 <= sic_code <= 3692 or # Storage batteries
          3699 <= sic_code <= 3699): # Misc electrical machinery, equipment and supplies
        return "ElcEq"

    # 23 Autos  Automobiles and Trucks
    elif (2296 <= sic_code <= 2296 or # Tire cord and fabric
          2396 <= sic_code <= 2396 or # Automotive trimmings, apparel findings & related products
          3010 <= sic_code <= 3011 or # Tires and inner tubes
          3537 <= sic_code <= 3537 or # Industrial trucks, tractors, trailers & stackers
          3647 <= sic_code <= 3647 or # Vehicular lighting equipment
          3694 <= sic_code <= 3694 or # Electrical equipment for internal combustion engines
          3700 <= sic_code <= 3700 or # Transportation equipment
          3710 <= sic_code <= 3710 or # Motor vehicles and motor vehicle equipment
          3711 <= sic_code <= 3711 or # Motor vehicles & passenger car bodies
          3713 <= sic_code <= 3713 or # Truck & bus bodies
          3714 <= sic_code <= 3714 or # Motor vehicle parts & accessories
          3715 <= sic_code <= 3715 or # Truck trailers
          3716 <= sic_code <= 3716 or # Motor homes
          3792 <= sic_code <= 3792 or # Travel trailers and campers
          3790 <= sic_code <= 3791 or # Misc transportation equipment
          3799 <= sic_code <= 3799): # Misc transportation equipment
        return "Autos"

    # 24 Aero   Aircraft
    elif (3720 <= sic_code <= 3720 or # Aircraft & parts
          3721 <= sic_code <= 3721 or # Aircraft
          3723 <= sic_code <= 3724 or # Aircraft engines & engine parts
          3725 <= sic_code <= 3725 or # Aircraft parts
          3728 <= sic_code <= 3729): # Misc aircraft parts & auxiliary equipment
        return "Aero"

    # 25 Ships  Shipbuilding, Railroad Equipment
    elif (3730 <= sic_code <= 3731 or # Ship building and repairing
          3740 <= sic_code <= 3743): # Railroad Equipment
        return "Ships"
    
    # 26 Guns   Defense
    elif (3760 <= sic_code <= 3769 or # Guided missiles and space vehicles and parts
          3795 <= sic_code <= 3795 or # Tanks and tank components
          3480 <= sic_code <= 3489): # Ordnance & accessories
        return "Guns"

    # 27 Gold   Precious Metals
    elif (1040 <= sic_code <= 1049): # Gold & silver ores
        return "Gold"

    # 28 Mines  Non-Metallic and Industrial Metal Mining
    elif (1000 <= sic_code <= 1009 or # Metal mining
          1010 <= sic_code <= 1019 or # Iron ores
          1020 <= sic_code <= 1029 or # Copper ores
          1030 <= sic_code <= 1039 or # Lead and zinc ores
          1050 <= sic_code <= 1059 or # Bauxite and other aluminum ores
          1060 <= sic_code <= 1069 or # Ferroalloy ores
          1070 <= sic_code <= 1079 or # Mining
          1080 <= sic_code <= 1089 or # Metal mining services
          1090 <= sic_code <= 1099 or # Misc metal ores
          1100 <= sic_code <= 1119 or # Anthracite mining
          1400 <= sic_code <= 1499): # Mining and quarrying nonmetallic minerals
        return "Mines"

    # 29 Coal   Coal
    elif (1200 <= sic_code <= 1299): # Bituminous coal and lignite mining
        return "Coal"

    # 30 Oil    Petroleum and Natural Gas
    elif (1300 <= sic_code <= 1300 or # Oil and gas extraction
          1310 <= sic_code <= 1319 or # Crude petroleum & natural gas
          1320 <= sic_code <= 1329 or # Natural gas liquids
          1330 <= sic_code <= 1339 or # Petroleum and natural gas
          1370 <= sic_code <= 1379 or # Petroleum and natural gas
          1380 <= sic_code <= 1380 or # Oil and gas field services
          1381 <= sic_code <= 1381 or # Drilling oil & gas wells
          1382 <= sic_code <= 1382 or # Oil & gas field exploration services
          1389 <= sic_code <= 1389 or # Misc oil & gas field services
          2900 <= sic_code <= 2912 or # Petroleum refining
          2990 <= sic_code <= 2999): # Misc products of petroleum & coal
        return "Oil"

    # 31 Utils  Utilities
    elif (4900 <= sic_code <= 4900 or # Electric, gas and sanitary services
          4910 <= sic_code <= 4911 or # Electric services
          4920 <= sic_code <= 4922 or # Natural gas transmission
          4923 <= sic_code <= 4923 or # Natural gas transmission and distribution
          4924 <= sic_code <= 4925 or # Natural gas distribution
          4930 <= sic_code <= 4931 or # Electric and other services combined
          4932 <= sic_code <= 4932 or # Gas and other services combined
          4939 <= sic_code <= 4939 or # Misc combination utilities
          4940 <= sic_code <= 4942): # Water supply
        return "Utils"

    # 32 Telcm  Communication
    elif (4800 <= sic_code <= 4800 or # Communications
          4810 <= sic_code <= 4813 or # Telephone communications
          4820 <= sic_code <= 4822 or # Telegraph and other message communication
          4830 <= sic_code <= 4839 or # Radio and TV broadcasters
          4840 <= sic_code <= 4841 or # Cable and other pay TV services
          4880 <= sic_code <= 4889 or # Communications
          4890 <= sic_code <= 4890 or # Communication services (Comsat)
          4891 <= sic_code <= 4891 or # Cable TV operators
          4892 <= sic_code <= 4892 or # Telephone interconnect
          4899 <= sic_code <= 4899): # Misc communication services
        return "Telcm"

    # 33 PerSv  Personal Services
    elif (7020 <= sic_code <= 7021 or # Rooming and boarding houses
          7030 <= sic_code <= 7033 or # Camps and recreational vehicle parks
          7200 <= sic_code <= 7200 or # Services - personal
          7210 <= sic_code <= 7212 or # Services - laundry, cleaning and garment services
          7214 <= sic_code <= 7214 or # Services - diaper service
          7215 <= sic_code <= 7216 or # Services - coin-operated cleaners, dry cleaners
          7217 <= sic_code <= 7217 or # Services - carpet and upholstery cleaning
          7219 <= sic_code <= 7219 or # Services - Misc laundry and garment services
          7220 <= sic_code <= 7221 or # Services - photographic studios, portrait
          7230 <= sic_code <= 7231 or # Services - beauty shops
          7240 <= sic_code <= 7241 or # Services - barber shops
          7250 <= sic_code <= 7251 or # Services - shoe repair shops and shoeshine parlors
          7260 <= sic_code <= 7269 or # Services - funeral service and crematories
          7270 <= sic_code <= 7290 or # Services - Misc
          7291 <= sic_code <= 7291 or # Services - tax return
          7292 <= sic_code <= 7299 or # Services - Misc
          7395 <= sic_code <= 7395 or # Services - photofinishing labs (School pictures)
          7500 <= sic_code <= 7500 or # Services - auto repair, services and parking
          7520 <= sic_code <= 7529 or # Services - automobile parking
          7530 <= sic_code <= 7539 or # Services - automotive repair shops
          7540 <= sic_code <= 7549 or # Services - automotive services, except repair (car washes)
          7600 <= sic_code <= 7600 or # Services - Misc repair services
          7620 <= sic_code <= 7620 or # Services - Electrical repair shops
          7622 <= sic_code <= 7622 or # Services - Radio and TV repair shops
          7623 <= sic_code <= 7623 or # Services - Refrigeration and air conditioning service and repair shops
          7629 <= sic_code <= 7629 or # Services - Electrical and electronic repair shops
          7630 <= sic_code <= 7631 or # Services - Watch, clock and jewelry repair
          7640 <= sic_code <= 7641 or # Services - Reupholster and furniture repair
          7690 <= sic_code <= 7699 or # Services - Misc repair shops and related services
          8100 <= sic_code <= 8199 or # Services - legal
          8200 <= sic_code <= 8299 or # Services - educational
          8300 <= sic_code <= 8399 or # Services - social services
          8400 <= sic_code <= 8499 or # Services - museums, art galleries, botanical and zoological gardens
          8600 <= sic_code <= 8699 or # Services - membership organizations
          8800 <= sic_code <= 8899 or # Services - private households
          7510 <= sic_code <= 7515): # Services - truck and auto rental and leasing
        return "PerSv"

    # 34 BusSv  Business Services
    elif (2750 <= sic_code <= 2759 or # Commercial printing
          3993 <= sic_code <= 3993 or # Signs & advertising specialties
          7218 <= sic_code <= 7218 or # Services - industrial launderers
          7300 <= sic_code <= 7300 or # Services - business services
          7310 <= sic_code <= 7319 or # Services - advertising
          7320 <= sic_code <= 7329 or # Services - consumer credit reporting agencies, collection services
          7330 <= sic_code <= 7339 or # Services - mailing, reproduction, commercial art & photography
          7340 <= sic_code <= 7342 or # Services - services to dwellings & other buildings
          7349 <= sic_code <= 7349 or # Services - building cleaning & maintenance
          7350 <= sic_code <= 7351 or # Services - Misc equipment rental and leasing
          7352 <= sic_code <= 7352 or # Services - medical equipment rental and leasing
          7353 <= sic_code <= 7353 or # Services - heavy construction equipment rental and leasing
          7359 <= sic_code <= 7359 or # Services - equipment rental and leasing
          7360 <= sic_code <= 7369 or # Services - personnel supply services
          7370 <= sic_code <= 7372 or # Services - computer programming and data processing
          7374 <= sic_code <= 7374 or # Services - computer processing, data preparation and processing
          7375 <= sic_code <= 7375 or # Services - information retrieval services
          7376 <= sic_code <= 7376 or # Services - computer facilities management service
          7377 <= sic_code <= 7377 or # Services - computer rental and leasing
          7378 <= sic_code <= 7378 or # Services - computer maintenance and repair
          7379 <= sic_code <= 7379 or # Services - computer related services
          7380 <= sic_code <= 7380 or # Services - Misc business services
          7381 <= sic_code <= 7382 or # Services - security
          7383 <= sic_code <= 7383 or # Services - news syndicates
          7384 <= sic_code <= 7384 or # Services - photofinishing labs
          7385 <= sic_code <= 7385 or # Services - telephone interconnect systems
          7389 <= sic_code <= 7390 or # Services - Misc business services
          7391 <= sic_code <= 7391 or # Services - R&D labs
          7392 <= sic_code <= 7392 or # Services - management consulting & P.R.
          7393 <= sic_code <= 7393 or # Services - detective and protective (ADT)
          7394 <= sic_code <= 7394 or # Services - equipment rental & leasing
          7396 <= sic_code <= 7396 or # Services - trading stamp services
          7397 <= sic_code <= 7397 or # Services - commercial testing labs
          7399 <= sic_code <= 7399 or # Services - business services
          7519 <= sic_code <= 7519 or # Services - utility trailer & recreational vehicle rental
          8700 <= sic_code <= 8700 or # Services - engineering, accounting, research, management
          8710 <= sic_code <= 8713 or # Services - engineering, accounting, surveying
          8720 <= sic_code <= 8721 or # Services - accounting, auditing, bookkeeping
          8730 <= sic_code <= 8734 or # Services - research, development, testing labs
          8740 <= sic_code <= 8748 or # Services - management, public relations, consulting
          8900 <= sic_code <= 8910 or # Services - Misc
          8911 <= sic_code <= 8911 or # Services - Misc engineering & architect
          8920 <= sic_code <= 8999 or # Services - Misc
          4220 <= sic_code <= 4229): # Public warehousing and storage
        return "BusSv"

    # 35 Comps  Computers
    elif (3570 <= sic_code <= 3579 or # Computer & office equipment
          3680 <= sic_code <= 3680 or # Computers
          3681 <= sic_code <= 3681 or # Computers - mini
          3682 <= sic_code <= 3682 or # Computers - mainframe
          3683 <= sic_code <= 3683 or # Computers - terminals
          3684 <= sic_code <= 3684 or # Computers - disk & tape drives
          3685 <= sic_code <= 3685 or # Computers - optical scanners
          3686 <= sic_code <= 3686 or # Computers - graphics
          3687 <= sic_code <= 3687 or # Computers - office automation systems
          3688 <= sic_code <= 3688 or # Computers - peripherals
          3689 <= sic_code <= 3689 or # Computers - equipment
          3695 <= sic_code <= 3695 or # Magnetic and optical recording media
          7373 <= sic_code <= 7373): # Computer integrated systems design
        return "Comps"

    # 36 Chips  Electronic Equipment
    elif (3622 <= sic_code <= 3622 or # Industrial controls
          3661 <= sic_code <= 3661 or # Telephone and telegraph apparatus
          3662 <= sic_code <= 3662 or # Communications equipment
          3663 <= sic_code <= 3663 or # Radio & TV broadcasting & communications equipment
          3664 <= sic_code <= 3664 or # Search, navigation, guidance systems
          3665 <= sic_code <= 3665 or # Training equipment & simulators
          3666 <= sic_code <= 3666 or # Alarm & signaling products
          3669 <= sic_code <= 3669 or # Communication equipment
          3670 <= sic_code <= 3679 or # Electronic components & accessories
          3810 <= sic_code <= 3810 or # Search, detection, navigation, guidance
          3812 <= sic_code <= 3812): # Search, detection, navigation, guidance
        return "Chips"

    # 37 LabEq  Measuring and Control Equipment
    elif (3811 <= sic_code <= 3811 or # Engr lab and research equipment
          3820 <= sic_code <= 3820 or # Measuring and controlling equipment
          3821 <= sic_code <= 3821 or # Laboratory apparatus and furniture
          3822 <= sic_code <= 3822 or # Automatic controls for regulating residential & commercial environments & appliances
          3823 <= sic_code <= 3823 or # Industrial measurement instruments & related products
          3824 <= sic_code <= 3824 or # Totalizing fluid meters & counting devices
          3825 <= sic_code <= 3825 or # Instruments for measuring & testing of electricity & electrical instruments
          3826 <= sic_code <= 3826 or # Lab analytical instruments
          3827 <= sic_code <= 3827 or # Optical instruments and lenses
          3829 <= sic_code <= 3829 or # Misc measuring and controlling devices
          3830 <= sic_code <= 3839): # Optical instruments and lenses
        return "LabEq"

    # 38 Paper  Business Supplies
    elif (2520 <= sic_code <= 2549 or # Office furniture and fixtures
          2600 <= sic_code <= 2639 or # Paper and allied products
          2670 <= sic_code <= 2699 or # Paper and allied products
          2760 <= sic_code <= 2761 or # Manifold business forms
          3950 <= sic_code <= 3955): # Pens, pencils & other artists’ supplies
        return "Paper"

    # 39 Boxes  Shipping Containers
    elif (2440 <= sic_code <= 2449 or # Wood containers
          2640 <= sic_code <= 2659 or # Paperboard containers, boxes, drums, tubs
          3220 <= sic_code <= 3221 or # Glass containers
          3410 <= sic_code <= 3412): # Metal cans and shipping containers
        return "Boxes"

    # 40 Trans  Transportation
    elif (4000 <= sic_code <= 4013 or # Railroads, line-haul operating
          4040 <= sic_code <= 4049 or # Railway express service
          4100 <= sic_code <= 4100 or # Local & suburban transit & interurban highway passenger transportation
          4110 <= sic_code <= 4119 or # Local & suburban passenger transportation
          4120 <= sic_code <= 4121 or # Taxicabs
          4130 <= sic_code <= 4131 or # Intercity & rural bus transportation (Greyhound)
          4140 <= sic_code <= 4142 or # Bus charter service
          4150 <= sic_code <= 4151 or # School buses
          4170 <= sic_code <= 4173 or # Motor vehicle terminals & service facilities
          4190 <= sic_code <= 4199 or # Misc transit and passenger transportation
          4200 <= sic_code <= 4200 or # Trucking & warehousing
          4210 <= sic_code <= 4219 or # Trucking & courier services, except air
          4230 <= sic_code <= 4231 or # Terminal & joint terminal maintenance
          4240 <= sic_code <= 4249 or # Transportation
          4400 <= sic_code <= 4499 or # Water transport
          4500 <= sic_code <= 4599 or # Air transportation
          4600 <= sic_code <= 4699 or # Pipelines, except natural gas
          4700 <= sic_code <= 4700 or # Transportation services
          4710 <= sic_code <= 4712 or # Freight forwarding
          4720 <= sic_code <= 4729 or # Arrangement of passenger transportation
          4730 <= sic_code <= 4739 or # Arrangement of transportation of freight and cargo
          4740 <= sic_code <= 4749 or # Rental of railroad cars
          4780 <= sic_code <= 4780 or # Misc services incidental to transportation
          4782 <= sic_code <= 4782 or # Inspection and weighing services
          4783 <= sic_code <= 4783 or # Packing and crating
          4784 <= sic_code <= 4784 or # Misc fixed facilities for vehicles
          4785 <= sic_code <= 4785 or # Motor vehicle inspection
            4789 <= sic_code <= 4789): # Misc transportation services
        return "Trans"

    # 41 Whlsl  Wholesale
    elif (5000 <= sic_code <= 5000 or # Wholesale - durable goods
          5010 <= sic_code <= 5015 or # Wholesale - automotive vehicles & automotive parts & supplies
          5020 <= sic_code <= 5023 or # Wholesale - furniture and home furnishings
          5030 <= sic_code <= 5039 or # Wholesale - lumber and construction materials
          5040 <= sic_code <= 5042 or # Wholesale - professional and commercial equipment and supplies
          5043 <= sic_code <= 5043 or # Wholesale - photographic equipment & supplies
          5044 <= sic_code <= 5044 or # Wholesale - office equipment
          5045 <= sic_code <= 5045 or # Wholesale - computers & peripheral equipment & software
          5046 <= sic_code <= 5046 or # Wholesale - commercial equipment
          5047 <= sic_code <= 5047 or # Wholesale - medical, dental & hospital equipment
          5048 <= sic_code <= 5048 or # Wholesale - ophthalmic goods
          5049 <= sic_code <= 5049 or # Wholesale - professional equipment and supplies
          5050 <= sic_code <= 5059 or # Wholesale - metals and minerals, except petroleum
          5060 <= sic_code <= 5060 or # Wholesale - electrical goods
          5063 <= sic_code <= 5063 or # Wholesale - electrical apparatus and equipment
          5064 <= sic_code <= 5064 or # Wholesale - electrical appliance, TV and radio sets
          5065 <= sic_code <= 5065 or # Wholesale - electronic parts & equipment
          5070 <= sic_code <= 5078 or # Wholesale - hardware, plumbing & heating equipment
          5080 <= sic_code <= 5080 or # Wholesale - machinery, equipment & supplies
          5081 <= sic_code <= 5081 or # Wholesale - machinery & equipment (?)
          5082 <= sic_code <= 5082 or # Wholesale - construction and mining machinery &equipment
          5083 <= sic_code <= 5083 or # Wholesale - farm and garden machinery & equipment
          5084 <= sic_code <= 5084 or # Wholesale - industrial machinery & equipment
          5085 <= sic_code <= 5085 or # Wholesale - industrial supplies
          5086 <= sic_code <= 5087 or # Wholesale - service establishment machinery & equipment (?)
          5088 <= sic_code <= 5088 or # Wholesale - transportation equipment, except motor vehicles
          5090 <= sic_code <= 5090 or # Wholesale - Misc durable goods
          5091 <= sic_code <= 5092 or # Wholesale - sporting goods & toys
          5093 <= sic_code <= 5093 or # Wholesale - scrap and waste materials
          5094 <= sic_code <= 5094 or # Wholesale - jewelry, watches, precious stones & metals
          5099 <= sic_code <= 5099 or # Wholesale - durable goods
          5100 <= sic_code <= 5100 or # Wholesale - nondurable goods
          5110 <= sic_code <= 5113 or # Wholesale - paper and paper products
          5120 <= sic_code <= 5122 or # Wholesale - drugs & drug proprietaries
          5130 <= sic_code <= 5139 or # Wholesale - apparel, piece goods & notions
          5140 <= sic_code <= 5149 or # Wholesale - groceries & related products
          5150 <= sic_code <= 5159 or # Wholesale - farm product raw materials
          5160 <= sic_code <= 5169 or # Wholesale - chemicals & allied products
          5170 <= sic_code <= 5172 or # Wholesale - petroleum and petroleum products
          5180 <= sic_code <= 5182 or # Wholesale - beer, wine & distilled alcoholic beverages
          5190 <= sic_code <= 5199): # Wholesale - Misc nondurable goods
        return "Whlsl"

    # 42 Rtail  Retail
    elif (5200 <= sic_code <= 5200 or # Retail - retail-building materials, hardware, garden supply
          5210 <= sic_code <= 5219 or # Retail - lumber & other building materials
          5220 <= sic_code <= 5229 or # Retail
          5230 <= sic_code <= 5231 or # Retail - paint, glass & wallpaper stores
          5250 <= sic_code <= 5251 or # Retail - hardware stores
          5260 <= sic_code <= 5261 or # Retail - nurseries, lawn & garden supply stores
          5270 <= sic_code <= 5271 or # Retail - mobile home dealers
          5300 <= sic_code <= 5300 or # Retail - general merchandise stores
          5310 <= sic_code <= 5311 or # Retail - department stores
          5320 <= sic_code <= 5320 or # Retail - general merchandise stores (?)
          5330 <= sic_code <= 5331 or # Retail - variety stores
          5334 <= sic_code <= 5334 or # Retail - catalog showroom
          5340 <= sic_code <= 5349 or # Retail
          5390 <= sic_code <= 5399 or # Retail - Misc general merchandise stores
          5400 <= sic_code <= 5400 or # Retail - food stores
          5410 <= sic_code <= 5411 or # Retail - grocery stores
          5412 <= sic_code <= 5412 or # Retail - convenience stores
          5420 <= sic_code <= 5429 or # Retail - meat & fish markets
          5430 <= sic_code <= 5439 or # Retail - fruit and vegetable markets
          5440 <= sic_code <= 5449 or # Retail - candy, nut & confectionary stores
          5450 <= sic_code <= 5459 or # Retail - dairy products stores
          5460 <= sic_code <= 5469 or # Retail - bakeries
          5490 <= sic_code <= 5499 or # Retail - Misc food stores
          5500 <= sic_code <= 5500 or # Retail - automotive dealers and gas stations
          5510 <= sic_code <= 5529 or # Retail - automotive dealers
          5530 <= sic_code <= 5539 or # Retail - automotive and home supply stores
          5540 <= sic_code <= 5549 or # Retail - gasoline service stations
          5550 <= sic_code <= 5559 or # Retail - boat dealers
          5560 <= sic_code <= 5569 or # Retail - recreation vehicle dealers
          5570 <= sic_code <= 5579 or # Retail - motorcycle dealers
          5590 <= sic_code <= 5599 or # Retail - automotive dealers
          5600 <= sic_code <= 5699 or # Retail - apparel & accessory stores
          5700 <= sic_code <= 5700 or # Retail - home furniture and equipment stores
          5710 <= sic_code <= 5719 or # Retail - home furnishings stores
          5720 <= sic_code <= 5722 or # Retail - household appliance stores
          5730 <= sic_code <= 5733 or # Retail - radio, TV and consumer electronic stores
          5734 <= sic_code <= 5734 or # Retail - computer and computer software stores
          5735 <= sic_code <= 5735 or # Retail - record and tape stores
          5736 <= sic_code <= 5736 or # Retail - musical instrument stores
          5750 <= sic_code <= 5799 or # Retail
          5900 <= sic_code <= 5900 or # Retail - Misc
          5910 <= sic_code <= 5912 or # Retail - drug & proprietary stores
          5920 <= sic_code <= 5929 or # Retail - liquor stores
          5930 <= sic_code <= 5932 or # Retail - used merchandise stores
          5940 <= sic_code <= 5940 or # Retail - Misc
          5941 <= sic_code <= 5941 or # Retail - sporting goods stores & bike shops
          5942 <= sic_code <= 5942 or # Retail - book stores
          5943 <= sic_code <= 5943 or # Retail - stationery stores
          5944 <= sic_code <= 5944 or # Retail - jewelry stores
          5945 <= sic_code <= 5945 or # Retail - hobby, toy and game shops
          5946 <= sic_code <= 5946 or # Retail - camera and photographic supply stores
          5947 <= sic_code <= 5947 or # Retail - gift, novelty & souvenir shops
          5948 <= sic_code <= 5948 or # Retail - luggage & leather goods stores
          5949 <= sic_code <= 5949 or # Retail - sewing & needlework stores
          5950 <= sic_code <= 5959 or # Retail
          5960 <= sic_code <= 5969 or # Retail - non-store retailers (catalogs, etc)
          5970 <= sic_code <= 5979 or # Retail
          5980 <= sic_code <= 5989 or # Retail - fuel dealers & ice stores (Penn Central Co)
          5990 <= sic_code <= 5990 or # Retail - Misc retail stores
          5992 <= sic_code <= 5992 or # Retail - florists
          5993 <= sic_code <= 5993 or # Retail - tobacco stores and stands
          5994 <= sic_code <= 5994 or # Retail - newsdealers and news stands
          5995 <= sic_code <= 5995 or # Retail - optical goods stores
          5999 <= sic_code <= 5999): # Misc retail stores
        return "Rtail"

    # 43 Meals  Restaurants, Hotels, Motels
    elif (5800 <= sic_code <= 5819 or # Retail - eating places
          5820 <= sic_code <= 5829 or # Restaurants, hotels, motels
          5890 <= sic_code <= 5899 or # Eating and drinking places
          7000 <= sic_code <= 7000 or # Hotels & other lodging places
          7010 <= sic_code <= 7019 or # Hotels & motels
          7040 <= sic_code <= 7049 or # Membership hotels and lodging houses
          7213 <= sic_code <= 7213): # Services - linen supply
        return "Meals"

    # 44 Banks  Banking
    elif (6000 <= sic_code <= 6000 or # Depository institutions
          6010 <= sic_code <= 6019 or # Federal reserve banks
          6020 <= sic_code <= 6020 or # Commercial banks
          6021 <= sic_code <= 6021 or # National commercial banks
          6022 <= sic_code <= 6022 or # State commercial banks - Fed Res System
          6023 <= sic_code <= 6024 or # State commercial banks - not Fed Res System
          6025 <= sic_code <= 6025 or # National commercial banks - Fed Res System
          6026 <= sic_code <= 6026 or # National commercial banks - not Fed Res System
          6027 <= sic_code <= 6027 or # National commercial banks, not FDIC                        
          6028 <= sic_code <= 6029 or # Misc commercial banks
          6030 <= sic_code <= 6036 or # Savings institutions
          6040 <= sic_code <= 6059 or # Banks (?)
          6060 <= sic_code <= 6062 or # Credit unions
          6080 <= sic_code <= 6082 or # Foreign banks
          6090 <= sic_code <= 6099 or # Functions related to depository banking
          6100 <= sic_code <= 6100 or # Non-depository credit institutions
          6110 <= sic_code <= 6111 or # Federal credit agencies
          6112 <= sic_code <= 6113 or # FNMA
          6120 <= sic_code <= 6129 or # S&Ls
          6130 <= sic_code <= 6139 or # Agricultural credit institutions                
          6140 <= sic_code <= 6149 or # Personal credit institutions (Beneficial)
          6150 <= sic_code <= 6159 or # Business credit institutions
          6160 <= sic_code <= 6169 or # Mortgage bankers and brokers
          6170 <= sic_code <= 6179 or # Finance lessors
          6190 <= sic_code <= 6199): # Financial services
        return "Banks"

    # 45 Insur  Insurance
    elif (6300 <= sic_code <= 6300 or # Insurance
          6310 <= sic_code <= 6319 or # Life insurance
          6320 <= sic_code <= 6329 or # Accident and health insurance
          6330 <= sic_code <= 6331 or # Fire, marine & casualty insurance
          6350 <= sic_code <= 6351 or # Surety insurance
          6360 <= sic_code <= 6361 or # Title insurance
          6370 <= sic_code <= 6379 or # Pension, health & welfare funds
          6390 <= sic_code <= 6399 or # Misc insurance carriers
          6400 <= sic_code <= 6411): # Insurance agents, brokers & service
        return "Insur"

    # 46 RlEst  Real Estate
    elif (6500 <= sic_code <= 6500 or # Real estate
          6510 <= sic_code <= 6510 or # Real estate operators and lessors
          6512 <= sic_code <= 6512 or # Operators - non-resident buildings
          6513 <= sic_code <= 6513 or # Operators - apartment buildings
          6514 <= sic_code <= 6514 or # Operators - other than apartment
          6515 <= sic_code <= 6515 or # Operators - residential mobile home
          6517 <= sic_code <= 6519 or # Lessors of railroad & real property
          6520 <= sic_code <= 6529 or # Real estate
          6530 <= sic_code <= 6531 or # Real estate agents and managers
          6532 <= sic_code <= 6532 or # Real estate dealers
          6540 <= sic_code <= 6541 or # Title abstract offices
          6550 <= sic_code <= 6553 or # Land subdividers & developers
          6590 <= sic_code <= 6599 or # Real estate
          6610 <= sic_code <= 6611): # Combined real estate, insurance, etc
        return "RlEst"

    # 47 Fin    Trading
    elif (6200 <= sic_code <= 6299 or # Security and commodity brokers, dealers, exchanges & services
          6700 <= sic_code <= 6700 or # Holding & other investment offices
          6710 <= sic_code <= 6719 or # Holding offices
          6720 <= sic_code <= 6722 or # Management investment offices, open-end
          6723 <= sic_code <= 6723 or # Management investment offices, closed-end
          6724 <= sic_code <= 6724 or # Unit investment trusts                          
          6725 <= sic_code <= 6725 or # Face-amount certificate offices 
          6726 <= sic_code <= 6726 or # Unit investment trusts, closed-end                
          6730 <= sic_code <= 6733 or # Trusts
          6740 <= sic_code <= 6779 or # Investment offices
          6790 <= sic_code <= 6791 or # Misc investing
          6792 <= sic_code <= 6792 or # Oil royalty traders
          6793 <= sic_code <= 6793 or # Commodity traders                               
          6794 <= sic_code <= 6794 or # Patent owners & lessors
          6795 <= sic_code <= 6795 or # Mineral royalty traders
          6798 <= sic_code <= 6798 or # REIT
          6799 <= sic_code <= 6799): # Investors, NEC
        return "Fin"

    # 48 Other  Almost Nothing
    elif (4950 <= sic_code <= 4959 or # Sanitary services
          4960 <= sic_code <= 4961 or # Steam & air conditioning supplies
          4970 <= sic_code <= 4971 or # Irrigation systems
          4990 <= sic_code <= 4991): # Cogeneration - SM power producer
        return "Other"

    # Unclassified
    else:
        return "Unclassified"


def sic_to_industry_fourty_nine(sic_code: int) -> str:
    """
    Converts a SIC code into the Fama-French 49 industry classification.

    Args:
        sic_code (int): The SIC code to convert.

    Returns:
        str: The Fama-French 49 industry classification.
    """

    # 1 Agric  Agriculture
    if (100 <= sic_code <= 199 or # Agricultural production - crops
        200 <= sic_code <= 299 or # Agricultural production - livestock
        700 <= sic_code <= 799 or # Agricultural services
        910 <= sic_code <= 919 or # Commercial fishing
        2048 <= sic_code <= 2048): # Prepared feeds for animals
        return "Agric"
    
    # 2 Food   Food Products
    elif (2000 <= sic_code <= 2009 or # Food and kindred products
          2010 <= sic_code <= 2019 or # Meat products
          2020 <= sic_code <= 2029 or # Dairy products
          2030 <= sic_code <= 2039 or # Canned & preserved fruits & vegetables
          2040 <= sic_code <= 2046 or # Flour and other grain mill products
          2050 <= sic_code <= 2059 or # Bakery products
          2060 <= sic_code <= 2063 or # Sugar and confectionery products
          2070 <= sic_code <= 2079 or # Fats and oils
          2090 <= sic_code <= 2092 or # Misc food preparations and kindred products
          2095 <= sic_code <= 2095 or # Roasted coffee
          2098 <= sic_code <= 2099): # Misc food preparations
        return "Food"
    
    # 3 Soda   Candy & Soda
    elif (2064 <= sic_code <= 2068 or # Candy and other confectionery
          2086 <= sic_code <= 2086 or # Bottled-canned soft drinks
          2087 <= sic_code <= 2087 or # Flavoring syrup
          2096 <= sic_code <= 2096 or # Potato chips
          2097 <= sic_code <= 2097): # Manufactured ice
        return "Soda"
    
    # 4 Beer   Beer & Liquor
    elif (2080 <= sic_code <= 2080 or # Beverages
          2082 <= sic_code <= 2082 or # Malt beverages
          2083 <= sic_code <= 2083 or # Malt
          2084 <= sic_code <= 2084 or # Wine
          2085 <= sic_code <= 2085): # Distilled and blended liquors
        return "Beer"
    
    # 5 Smoke  Tobacco Products
    elif (2100 <= sic_code <= 2199): # Tobacco products
        return "Smoke"

    # 6 Toys   Recreation
    elif (920 <= sic_code <= 999 or # Fishing, hunting & trapping
          3650 <= sic_code <= 3651 or # Household audio visual equipment
          3652 <= sic_code <= 3652 or # Phonograph records
          3732 <= sic_code <= 3732 or # Boat building and repairing
          3930 <= sic_code <= 3931 or # Musical instruments
          3940 <= sic_code <= 3949): # Toys
        return "Toys"

    # 7 Fun    Entertainment
    elif (7800 <= sic_code <= 7829 or # Services - motion picture production and distribution
          7830 <= sic_code <= 7833 or # Services - motion picture theaters
          7840 <= sic_code <= 7841 or # Services - video rental
          7900 <= sic_code <= 7900 or # Services - amusement and recreation
          7910 <= sic_code <= 7911 or # Services - dance studios
          7920 <= sic_code <= 7929 or # Services - bands, entertainers
          7930 <= sic_code <= 7933 or # Services - bowling centers
          7940 <= sic_code <= 7949 or # Services - professional sports
          7980 <= sic_code <= 7980 or # Amusement and recreation services (?)
          7990 <= sic_code <= 7999): # Services - Misc entertainment
        return "Fun"

    # 8 Books  Printing and Publishing
    elif (2700 <= sic_code <= 2709 or # Printing publishing and allied
          2710 <= sic_code <= 2719 or # Newspapers: publishing-printing
          2720 <= sic_code <= 2729 or # Periodicals: publishing-printing
          2730 <= sic_code <= 2739 or # Books: publishing-printing
          2740 <= sic_code <= 2749 or # Misc publishing
          2770 <= sic_code <= 2771 or # Greeting card
          2780 <= sic_code <= 2789 or # Bookbinding
          2790 <= sic_code <= 2799): # Service industries for the print trade
        return "Books"

    # 9 Hshld  Consumer Goods
    elif (2047 <= sic_code <= 2047 or # Dog and cat food
          2391 <= sic_code <= 2392 or # Curtains, home furnishings
          2510 <= sic_code <= 2519 or # Household furniture
          2590 <= sic_code <= 2599 or # Misc furniture and fixtures
          2840 <= sic_code <= 2843 or # Soap & other detergents
          2844 <= sic_code <= 2844 or # Perfumes, cosmetics and other toilet preparations
          3160 <= sic_code <= 3161 or # Luggage
          3170 <= sic_code <= 3171 or # Handbags and purses
          3172 <= sic_code <= 3172 or # Personal leather goods, except handbags and purses
          3190 <= sic_code <= 3199 or # Leather goods
          3229 <= sic_code <= 3229 or # Pressed and blown glass
          3260 <= sic_code <= 3260 or # Pottery and related products
          3262 <= sic_code <= 3263 or # China and earthenware table articles
          3269 <= sic_code <= 3269 or # Pottery products
          3230 <= sic_code <= 3231 or # Glass products
          3630 <= sic_code <= 3639 or # Household appliances
          3750 <= sic_code <= 3751 or # Motorcycles, bicycles and parts  (Harley & Huffy)
          3800 <= sic_code <= 3800 or # Misc instruments, photo goods & watches
          3860 <= sic_code <= 3861 or # Photographic equipment  (Kodak etc, but also Xerox)
          3870 <= sic_code <= 3873 or # Watches, clocks and parts
          3910 <= sic_code <= 3911 or # Jewelry, precious metals
          3914 <= sic_code <= 3914 or # Silverware
          3915 <= sic_code <= 3915 or # Jewelers' findings and materials
          3960 <= sic_code <= 3962 or # Costume jewelry and novelties
          3991 <= sic_code <= 3991 or # Brooms and brushes
          3995 <= sic_code <= 3995): # Burial caskets
        return "Hshld"

    # 10 Clths  Apparel
    elif (2300 <= sic_code <= 2390 or # Apparel and other finished products
          3020 <= sic_code <= 3021 or # Rubber and plastics footwear
          3100 <= sic_code <= 3111 or # Leather tanning and finishing
          3130 <= sic_code <= 3131 or # Boot & shoe cut stock & findings
          3140 <= sic_code <= 3149 or # Footwear, except rubber
          3150 <= sic_code <= 3151 or # Leather gloves and mittens
          3963 <= sic_code <= 3965): # Fasteners, buttons, needles, pins
        return "Clths"

    # 11 Hlth   Healthcare
    elif (8000 <= sic_code <= 8099): # Services - health
        return "Hlth"

    # 12 MedEq  Medical Equipment
    elif (3693 <= sic_code <= 3693 or # X-ray, electromedical app
          3840 <= sic_code <= 3849 or # Surgical, medical, and dental instruments and supplies
          3850 <= sic_code <= 3851): # Ophthalmic goods
        return "MedEq"

    # 13 Drugs  Pharmaceutical Products
    elif (2830 <= sic_code <= 2830 or # Drugs
          2831 <= sic_code <= 2831 or # Biological products
          2833 <= sic_code <= 2833 or # Medicinal chemicals
          2834 <= sic_code <= 2834 or # Pharmaceutical preparations
          2835 <= sic_code <= 2835 or # In vitro, in vivo diagnostic substances
          2836 <= sic_code <= 2836): # Biological products, except diagnostic substances
        return "Drugs"

    # 14 Chems  Chemicals
    elif (2800 <= sic_code <= 2809 or # Chemicals and allied products
          2810 <= sic_code <= 2819 or # Industrial inorganic chemicals
          2820 <= sic_code <= 2829 or # Plastic material & synthetic resin/rubber
          2850 <= sic_code <= 2859 or # Paints
          2860 <= sic_code <= 2869 or # Industrial organic chemicals
          2870 <= sic_code <= 2879 or # Agriculture chemicals
          2890 <= sic_code <= 2899): # Misc chemical products
        return "Chems"

    # 15 Rubbr  Rubber and Plastic Products
    elif (3031 <= sic_code <= 3031 or # Reclaimed rubber
          3041 <= sic_code <= 3041 or # Rubber & plastic hose & belting
          3050 <= sic_code <= 3053 or # Gaskets, hoses, etc
          3060 <= sic_code <= 3069 or # Fabricated rubber products
          3070 <= sic_code <= 3079 or # Misc rubber products (?)
          3080 <= sic_code <= 3089 or # Misc plastic products
          3090 <= sic_code <= 3099): # Misc rubber and plastic products (?)
        return "Rubbr"

    # 16 Txtls  Textiles
    elif (2200 <= sic_code <= 2269 or # Textile mill products
          2270 <= sic_code <= 2279 or # Floor covering mills
          2280 <= sic_code <= 2284 or # Yarn and thread mills
          2290 <= sic_code <= 2295 or # Misc textile goods
          2297 <= sic_code <= 2297 or # Non-woven fabrics
          2298 <= sic_code <= 2298 or # Cordage and twine
          2299 <= sic_code <= 2299 or # Misc textile products
          2393 <= sic_code <= 2395 or # Textile bags, canvas products
          2397 <= sic_code <= 2399): # Misc textile products
        return "Txtls"

    # 17 BldMt  Construction Materials
    elif (800 <= sic_code <= 899 or # Forestry
          2400 <= sic_code <= 2439 or # Lumber and wood products
          2450 <= sic_code <= 2459 or # Wood buildings & mobile homes
          2490 <= sic_code <= 2499 or # Misc wood products
          2660 <= sic_code <= 2661 or # Building paper and board mills
          2950 <= sic_code <= 2952 or # Paving & roofing materials
          3200 <= sic_code <= 3200 or # Stone, clay, glass, concrete, etc
          3210 <= sic_code <= 3211 or # Flat glass
          3240 <= sic_code <= 3241 or # Cement, hydraulic
          3250 <= sic_code <= 3259 or # Structural clay products
          3261 <= sic_code <= 3261 or # Vitreous china plumbing fixtures
          3264 <= sic_code <= 3264 or # Porcelain electrical supplies
          3270 <= sic_code <= 3275 or # Concrete, gypsum & plaster products
          3280 <= sic_code <= 3281 or # Cut stone and stone products
          3290 <= sic_code <= 3293 or # Abrasive and asbestos products
          3295 <= sic_code <= 3299 or # Misc nonmetallic mineral products
          3420 <= sic_code <= 3429 or # Cutlery, hand tools and general hardware
          3430 <= sic_code <= 3433 or # Heating equipment & plumbing fixtures
          3440 <= sic_code <= 3441 or # Fabricated structural metal products
          3442 <= sic_code <= 3442 or # Metal doors, frames
          3446 <= sic_code <= 3446 or # Architectural or ornamental metal work
          3448 <= sic_code <= 3448 or # Prefabricated metal buildings and components
          3449 <= sic_code <= 3449 or # Misc structural metal work
          3450 <= sic_code <= 3451 or # Screw machine products
          3452 <= sic_code <= 3452 or # Bolts, nuts, screws, rivets and washers
          3490 <= sic_code <= 3499 or # Misc fabricated metal products
          3996 <= sic_code <= 3996): # Hard surface floor coverings
        return "BldMt"

    # 18 Cnstr  Construction
    elif (1500 <= sic_code <= 1511 or # Build construction - general contractors
          1520 <= sic_code <= 1529 or # General building contractors - residential
          1530 <= sic_code <= 1539 or # Operative builders
          1540 <= sic_code <= 1549 or # General building contractors - non-residential
          1600 <= sic_code <= 1699 or # Heavy construction - not building contractors
          1700 <= sic_code <= 1799): # Construction - special contractors
        return "Cnstr"

    # 19 Steel  Steel Works Etc
    elif (3300 <= sic_code <= 3300 or # Primary metal industries
          3310 <= sic_code <= 3317 or # Blast furnaces & steel works
          3320 <= sic_code <= 3325 or # Iron & steel foundries
          3330 <= sic_code <= 3339 or # Primary smelting & refining of nonferrous metals
          3340 <= sic_code <= 3341 or # Secondary smelting & refining of nonferrous metals
          3350 <= sic_code <= 3357 or # Rolling, drawing & extruding of nonferrous metals
          3360 <= sic_code <= 3369 or # Nonferrous foundries and casting
          3370 <= sic_code <= 3379 or # Steel works etc
          3390 <= sic_code <= 3399): # Misc primary metal products
        return "Steel"

    # 20 FabPr  Fabricated Products
    elif (3400 <= sic_code <= 3400 or # Fabricated metal, except machinery and trans eq
          3443 <= sic_code <= 3443 or # Fabricated plate work
          3444 <= sic_code <= 3444 or # Sheet metal work
          3460 <= sic_code <= 3469 or # Metal forgings and stampings
          3470 <= sic_code <= 3479): # Coating, engraving and allied services
        return "FabPr"

    # 21 Mach   Machinery
    elif (3510 <= sic_code <= 3519 or # Engines & turbines
          3520 <= sic_code <= 3529 or # Farm and garden machinery and equipment
          3530 <= sic_code <= 3530 or # Construction, mining & material handling machinery & equipment
          3531 <= sic_code <= 3531 or # Construction machinery & equipment
          3532 <= sic_code <= 3532 or # Mining machinery & equipment, except oil field
          3533 <= sic_code <= 3533 or # Oil & gas field machinery & equipment
          3534 <= sic_code <= 3534 or # Elevators & moving stairways
          3535 <= sic_code <= 3535 or # Conveyors & conveying equipment
          3536 <= sic_code <= 3536 or # Cranes, hoists and monorail systems
          3538 <= sic_code <= 3538 or # Machinery
          3540 <= sic_code <= 3549 or # Metalworking machinery & equipment
          3550 <= sic_code <= 3559 or # Special industry machinery
          3560 <= sic_code <= 3569 or # General industrial machinery & equipment
          3580 <= sic_code <= 3580 or # Refrigeration & service industry machinery
          3581 <= sic_code <= 3581 or # Automatic vending machines
          3582 <= sic_code <= 3582 or # Commercial laundry and dry cleaning machines
          3585 <= sic_code <= 3585 or # Air conditioning, warm air heating and refrigeration equipment
          3586 <= sic_code <= 3586 or # Measuring and dispensing pumps
          3589 <= sic_code <= 3589 or # Service industry machinery
          3590 <= sic_code <= 3599): # Misc industrial and commercial equipment and machinery
        return "Mach"

    # 22 ElcEq  Electrical Equipment
    elif (3600 <= sic_code <= 3600 or # Electronic & other electrical equipment
          3610 <= sic_code <= 3613 or # Electric transmission and distribution equipment
          3620 <= sic_code <= 3621 or # Electrical industrial apparatus
          3623 <= sic_code <= 3629 or # Electrical industrial apparatus
          3640 <= sic_code <= 3644 or # Electric lighting & wiring equipment
          3645 <= sic_code <= 3645 or # Residential electric lighting fixtures
          3646 <= sic_code <= 3646 or # Commercial, industrial and institutional electric lighting fixtures
          3648 <= sic_code <= 3649 or # Misc lighting equipment
          3660 <= sic_code <= 3660 or # Communications equipment
          3690 <= sic_code <= 3690 or # Misc electrical machinery and equipment
          3691 <= sic_code <= 3692 or # Storage batteries
          3699 <= sic_code <= 3699): # Misc electrical machinery, equipment and supplies
        return "ElcEq"

    # 23 Autos  Automobiles and Trucks
    elif (2296 <= sic_code <= 2296 or # Tire cord and fabric
          2396 <= sic_code <= 2396 or # Automotive trimmings, apparel findings & related products
          3010 <= sic_code <= 3011 or # Tires and inner tubes
          3537 <= sic_code <= 3537 or # Industrial trucks, tractors, trailers & stackers
          3647 <= sic_code <= 3647 or # Vehicular lighting equipment
          3694 <= sic_code <= 3694 or # Electrical equipment for internal combustion engines
          3700 <= sic_code <= 3700 or # Transportation equipment
          3710 <= sic_code <= 3710 or # Motor vehicles and motor vehicle equipment
          3711 <= sic_code <= 3711 or # Motor vehicles & passenger car bodies
          3713 <= sic_code <= 3713 or # Truck & bus bodies
          3714 <= sic_code <= 3714 or # Motor vehicle parts & accessories
          3715 <= sic_code <= 3715 or # Truck trailers
          3716 <= sic_code <= 3716 or # Motor homes
          3792 <= sic_code <= 3792 or # Travel trailers and campers
          3790 <= sic_code <= 3791 or # Misc transportation equipment
          3799 <= sic_code <= 3799): # Misc transportation equipment
        return "Autos"

    # 24 Aero   Aircraft
    elif (3720 <= sic_code <= 3720 or # Aircraft & parts
          3721 <= sic_code <= 3721 or # Aircraft
          3723 <= sic_code <= 3724 or # Aircraft engines & engine parts
          3725 <= sic_code <= 3725 or # Aircraft parts
          3728 <= sic_code <= 3729): # Misc aircraft parts & auxiliary equipment
        return "Aero"

    # 25 Ships  Shipbuilding, Railroad Equipment
    elif (3730 <= sic_code <= 3731 or # Ship building and repairing
          3740 <= sic_code <= 3743): # Railroad Equipment
        return "Ships"

    # 26 Guns   Defense
    elif (3760 <= sic_code <= 3769 or # Guided missiles and space vehicles and parts
          3795 <= sic_code <= 3795 or # Tanks and tank components
          3480 <= sic_code <= 3489): # Ordnance & accessories
        return "Guns"

    # 27 Gold   Precious Metals
    elif (1040 <= sic_code <= 1049): # Gold & silver ores
        return "Gold"

    # 28 Mines  Non-Metallic and Industrial Metal Mining
    elif (1000 <= sic_code <= 1009 or # Metal mining
          1010 <= sic_code <= 1019 or # Iron ores
          1020 <= sic_code <= 1029 or # Copper ores
          1030 <= sic_code <= 1039 or # Lead and zinc ores
          1050 <= sic_code <= 1059 or # Bauxite and other aluminum ores
          1060 <= sic_code <= 1069 or # Ferroalloy ores
          1070 <= sic_code <= 1079 or # Mining
          1080 <= sic_code <= 1089 or # Metal mining services
          1090 <= sic_code <= 1099 or # Misc metal ores
          1100 <= sic_code <= 1119 or # Anthracite mining
          1400 <= sic_code <= 1499): # Mining and quarrying nonmetallic minerals
        return "Mines"

    # 29 Coal   Coal
    elif (1200 <= sic_code <= 1299): # Bituminous coal and lignite mining
        return "Coal"

    # 30 Oil    Petroleum and Natural Gas
    elif (1300 <= sic_code <= 1300 or # Oil and gas extraction
          1310 <= sic_code <= 1319 or # Crude petroleum & natural gas
          1320 <= sic_code <= 1329 or # Natural gas liquids
          1330 <= sic_code <= 1339 or # Petroleum and natural gas
          1370 <= sic_code <= 1379 or # Petroleum and natural gas
          1380 <= sic_code <= 1380 or # Oil and gas field services
          1381 <= sic_code <= 1381 or # Drilling oil & gas wells
          1382 <= sic_code <= 1382 or # Oil & gas field exploration services
          1389 <= sic_code <= 1389 or # Misc oil & gas field services
          2900 <= sic_code <= 2912 or # Petroleum refining
          2990 <= sic_code <= 2999): # Misc products of petroleum & coal
        return "Oil"

    # 31 Util   Utilities
    elif (4900 <= sic_code <= 4900 or # Electric, gas & sanitary services
          4910 <= sic_code <= 4911 or # Electric services
          4920 <= sic_code <= 4922 or # Natural gas transmission
          4923 <= sic_code <= 4923 or # Natural gas transmission & distribution
          4924 <= sic_code <= 4925 or # Natural gas distribution
          4930 <= sic_code <= 4931 or # Electric and other services combined
          4932 <= sic_code <= 4932 or # Gas and other services combined
          4939 <= sic_code <= 4939 or # Misc combination utilities
          4940 <= sic_code <= 4942): # Water supply
        return "Util"

    # 32 Telcm  Communication
    elif (4800 <= sic_code <= 4800 or # Communications
          4810 <= sic_code <= 4813 or # Telephone communications
          4820 <= sic_code <= 4822 or # Telegraph and other message communication
          4830 <= sic_code <= 4839 or # Radio & TV broadcasters
          4840 <= sic_code <= 4841 or # Cable and other pay TV services
          4880 <= sic_code <= 4889 or # Communications
          4890 <= sic_code <= 4890 or # Communication services (Comsat)
          4891 <= sic_code <= 4891 or # Cable TV operators
          4892 <= sic_code <= 4892 or # Telephone interconnect
          4899 <= sic_code <= 4899): # Misc communication services
        return "Telcm"

    # 33 PerSv  Personal Services
    elif (7020 <= sic_code <= 7021 or # Rooming and boarding houses
          7030 <= sic_code <= 7033 or # Camps and recreational vehicle parks
          7200 <= sic_code <= 7200 or # Services - personal
          7210 <= sic_code <= 7212 or # Services - laundry, cleaning & garment services
          7214 <= sic_code <= 7214 or # Services - diaper service
          7215 <= sic_code <= 7216 or # Services - coin-operated cleaners, dry cleaners
          7217 <= sic_code <= 7217 or # Services - carpet & upholstery cleaning
          7219 <= sic_code <= 7219 or # Services - Misc laundry & garment services
          7220 <= sic_code <= 7221 or # Services - photographic studios, portrait
          7230 <= sic_code <= 7231 or # Services - beauty shops
          7240 <= sic_code <= 7241 or # Services - barber shops
          7250 <= sic_code <= 7251 or # Services - shoe repair shops & shoeshine parlors
          7260 <= sic_code <= 7269 or # Services - funeral service & crematories
          7270 <= sic_code <= 7290 or # Services – Misc
          7291 <= sic_code <= 7291 or # Services - tax return
          7292 <= sic_code <= 7299 or # Services - Misc
          7395 <= sic_code <= 7395 or # Services - photofinishing labs (School pictures)
          7500 <= sic_code <= 7500 or # Services - auto repair, services & parking
          7520 <= sic_code <= 7529 or # Services - automobile parking
          7530 <= sic_code <= 7539 or # Services - automotive repair shops
          7540 <= sic_code <= 7549 or # Services - automotive services, except repair (car washes)
          7600 <= sic_code <= 7600 or # Services - Misc repair services
          7620 <= sic_code <= 7620 or # Services - Electrical repair shops
          7622 <= sic_code <= 7622 or # Services - Radio and TV repair shops
          7623 <= sic_code <= 7623 or # Services - Refrigeration and air conditioning service & repair shops
          7629 <= sic_code <= 7629 or # Services - Electrical & electronic repair shops
          7630 <= sic_code <= 7631 or # Services - Watch, clock and jewelry repair
          7640 <= sic_code <= 7641 or # Services - Reupholster & furniture repair
          7690 <= sic_code <= 7699 or # Services - Misc repair shops & related services
          8100 <= sic_code <= 8199 or # Services - legal
          8200 <= sic_code <= 8299 or # Services - educational
          8300 <= sic_code <= 8399 or # Services - social services
          8400 <= sic_code <= 8499 or # Services - museums, art galleries, botanical and zoological gardens
          8600 <= sic_code <= 8699 or # Services - membership organizations
          8800 <= sic_code <= 8899 or # Services - private households
          7510 <= sic_code <= 7515): # Services - truck & auto rental and leasing
        return "PerSv"

    # 34 BusSv  Business Services
    elif (2750 <= sic_code <= 2759 or # Commercial printing
          3993 <= sic_code <= 3993 or # Signs & advertising specialties
          7218 <= sic_code <= 7218 or # Services - industrial launderers
          7300 <= sic_code <= 7300 or # Services - business services
          7310 <= sic_code <= 7319 or # Services - advertising
          7320 <= sic_code <= 7329 or # Services - consumer credit reporting agencies, collection services
          7330 <= sic_code <= 7339 or # Services - mailing, reproduction, commercial art & photography
          7340 <= sic_code <= 7342 or # Services - services to dwellings & other buildings
          7349 <= sic_code <= 7349 or # Services - building cleaning & maintenance
          7350 <= sic_code <= 7351 or # Services - Misc equipment rental and leasing
          7352 <= sic_code <= 7352 or # Services - medical equipment rental and leasing
          7353 <= sic_code <= 7353 or # Services - heavy construction equipment rental and leasing
          7359 <= sic_code <= 7359 or # Services - equipment rental and leasing
          7360 <= sic_code <= 7369 or # Services - personnel supply services
          7374 <= sic_code <= 7374 or # Services - computer processing, data preparation and processing
          7376 <= sic_code <= 7376 or # Services - computer facilities management service
          7377 <= sic_code <= 7377 or # Services - computer rental and leasing
          7378 <= sic_code <= 7378 or # Services - computer maintenance and repair
          7379 <= sic_code <= 7379 or # Services - computer related services
          7380 <= sic_code <= 7380 or # Services - Misc business services
          7381 <= sic_code <= 7382 or # Services - security
          7383 <= sic_code <= 7383 or # Services - news syndicates
          7384 <= sic_code <= 7384 or # Services - photofinishing labs
          7385 <= sic_code <= 7385 or # Services - telephone interconnect systems
          7389 <= sic_code <= 7390 or # Services - Misc business services
          7391 <= sic_code <= 7391 or # Services - R&D labs
          7392 <= sic_code <= 7392 or # Services - management consulting & P.R.
          7393 <= sic_code <= 7393 or # Services - detective and protective (ADT)
          7394 <= sic_code <= 7394 or # Services - equipment rental & leasing
          7396 <= sic_code <= 7396 or # Services - trading stamp services
          7397 <= sic_code <= 7397 or # Services - commercial testing labs
          7399 <= sic_code <= 7399 or # Services - business services
          7519 <= sic_code <= 7519 or # Services - utility trailer & recreational vehicle rental
          8700 <= sic_code <= 8700 or # Services - engineering, accounting, research, management
          8710 <= sic_code <= 8713 or # Services - engineering, accounting, surveying
          8720 <= sic_code <= 8721 or # Services - accounting, auditing, bookkeeping
          8730 <= sic_code <= 8734 or # Services - research, development, testing labs
          8740 <= sic_code <= 8748 or # Services - management, public relations, consulting
          8900 <= sic_code <= 8910 or # Services - Misc
          8911 <= sic_code <= 8911 or # Services - Misc engineering & architect
          8920 <= sic_code <= 8999 or # Services - Misc
          4220 <= sic_code <= 4229): # Public warehousing and storage
        return "BusSv"

    # 35 Hardw  Computers
    elif (3570 <= sic_code <= 3579 or # Computer & office equipment
          3680 <= sic_code <= 3680 or # Computers
          3681 <= sic_code <= 3681 or # Computers - mini
          3682 <= sic_code <= 3682 or # Computers - mainframe
          3683 <= sic_code <= 3683 or # Computers - terminals
          3684 <= sic_code <= 3684 or # Computers - disk & tape drives
          3685 <= sic_code <= 3685 or # Computers - optical scanners
          3686 <= sic_code <= 3686 or # Computers - graphics
          3687 <= sic_code <= 3687 or # Computers - office automation systems
          3688 <= sic_code <= 3688 or # Computers - peripherals
          3689 <= sic_code <= 3689 or # Computers - equipment
          3695 <= sic_code <= 3695): # Magnetic and optical recording media
        return "Hardw"

    # 36 Softw  Computer Software
    elif (7370 <= sic_code <= 7372 or # Services - computer programming and data processing
          7375 <= sic_code <= 7375 or # Services - information retrieval services
          7373 <= sic_code <= 7373): # Computer integrated systems design
        return "Softw"

    # 37 Chips  Electronic Equipment
    elif (3622 <= sic_code <= 3622 or # Industrial controls
          3661 <= sic_code <= 3661 or # Telephone and telegraph apparatus
          3662 <= sic_code <= 3662 or # Communications equipment
          3663 <= sic_code <= 3663 or # Radio & TV broadcasting & communications equipment
          3664 <= sic_code <= 3664 or # Search, navigation, guidance systems
          3665 <= sic_code <= 3665 or # Training equipment & simulators
          3666 <= sic_code <= 3666 or # Alarm & signaling products
          3669 <= sic_code <= 3669 or # Communication equipment
          3670 <= sic_code <= 3679 or # Electronic components & accessories
          3810 <= sic_code <= 3810 or # Search, detection, navigation, guidance, aeronautical & nautical systems, instruments & equipment
          3812 <= sic_code <= 3812): # Search, detection, navigation, guidance, aeronautical & nautical systems & instruments
        return "Chips"

    # 38 LabEq  Measuring and Control Equipment
    elif (3811 <= sic_code <= 3811 or # Engr laboratory and research equipment
          3820 <= sic_code <= 3820 or # Measuring and controlling equipment
          3821 <= sic_code <= 3821 or # Laboratory apparatus and furniture
          3822 <= sic_code <= 3822 or # Automatic controls for regulating residential & commercial environments & appliances
          3823 <= sic_code <= 3823 or # Industrial measurement instruments & related products
          3824 <= sic_code <= 3824 or # Totalizing fluid meters & counting devices
          3825 <= sic_code <= 3825 or # Instruments for measuring & testing of electricity & electrical instruments
          3826 <= sic_code <= 3826 or # Lab analytical instruments
          3827 <= sic_code <= 3827 or # Optical instruments and lenses
          3829 <= sic_code <= 3829 or # Misc measuring and controlling devices
          3830 <= sic_code <= 3839): # Optical instruments and lenses
        return "LabEq"

    # 39 Paper  Business Supplies
    elif (2520 <= sic_code <= 2549 or # Office furniture and fixtures
          2600 <= sic_code <= 2639 or # Paper and allied products
          2670 <= sic_code <= 2699 or # Paper and allied products
          2760 <= sic_code <= 2761 or # Manifold business forms
          3950 <= sic_code <= 3955): # Pens, pencils & other artists’ supplies
        return "Paper"

    # 40 Boxes  Shipping Containers
    elif (2440 <= sic_code <= 2449 or # Wood containers
          2640 <= sic_code <= 2659 or # Paperboard containers, boxes, drums, tubs
          3220 <= sic_code <= 3221 or # Glass containers
          3410 <= sic_code <= 3412): # Metal cans and shipping containers
        return "Boxes"

    # 41 Trans  Transportation
    elif (4000 <= sic_code <= 4013 or # Railroads, line-haul operating
          4040 <= sic_code <= 4049 or # Railway express service
          4100 <= sic_code <= 4100 or # Local & suburban transit & interurban highway passenger transportation
          4110 <= sic_code <= 4119 or # Local & suburban passenger transportation
          4120 <= sic_code <= 4121 or # Taxicabs
          4130 <= sic_code <= 4131 or # Intercity & rural bus transportation
          4140 <= sic_code <= 4142 or # Bus charter service
          4150 <= sic_code <= 4151 or # School buses
          4170 <= sic_code <= 4173 or # Motor vehicle terminals & service facilities
          4190 <= sic_code <= 4199 or # Misc transit and passenger transportation
          4200 <= sic_code <= 4200 or # Trucking & warehousing
          4210 <= sic_code <= 4219 or # Trucking & courier services, except air
          4230 <= sic_code <= 4231 or # Terminal & joint terminal maintenance
          4240 <= sic_code <= 4249 or # Transportation
          4400 <= sic_code <= 4499 or # Water transport
          4500 <= sic_code <= 4599 or # Air transportation
          4600 <= sic_code <= 4699 or # Pipelines, except natural gas
          4700 <= sic_code <= 4700 or # Transportation services
          4710 <= sic_code <= 4712 or # Freight forwarding
          4720 <= sic_code <= 4729 or # Arrangement of passenger transportation
          4730 <= sic_code <= 4739 or # Arrangement of transportation of freight and cargo
          4740 <= sic_code <= 4749 or # Rental of railroad cars
          4780 <= sic_code <= 4780 or # Misc services incidental to transportation
          4782 <= sic_code <= 4782 or # Inspection and weighing services
          4783 <= sic_code <= 4783 or # Packing and crating
          4784 <= sic_code <= 4784 or # Misc fixed facilities for vehicles
          4785 <= sic_code <= 4785 or # Motor vehicle inspection
          4789 <= sic_code <= 4789): # Misc transportation services
        return "Trans"

    # 42 Whlsl  Wholesale
    elif (5000 <= sic_code <= 5000 or # Wholesale - durable goods
          5010 <= sic_code <= 5015 or # Wholesale - automotive vehicles & automotive parts & supplies
          5020 <= sic_code <= 5023 or # Wholesale - furniture and home furnishings
          5030 <= sic_code <= 5039 or # Wholesale - lumber and construction materials
          5040 <= sic_code <= 5042 or # Wholesale - professional and commercial equipment and supplies
          5043 <= sic_code <= 5043 or # Wholesale - photographic equipment & supplies
          5044 <= sic_code <= 5044 or # Wholesale - office equipment
          5045 <= sic_code <= 5045 or # Wholesale - computers & peripheral equipment & software
          5046 <= sic_code <= 5046 or # Wholesale - commercial equipment
          5047 <= sic_code <= 5047 or # Wholesale - medical, dental & hospital equipment
          5048 <= sic_code <= 5048 or # Wholesale - ophthalmic goods
          5049 <= sic_code <= 5049 or # Wholesale - professional equipment and supplies
          5050 <= sic_code <= 5059 or # Wholesale - metals and minerals, except petroleum
          5060 <= sic_code <= 5060 or # Wholesale - electrical goods
          5063 <= sic_code <= 5063 or # Wholesale - electrical apparatus and equipment
          5064 <= sic_code <= 5064 or # Wholesale - electrical appliance, TV and radio sets
          5065 <= sic_code <= 5065 or # Wholesale - electronic parts & equipment
          5070 <= sic_code <= 5078 or # Wholesale - hardware, plumbing & heating equipment
          5080 <= sic_code <= 5080 or # Wholesale - machinery, equipment & supplies
          5081 <= sic_code <= 5081 or # Wholesale - machinery & equipment (?)
          5082 <= sic_code <= 5082 or # Wholesale - construction and mining machinery &equipment
          5083 <= sic_code <= 5083 or # Wholesale - farm and garden machinery & equipment
          5084 <= sic_code <= 5084 or # Wholesale - industrial machinery & equipment
          5085 <= sic_code <= 5085 or # Wholesale - industrial supplies
          5086 <= sic_code <= 5087 or # Wholesale - service establishment machinery & equipment (?)
          5088 <= sic_code <= 5088 or # Wholesale - transportation equipment, except motor vehicles
          5090 <= sic_code <= 5090 or # Wholesale - Misc durable goods
          5091 <= sic_code <= 5092 or # Wholesale - sporting goods & toys
          5093 <= sic_code <= 5093 or # Wholesale - scrap and waste materials
          5094 <= sic_code <= 5094 or # Wholesale - jewelry, watches, precious stones & metals
          5099 <= sic_code <= 5099 or # Wholesale - durable goods
          5100 <= sic_code <= 5100 or # Wholesale - nondurable goods
          5110 <= sic_code <= 5113 or # Wholesale - paper and paper products
          5120 <= sic_code <= 5122 or # Wholesale - drugs & drug proprietaries
          5130 <= sic_code <= 5139 or # Wholesale - apparel, piece goods & notions
          5140 <= sic_code <= 5149 or # Wholesale - groceries & related products
          5150 <= sic_code <= 5159 or # Wholesale - farm product raw materials
          5160 <= sic_code <= 5169 or # Wholesale - chemicals & allied products
          5170 <= sic_code <= 5172 or # Wholesale - petroleum and petroleum products
          5180 <= sic_code <= 5182 or # Wholesale - beer, wine & distilled alcoholic beverages
          5190 <= sic_code <= 5199): # Wholesale - Misc nondurable goods
        return "Whlsl"

    # 43 Rtail  Retail
    elif (5200 <= sic_code <= 5200 or # Retail - retail-building materials, hardware, garden supply
          5210 <= sic_code <= 5219 or # Retail - lumber & other building materials
          5220 <= sic_code <= 5229 or # Retail
          5230 <= sic_code <= 5231 or # Retail - paint, glass & wallpaper stores
          5250 <= sic_code <= 5251 or # Retail - hardware stores
          5260 <= sic_code <= 5261 or # Retail - nurseries, lawn & garden supply stores
          5270 <= sic_code <= 5271 or # Retail - mobile home dealers
          5300 <= sic_code <= 5300 or # Retail - general merchandise stores
          5310 <= sic_code <= 5311 or # Retail - department stores
          5320 <= sic_code <= 5320 or # Retail - general merchandise stores (?)
          5330 <= sic_code <= 5331 or # Retail - variety stores
          5334 <= sic_code <= 5334 or # Retail - catalog showroom
          5340 <= sic_code <= 5349 or # Retail
          5390 <= sic_code <= 5399 or # Retail - Misc general merchandise stores
          5400 <= sic_code <= 5400 or # Retail - food stores
          5410 <= sic_code <= 5411 or # Retail - grocery stores
          5412 <= sic_code <= 5412 or # Retail - convenience stores
          5420 <= sic_code <= 5429 or # Retail - meat & fish markets
          5430 <= sic_code <= 5439 or # Retail - fruit and vegetable markets
          5440 <= sic_code <= 5449 or # Retail - candy, nut & confectionary stores
          5450 <= sic_code <= 5459 or # Retail - dairy products stores
          5460 <= sic_code <= 5469 or # Retail - bakeries
          5490 <= sic_code <= 5499 or # Retail - Misc food stores
          5500 <= sic_code <= 5500 or # Retail - automotive dealers and gas stations
          5510 <= sic_code <= 5529 or # Retail - automotive dealers
          5530 <= sic_code <= 5539 or # Retail - automotive and home supply stores
          5540 <= sic_code <= 5549 or # Retail - gasoline service stations
          5550 <= sic_code <= 5559 or # Retail - boat dealers
          5560 <= sic_code <= 5569 or # Retail - recreation vehicle dealers
          5570 <= sic_code <= 5579 or # Retail - motorcycle dealers
          5590 <= sic_code <= 5599 or # Retail - automotive dealers
          5600 <= sic_code <= 5699 or # Retail - apparel & accessory stores
          5700 <= sic_code <= 5700 or # Retail - home furniture and equipment stores
          5710 <= sic_code <= 5719 or # Retail - home furnishings stores
          5720 <= sic_code <= 5722 or # Retail - household appliance stores
          5730 <= sic_code <= 5733 or # Retail - radio, TV and consumer electronic stores
          5734 <= sic_code <= 5734 or # Retail - computer and computer software stores
          5735 <= sic_code <= 5735 or # Retail - record and tape stores
          5736 <= sic_code <= 5736 or # Retail - musical instrument stores
          5750 <= sic_code <= 5799 or # Retail
          5900 <= sic_code <= 5900 or # Retail - Misc
          5910 <= sic_code <= 5912 or # Retail - drug & proprietary stores
          5920 <= sic_code <= 5929 or # Retail - liquor stores
          5930 <= sic_code <= 5932 or # Retail - used merchandise stores
          5940 <= sic_code <= 5940 or # Retail - Misc
          5941 <= sic_code <= 5941 or # Retail - sporting goods stores & bike shops
          5942 <= sic_code <= 5942 or # Retail - book stores
          5943 <= sic_code <= 5943 or # Retail - stationery stores
          5944 <= sic_code <= 5944 or # Retail - jewelry stores
          5945 <= sic_code <= 5945 or # Retail - hobby, toy and game shops
          5946 <= sic_code <= 5946 or # Retail - camera and photographic supply stores
          5947 <= sic_code <= 5947 or # Retail - gift, novelty & souvenir shops
          5948 <= sic_code <= 5948 or # Retail - luggage & leather goods stores
          5949 <= sic_code <= 5949 or # Retail - sewing & needlework stores
          5950 <= sic_code <= 5959 or # Retail
          5960 <= sic_code <= 5969 or # Retail - non-store retailers (catalogs, etc)
          5970 <= sic_code <= 5979 or # Retail
          5980 <= sic_code <= 5989 or # Retail - fuel dealers & ice stores
          5990 <= sic_code <= 5990 or # Retail - Misc retail stores
          5992 <= sic_code <= 5992 or # Retail - florists
          5993 <= sic_code <= 5993 or # Retail - tobacco stores and stands
          5994 <= sic_code <= 5994 or # Retail - newsdealers and news stands
          5995 <= sic_code <= 5995 or # Retail - optical goods stores
          5999 <= sic_code <= 5999): # Misc retail stores
        return "Rtail"

    # 44 Meals  Restaurants, Hotels, Motels
    elif (5800 <= sic_code <= 5819 or # Retail - eating places
          5820 <= sic_code <= 5829 or # Restaurants, hotels, motels
          5890 <= sic_code <= 5899 or # Eating and drinking places
          7000 <= sic_code <= 7000 or # Hotels & other lodging places
          7010 <= sic_code <= 7019 or # Hotels & motels
          7040 <= sic_code <= 7049 or # Membership hotels and lodging houses
          7213 <= sic_code <= 7213): # Services - linen supply
        return "Meals"

    # 45 Banks  Banking
    elif (6000 <= sic_code <= 6000 or # Depository institutions
          6010 <= sic_code <= 6019 or # Federal reserve banks
          6020 <= sic_code <= 6020 or # Commercial banks
          6021 <= sic_code <= 6021 or # National commercial banks
          6022 <= sic_code <= 6022 or # State commercial banks - Fed Res System
          6023 <= sic_code <= 6024 or # State commercial banks - not Fed Res System
          6025 <= sic_code <= 6025 or # National commercial banks - Fed Res System
          6026 <= sic_code <= 6026 or # National commercial banks - not Fed Res System
          6027 <= sic_code <= 6027 or # National commercial banks, not FDIC
          6028 <= sic_code <= 6029 or # Misc commercial banks
          6030 <= sic_code <= 6036 or # Savings institutions
          6040 <= sic_code <= 6059 or # Banks (?)
          6060 <= sic_code <= 6062 or # Credit unions
          6080 <= sic_code <= 6082 or # Foreign banks
          6090 <= sic_code <= 6099 or # Functions related to depository banking
          6100 <= sic_code <= 6100 or # Non-depository credit institutions
          6110 <= sic_code <= 6111 or # Federal credit agencies
          6112 <= sic_code <= 6113 or # FNMA
          6120 <= sic_code <= 6129 or # S&Ls
          6130 <= sic_code <= 6139 or # Agricultural credit institutions
          6140 <= sic_code <= 6149 or # Personal credit institutions
          6150 <= sic_code <= 6159 or # Business credit institutions
          6160 <= sic_code <= 6169 or # Mortgage bankers and brokers
          6170 <= sic_code <= 6179 or # Finance lessors
          6190 <= sic_code <= 6199): # Financial services
        return "Banks"

    # 46 Insur  Insurance
    elif (6300 <= sic_code <= 6300 or # Insurance
          6310 <= sic_code <= 6319 or # Life insurance
          6320 <= sic_code <= 6329 or # Accident and health insurance
          6330 <= sic_code <= 6331 or # Fire, marine & casualty insurance
          6350 <= sic_code <= 6351 or # Surety insurance
          6360 <= sic_code <= 6361 or # Title insurance
          6370 <= sic_code <= 6379 or # Pension, health & welfare funds
          6390 <= sic_code <= 6399 or # Misc insurance carriers
          6400 <= sic_code <= 6411): # Insurance agents, brokers & service
        return "Insur"

    # 47 RlEst  Real Estate
    elif (6500 <= sic_code <= 6500 or # Real estate
          6510 <= sic_code <= 6510 or # Real estate operators and lessors
          6512 <= sic_code <= 6512 or # Operators - non-resident buildings
          6513 <= sic_code <= 6513 or # Operators - apartment buildings
          6514 <= sic_code <= 6514 or # Operators - other than apartment
          6515 <= sic_code <= 6515 or # Operators - residential mobile home
          6517 <= sic_code <= 6519 or # Lessors of railroad & real property
          6520 <= sic_code <= 6529 or # Real estate
          6530 <= sic_code <= 6531 or # Real estate agents and managers
          6532 <= sic_code <= 6532 or # Real estate dealers
          6540 <= sic_code <= 6541 or # Title abstract offices
          6550 <= sic_code <= 6553 or # Land subdividers & developers
          6590 <= sic_code <= 6599 or # Real estate
          6610 <= sic_code <= 6611): # Combined real estate, insurance, etc
        return "RlEst"

    # 48 Fin    Trading
    elif (6200 <= sic_code <= 6299 or # Security and commodity brokers, dealers, exchanges & services
          6700 <= sic_code <= 6700 or # Holding & other investment offices
          6710 <= sic_code <= 6719 or # Holding offices
          6720 <= sic_code <= 6722 or # Management investment offices, open-end
          6723 <= sic_code <= 6723 or # Management investment offices, closed-end
          6724 <= sic_code <= 6724 or # Unit investment trusts
          6725 <= sic_code <= 6725 or # Face-amount certificate offices
          6726 <= sic_code <= 6726 or # Unit investment trusts, closed-end
          6730 <= sic_code <= 6733 or # Trusts
          6740 <= sic_code <= 6779 or # Investment offices
          6790 <= sic_code <= 6791 or # Misc investing
          6792 <= sic_code <= 6792 or # Oil royalty traders
          6793 <= sic_code <= 6793 or # Commodity traders
          6794 <= sic_code <= 6794 or # Patent owners & lessors
          6795 <= sic_code <= 6795 or # Mineral royalty traders
          6798 <= sic_code <= 6798 or # REIT
          6799 <= sic_code <= 6799): # Investors, NEC
        return "Fin"

    # 49 Other  Almost Nothing
    elif (4950 <= sic_code <= 4959 or # Sanitary services
          4960 <= sic_code <= 4961 or # Steam & air conditioning supplies
          4970 <= sic_code <= 4971 or # Irrigation systems
          4990 <= sic_code <= 4991): # Cogeneration - SM power producer
        return "Other"

    # Unclassified
    else:
        return "Unclassified"


def assign_industry(df: pd.DataFrame, industries: int) -> None:
    """
    Assigns an industry to each company in the dataframe based on the SIC code.

    Args:
        df (pd.DataFrame): dataframe with the sic column
        industries (int): number of industries

    Returns:
        None
    """
    if industries == 5:
        df["industry"] = df["sic"].apply(lambda x: sic_to_industry_five(x))
    elif industries == 10:
        df["industry"] = df["sic"].apply(lambda x: sic_to_industry_ten(x))
    elif industries == 12:
        df["industry"] = df["sic"].apply(lambda x: sic_to_industry_twelve(x))
    elif industries == 17:
        df["industry"] = df["sic"].apply(lambda x: sic_to_industry_seventeen(x))
    elif industries == 30:
        df["industry"] = df["sic"].apply(lambda x: sic_to_industry_thirty(x))
    elif industries == 38:
        df["industry"] = df["sic"].apply(lambda x: sic_to_industry_thirty_eight(x))
    elif industries == 48:
        df["industry"] = df["sic"].apply(lambda x: sic_to_industry_forty_eight(x))
    elif industries == 49:
        df["industry"] = df["sic"].apply(lambda x: sic_to_industry_fourty_nine(x))
    else:
        raise ValueError("Invalid number of industries")
    
