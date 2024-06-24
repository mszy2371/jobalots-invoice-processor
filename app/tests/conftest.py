import pytest


@pytest.fixture(scope="session")
def invoice_str_and_list():
    return (
        " \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \nJobalots\nUnits 11-13 Thomas Court / Pembroke Dock WLS\nSA72 4RZ / United Kingdom\n01646216123\njobalots.com - support@jobalots.com\nVAT numbers:\xa0\nUK - GB132656618, FR - FR64841743966, IT - IT00217299999,\xa0\nDE - DE319729384, CZ - CZ684550142, PL - PL5263222338, ES - ESN6060063B\xa0\nCompany number: 08031626\nORDER DATE : 2024-05-21\nINVOICE JL278024\nTITLE\nSKU\nQTY\nTAX\nPRICE\nJobalots auction\n59 x Brand New Mixed Home & Kitchen - RRP £352.41-4317670-\n3296332\nspIlV11iMMR\n1\n20%\n£ 8.00\nJobalots auction\n19 x Brand New Mixed Toys & Games - RRP £141.96-4317727-\n3296369\nspW73n5369e\n1\n20%\n£ 9.30\nJobalots auction\n15 x Brand New Mixed Home & Kitchen - RRP £90.84-4319024-\n3297418\nspW74u8077Q\n1\n20%\n£ 3.20\nJobalots auction\n40 x Brand New Mixed Home & Kitchen - RRP £425.46-4320708-\n3298834\nspIna13cyjJ\n1\n20%\n£ 24.00\nJobalots auction\n3 x Brand New Aiiwer 10 Set Packing Cubes for Suitcases, Travel\nEssentials Suitcase Organizers Bag for Carry on, Travel Organizer\nBags for Luggage, Travel Cubes Packing Cubes for Carry on Gr-\n4323700-3301112\nspW74y5654j\n1\n20%\n£ 2.10\nJobalots auction\n2 x Brand New ZCOINS 4 Bundles Hanging Plants ArtiĆcial Flowers\nPlants Outdoor Indoor, UV Resistant Fake Haning Admiralty Willow,\nFaux Plastic Flowers Plants for Home Garden Decorations- Gr-\n4323794-3301201\nspW72I5756s\n1\n20%\n£ 4.00\nJobalots auction\n5 x Brand New ilauke 60 Pack Non-slip Brown Tubular Children s\nHangers with 5 Hanger Chains for Kids Baby Toddler with Plastic\nHanger Straps, Kids Hangers Perfect for Better Organisation Max-\n4326371-3303910\nspSJL31jrL5\n1\n20%\n£ 5.21\nSHIPPING\n \nDETAILS\nJohn Doe\n190 Oxford Street\nLondon\nEngland\nW1D 1NR\nUnited\n \nKingdom\n07512 345678\nBILLING\n \nDETAILS\nJohn\n \nDoe\n190 Oxford Street\nLondon\nEngland\nW1D 1NR\nUnited\n \nKingdom\n07512 345678\nCUSTOMER\n \nDETAILS\nJohn Doe \njohndoe@example.com\nDISCOUNT :\n- £ 2.32\nSUB TOTAL :\n£ 55.81\nSHIPPING :\n£ 30.99\nGB VAT (20%) :\n£ 16.89\nTOTAL :\n£ 101.37\nThank you for shopping with Jobalots!\n",
        [
            [
                "Jobalots auction\n59 x Brand New Mixed Home & Kitchen - RRP £352.41-4317670-\n3296332",
                "spIlV11iMMR",
                "1",
                "20%",
                "£ 8.00",
            ],
            [
                "Jobalots auction\n19 x Brand New Mixed Toys & Games - RRP £141.96-4317727-\n3296369",
                "spW73n5369e",
                "1",
                "20%",
                "£ 9.30",
            ],
            [
                "Jobalots auction\n15 x Brand New Mixed Home & Kitchen - RRP £90.84-4319024-\n3297418",
                "spW74u8077Q",
                "1",
                "20%",
                "£ 3.20",
            ],
            [
                "Jobalots auction\n40 x Brand New Mixed Home & Kitchen - RRP £425.46-4320708-\n3298834",
                "spIna13cyjJ",
                "1",
                "20%",
                "£ 24.00",
            ],
            [
                "Jobalots auction\n3 x Brand New Aiiwer 10 Set Packing Cubes for Suitcases, Travel\nEssentials Suitcase Organizers Bag for Carry on, Travel Organizer\nBags for Luggage, Travel Cubes Packing Cubes for Carry on Gr-\n4323700-3301112",
                "spW74y5654j",
                "1",
                "20%",
                "£ 2.10",
            ],
            [
                "Jobalots auction\n2 x Brand New ZCOINS 4 Bundles Hanging Plants ArtiĆcial Flowers\nPlants Outdoor Indoor, UV Resistant Fake Haning Admiralty Willow,\nFaux Plastic Flowers Plants for Home Garden Decorations- Gr-\n4323794-3301201",
                "spW72I5756s",
                "1",
                "20%",
                "£ 4.00",
            ],
            [
                "Jobalots auction\n5 x Brand New ilauke 60 Pack Non-slip Brown Tubular Children s\nHangers with 5 Hanger Chains for Kids Baby Toddler with Plastic\nHanger Straps, Kids Hangers Perfect for Better Organisation Max-\n4326371-3303910",
                "spSJL31jrL5",
                "1",
                "20%",
                "£ 5.21",
            ],
        ],
    )