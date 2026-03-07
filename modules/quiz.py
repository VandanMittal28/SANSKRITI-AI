"""
Quiz module for heritage knowledge testing.
"""
QUIZ_DATA = {
    "Taj Mahal": [
        {
            "question": "Who commissioned the Taj Mahal?",
            "options": ["A. Akbar", "B. Shah Jahan", "C. Humayun", "D. Aurangzeb"],
            "answer": "B. Shah Jahan",
            "explanation": "Shah Jahan built the Taj Mahal in memory of his beloved wife Mumtaz Mahal.",
        },
        {
            "question": "In which city is the Taj Mahal located?",
            "options": ["A. Delhi", "B. Jaipur", "C. Agra", "D. Lucknow"],
            "answer": "C. Agra",
            "explanation": "The Taj Mahal is located in Agra, Uttar Pradesh, on the banks of the Yamuna river.",
        },
        {
            "question": "What material was primarily used to build the Taj Mahal?",
            "options": ["A. Red Sandstone", "B. Granite", "C. Limestone", "D. White Marble"],
            "answer": "D. White Marble",
            "explanation": "The Taj Mahal was built using white Makrana marble from Rajasthan.",
        },
        {
            "question": "When was the Taj Mahal designated a UNESCO World Heritage Site?",
            "options": ["A. 1972", "B. 1983", "C. 1991", "D. 2000"],
            "answer": "B. 1983",
            "explanation": "The Taj Mahal was inscribed as a UNESCO World Heritage Site in 1983.",
        },
        {
            "question": "How many minarets does the Taj Mahal have?",
            "options": ["A. 2", "B. 6", "C. 4", "D. 8"],
            "answer": "C. 4",
            "explanation": "The Taj Mahal has four minarets, one at each corner of the plinth, slightly tilted outward.",
        },
    ],
    "Red Fort": [
        {
            "question": "Who built the Red Fort?",
            "options": ["A. Akbar", "B. Humayun", "C. Shah Jahan", "D. Babur"],
            "answer": "C. Shah Jahan",
            "explanation": "Shah Jahan built the Red Fort in 1638 when he shifted the Mughal capital from Agra to Delhi.",
        },
        {
            "question": "What is the Red Fort also known as?",
            "options": ["A. Lal Qila", "B. Qila-i-Mubarak", "C. Both A and B", "D. Agra Fort"],
            "answer": "C. Both A and B",
            "explanation": "Red Fort is called Lal Qila in Hindi and was originally named Qila-i-Mubarak (The Blessed Fort).",
        },
        {
            "question": "What happens at the Red Fort every Independence Day?",
            "options": [
                "A. Cultural festival",
                "B. Prime Minister hoists the national flag",
                "C. Military parade",
                "D. Fireworks display",
            ],
            "answer": "B. Prime Minister hoists the national flag",
            "explanation": "India's Prime Minister hoists the national flag at the Red Fort every Independence Day (August 15).",
        },
        {
            "question": "How many acres does the Red Fort complex cover?",
            "options": ["A. 100 acres", "B. 254 acres", "C. 500 acres", "D. 1000 acres"],
            "answer": "B. 254 acres",
            "explanation": "The Red Fort complex spans 254 acres and served as the main residence of Mughal emperors.",
        },
        {
            "question": "What famous diamond was once kept in the Red Fort?",
            "options": ["A. Hope Diamond", "B. Kohinoor", "C. Cullinan", "D. Orlov"],
            "answer": "B. Kohinoor",
            "explanation": "The famous Kohinoor diamond was once kept in the Red Fort before being taken to Britain.",
        },
    ],
    "Qutub Minar": [
        {
            "question": "Who started the construction of Qutub Minar?",
            "options": [
                "A. Iltutmish",
                "B. Qutb ud-Din Aibak",
                "C. Alauddin Khilji",
                "D. Razia Sultana",
            ],
            "answer": "B. Qutb ud-Din Aibak",
            "explanation": "Qutb ud-Din Aibak started building Qutub Minar in 1193, and it was completed by Iltutmish.",
        },
        {
            "question": "How tall is the Qutub Minar?",
            "options": ["A. 50 meters", "B. 65 meters", "C. 72.5 meters", "D. 80 meters"],
            "answer": "C. 72.5 meters",
            "explanation": "The Qutub Minar stands 72.5 meters tall and is the tallest brick minaret in the world.",
        },
        {
            "question": "What is special about the Iron Pillar near Qutub Minar?",
            "options": [
                "A. It's the tallest pillar",
                "B. It has stood for 1600 years without rusting",
                "C. It's made of gold",
                "D. It rotates",
            ],
            "answer": "B. It has stood for 1600 years without rusting",
            "explanation": "The Iron Pillar is a metallurgical marvel — 1600 years old and still rust-free.",
        },
        {
            "question": "How many storeys does the Qutub Minar have?",
            "options": ["A. 3", "B. 4", "C. 5", "D. 6"],
            "answer": "C. 5",
            "explanation": "The Qutub Minar has 5 distinct storeys, each with a projecting balcony.",
        },
        {
            "question": "What was the Qutub Minar built to mark?",
            "options": [
                "A. Victory in battle",
                "B. Beginning of Muslim rule in India",
                "C. Birth of an emperor",
                "D. End of a dynasty",
            ],
            "answer": "B. Beginning of Muslim rule in India",
            "explanation": "Qutub Minar was built to mark the beginning of Muslim rule in India and the Delhi Sultanate.",
        },
    ],
    "Hawa Mahal": [
        {
            "question": "What does 'Hawa Mahal' mean?",
            "options": [
                "A. Palace of Winds",
                "B. Palace of Mirrors",
                "C. Palace of Flowers",
                "D. Palace of Light",
            ],
            "answer": "A. Palace of Winds",
            "explanation": "Hawa Mahal means 'Palace of Winds' in Hindi, named for its 953 windows that allow cool air circulation.",
        },
        {
            "question": "Who built the Hawa Mahal?",
            "options": [
                "A. Maharaja Sawai Pratap Singh",
                "B. Maharaja Jai Singh II",
                "C. Maharaja Man Singh I",
                "D. Maharaja Ram Singh",
            ],
            "answer": "A. Maharaja Sawai Pratap Singh",
            "explanation": "Hawa Mahal was built by Maharaja Sawai Pratap Singh of Jaipur in 1799.",
        },
        {
            "question": "How many windows (jharokhas) does Hawa Mahal have?",
            "options": ["A. 500", "B. 750", "C. 953", "D. 1200"],
            "answer": "C. 953",
            "explanation": "Hawa Mahal has 953 small windows (jharokhas) decorated with intricate latticework.",
        },
        {
            "question": "Why was Hawa Mahal built?",
            "options": [
                "A. As a royal residence",
                "B. For royal ladies to observe festivals without being seen",
                "C. As a military fort",
                "D. As a temple",
            ],
            "answer": "B. For royal ladies to observe festivals without being seen",
            "explanation": "Hawa Mahal was built so royal ladies could observe street festivals and daily life without being seen, respecting the purdah system.",
        },
        {
            "question": "What architectural style is Hawa Mahal?",
            "options": [
                "A. Mughal only",
                "B. Rajput only",
                "C. Rajput with Islamic and Mughal influences",
                "D. British colonial",
            ],
            "answer": "C. Rajput with Islamic and Mughal influences",
            "explanation": "Hawa Mahal features Rajput architecture with Islamic and Mughal influences, built with red and pink sandstone.",
        },
    ],
    "India Gate": [
        {
            "question": "What is India Gate originally called?",
            "options": [
                "A. War Memorial",
                "B. All India War Memorial",
                "C. Victory Arch",
                "D. National Monument",
            ],
            "answer": "B. All India War Memorial",
            "explanation": "India Gate was originally called the All India War Memorial, built to commemorate Indian soldiers.",
        },
        {
            "question": "Who designed India Gate?",
            "options": [
                "A. Edwin Lutyens",
                "B. Le Corbusier",
                "C. Charles Correa",
                "D. Laurie Baker",
            ],
            "answer": "A. Edwin Lutyens",
            "explanation": "India Gate was designed by British architect Sir Edwin Lutyens and built between 1921-1931.",
        },
        {
            "question": "How many soldiers' names are inscribed on India Gate?",
            "options": ["A. 7,000", "B. 10,000", "C. 13,300", "D. 20,000"],
            "answer": "C. 13,300",
            "explanation": "Over 13,300 names of British Indian soldiers who died in World War I are inscribed on India Gate.",
        },
        {
            "question": "What does India Gate commemorate?",
            "options": [
                "A. Independence Day",
                "B. 70,000 Indian soldiers who died in World War I",
                "C. Republic Day",
                "D. Victory in World War II",
            ],
            "answer": "B. 70,000 Indian soldiers who died in World War I",
            "explanation": "India Gate commemorates 70,000 Indian soldiers who died fighting for the British Empire in World War I.",
        },
        {
            "question": "What is India Gate's height?",
            "options": ["A. 30 meters", "B. 42 meters", "C. 50 meters", "D. 60 meters"],
            "answer": "B. 42 meters",
            "explanation": "India Gate stands 42 meters tall and is built in the neoclassical triumphal arch style.",
        },
    ],
}


def get_quiz_questions(monument_name: str) -> list[dict] | None:
    """
    Get quiz questions for a specific monument.
    Returns list of question dicts if found, None otherwise.
    """
    return QUIZ_DATA.get(monument_name)

# ── New monuments added for hackathon expansion ──────────────────────────────

QUIZ_DATA["Hampi"] = [
    {
        "question": "Which empire made Hampi its capital?",
        "options": [
            "A. Maurya Empire",
            "B. Vijayanagara Empire",
            "C. Mughal Empire",
            "D. Chola Empire",
        ],
        "answer": "B. Vijayanagara Empire",
        "explanation": "Hampi served as the capital of the Vijayanagara Empire from 1336 to 1646, one of the greatest South Indian empires.",
    },
    {
        "question": "What is the famous landmark at Vittala Temple in Hampi?",
        "options": [
            "A. The Dancing Hall",
            "B. The Stone Chariot",
            "C. The Golden Dome",
            "D. The Iron Pillar",
        ],
        "answer": "B. The Stone Chariot",
        "explanation": "The Stone Chariot at Vittala Temple is a masterpiece of Vijayanagara architecture and appears on the Indian 50-rupee note.",
    },
    {
        "question": "Which river flows through the Hampi ruins?",
        "options": ["A. Krishna", "B. Kaveri", "C. Tungabhadra", "D. Godavari"],
        "answer": "C. Tungabhadra",
        "explanation": "The Tungabhadra River flows through Hampi, considered sacred and central to the city's layout and rituals.",
    },
    {
        "question": "In which year was Hampi sacked and destroyed?",
        "options": ["A. 1498", "B. 1526", "C. 1565", "D. 1600"],
        "answer": "C. 1565",
        "explanation": "Hampi was sacked in 1565 by a coalition of five Deccan Sultanates after the Battle of Talikota, ending Vijayanagara's glory.",
    },
    {
        "question": "How many surviving monuments does Hampi contain?",
        "options": ["A. 200+", "B. 600+", "C. 1,600+", "D. 3,000+"],
        "answer": "C. 1,600+",
        "explanation": "Hampi has over 1,600 surviving monuments spread across 26 sq km, making it one of the largest archaeological sites in the world.",
    },
]

QUIZ_DATA["Konark Sun Temple"] = [
    {
        "question": "Who built the Konark Sun Temple?",
        "options": [
            "A. Ashoka",
            "B. King Narasimhadeva I",
            "C. Prataparudra II",
            "D. Kanishka",
        ],
        "answer": "B. King Narasimhadeva I",
        "explanation": "King Narasimhadeva I of the Eastern Ganga dynasty built the Konark Sun Temple around 1250 CE.",
    },
    {
        "question": "What unique function do the 24 stone wheels of Konark serve?",
        "options": [
            "A. Religious prayer wheels",
            "B. Decorative carvings only",
            "C. Accurate sundials telling time",
            "D. Astronomical calendars",
        ],
        "answer": "C. Accurate sundials telling time",
        "explanation": "The 24 stone chariot wheels function as sundials that can accurately tell the time of day to the minute using shadow positions.",
    },
    {
        "question": "What nickname did European sailors give to Konark Sun Temple?",
        "options": [
            "A. White Pagoda",
            "B. Black Pagoda",
            "C. Golden Temple",
            "D. Stone Lighthouse",
        ],
        "answer": "B. Black Pagoda",
        "explanation": "European sailors called it the 'Black Pagoda' because it appeared dark against the horizon and helped them navigate along the Odisha coast.",
    },
    {
        "question": "The Konark Sun Temple is dedicated to which Hindu deity?",
        "options": ["A. Vishnu", "B. Shiva", "C. Surya", "D. Brahma"],
        "answer": "C. Surya",
        "explanation": "Konark Sun Temple is dedicated to Surya, the Sun God. The entire structure represents his divine chariot moving across the sky.",
    },
    {
        "question": "Which annual event is celebrated at Konark?",
        "options": [
            "A. Konark Music Festival",
            "B. Konark Dance Festival",
            "C. Konark Heritage Fair",
            "D. Konark Light Show",
        ],
        "answer": "B. Konark Dance Festival",
        "explanation": "The Konark Dance Festival is held every December against the backdrop of the Sun Temple, celebrating classical Indian dance forms.",
    },
]

QUIZ_DATA["Ajanta Caves"] = [
    {
        "question": "How many rock-cut caves does Ajanta comprise?",
        "options": ["A. 12", "B. 20", "C. 30", "D. 45"],
        "answer": "C. 30",
        "explanation": "Ajanta has 30 rock-cut Buddhist caves carved into basalt cliffs, created over several centuries.",
    },
    {
        "question": "Who rediscovered the Ajanta Caves in 1819?",
        "options": [
            "A. Lord Curzon",
            "B. John Smith",
            "C. James Fergusson",
            "D. Alexander Cunningham",
        ],
        "answer": "B. John Smith",
        "explanation": "British officer John Smith rediscovered Ajanta in 1819 while on a tiger-hunting expedition in the Sahyadri hills.",
    },
    {
        "question": "What religion do the Ajanta Cave monuments primarily represent?",
        "options": ["A. Hinduism", "B. Jainism", "C. Buddhism", "D. Zoroastrianism"],
        "answer": "C. Buddhism",
        "explanation": "Ajanta Caves are entirely Buddhist monuments featuring chaitya halls (prayer halls) and viharas (monasteries) with scenes from Buddha's life.",
    },
    {
        "question": "What makes the Ajanta paintings extraordinary?",
        "options": [
            "A. Painted using gold leaf",
            "B. Survived 1,500+ years using natural pigments",
            "C. Painted by foreign artists",
            "D. Use fluorescent colours",
        ],
        "answer": "B. Survived 1,500+ years using natural pigments",
        "explanation": "The Ajanta murals were created using natural minerals, plants, and earth pigments and have remarkably survived over 1,500 years.",
    },
    {
        "question": "For approximately how long were the Ajanta Caves forgotten before rediscovery?",
        "options": ["A. 200 years", "B. 500 years", "C. 1,000 years", "D. 1,500 years"],
        "answer": "C. 1,000 years",
        "explanation": "The caves were abandoned around the 7th century CE and lay hidden in jungle for over 1,000 years until 1819.",
    },
]
