import sqlite3

# Connect to (or create) the database file
conn = sqlite3.connect("jobcards.db")
cursor = conn.cursor()

# Create the 'questions' table if it doesn't already exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job TEXT NOT NULL,
    question TEXT NOT NULL,
    answer TEXT NOT NULL
)
""")

# Sample data: 5 questions and answers for each job profile.
sample_data = {
    "Farmer": [
        ("What are the challenges of modern farming?", 
         "Modern farming requires adapting to unpredictable weather, changing market conditions, and managing resources effectively."),
        ("How does technology improve farming?", 
         "Technology increases efficiency, crop yields, and helps in better resource management in farming."),
        ("What sustainable practices are important in agriculture?", 
         "Crop rotation, organic fertilizers, and water conservation are vital sustainable practices."),
        ("How do farmers contribute to society?", 
         "Farmers provide food security, support rural economies, and contribute to the overall well-being of the community."),
        ("What skills are crucial for a successful farmer?", 
         "Resilience, innovation, and deep knowledge of agronomy are essential for success in farming.")
    ],
    "Doctor": [
        ("What is the most challenging aspect of being a doctor?", 
         "Balancing long hours and intense patient care with personal well-being is a major challenge."),
        ("How do doctors manage stress in a busy hospital?", 
         "Effective time management, teamwork, and self-care are crucial to managing stress in a hospital setting."),
        ("What innovations are shaping the future of medicine?", 
         "Telemedicine, AI diagnostics, and personalized medicine are revolutionizing healthcare."),
        ("How do doctors stay updated with medical advancements?", 
         "Through continuous education, professional conferences, and staying current with research."),
        ("What is the role of empathy in healthcare?", 
         "Empathy builds patient trust, improves care outcomes, and enhances the overall patient experience.")
    ],
    "IAS Officer": [
        ("What is the primary role of an IAS officer?", 
         "IAS officers implement policies, manage public resources, and drive development projects."),
        ("How do IAS officers manage public resources?", 
         "They use strategic planning and diligent monitoring to ensure effective resource management."),
        ("What challenges do IAS officers face in governance?", 
         "They often encounter bureaucratic hurdles, public accountability, and high-pressure decision-making."),
        ("How can IAS officers drive social change?", 
         "By implementing progressive policies and engaging directly with communities."),
        ("What skills are essential for an IAS officer?", 
         "Strong leadership, strategic thinking, and effective communication are key skills for an IAS officer.")
    ],
    "Teacher": [
        ("How do you engage students in a classroom?", 
         "Interactive methods, personalized attention, and innovative teaching tools help engage students."),
        ("What challenges do teachers face with large class sizes?", 
         "Large class sizes require efficient classroom management and tailored instruction strategies."),
        ("How can teachers integrate technology into their lessons?", 
         "Using digital tools and online resources can make lessons more engaging and informative."),
        ("What makes teaching a rewarding career?", 
         "Watching students learn and succeed, and making a lasting impact on their lives, is incredibly rewarding."),
        ("How do teachers adapt to diverse learning styles?", 
         "By employing varied teaching methods and personalized learning strategies.")
    ],
    "Nurse": [
        ("What is the most fulfilling part of nursing?", 
         "Providing compassionate care and supporting patients in their recovery is very fulfilling."),
        ("How do nurses manage the demands of shift work?", 
         "Teamwork, proper time management, and self-care strategies are essential for managing shift work."),
        ("What role do nurses play in patient advocacy?", 
         "Nurses ensure that patients receive appropriate care and that their voices are heard."),
        ("How do nurses handle high-stress situations?", 
         "By staying calm, following protocols, and communicating effectively with the team."),
        ("What advancements have improved nursing care?", 
         "Innovations in medical technology and updated care protocols have greatly enhanced nursing practice.")
    ],
    "Political Leader": [
        ("What is the primary responsibility of a political leader?", 
         "Political leaders are responsible for shaping policies and steering the direction of governance."),
        ("How do political leaders balance diverse interests?", 
         "They build consensus through negotiation and work with various stakeholders."),
        ("What challenges do political leaders face in governance?", 
         "They often deal with public scrutiny, conflicting interests, and complex policy issues."),
        ("How can a political leader drive positive change?", 
         "By advocating for policies that promote social welfare and sustainable development."),
        ("What skills are essential for effective political leadership?", 
         "Effective communication, strategic vision, and integrity are crucial for political leaders.")
    ],
    "Police Officer": [
        ("What motivates you to serve as a police officer?", 
         "A commitment to justice and community safety motivates many police officers."),
        ("How do police officers maintain public trust?", 
         "By upholding the law fairly and engaging positively with the community."),
        ("What are the biggest challenges in policing?", 
         "Handling dangerous situations and maintaining order in unpredictable circumstances are major challenges."),
        ("How do police officers manage stress on the job?", 
         "Regular training, strong teamwork, and support systems help manage job-related stress."),
        ("What role does community policing play in modern law enforcement?", 
         "Community policing builds trust and improves communication between law enforcement and residents.")
    ],
    "Actor": [
        ("How do actors prepare for a role?", 
         "Actors research the character, study the script, and often engage in method acting techniques."),
        ("What is the most challenging aspect of acting?", 
         "Capturing authentic emotions and maintaining character integrity can be very challenging."),
        ("How do actors deal with rejection?", 
         "Resilience, continuous self-improvement, and passion for the craft help actors handle rejection."),
        ("What role does collaboration play in acting?", 
         "Collaboration with directors, fellow actors, and crew is essential for a successful performance."),
        ("How do actors stay motivated in a competitive industry?", 
         "A love for storytelling and constant practice keep actors motivated despite the competition.")
    ],
    "Singer": [
        ("What is essential for a captivating singing performance?", 
         "Emotional connection, vocal control, and strong stage presence are essential."),
        ("How do singers maintain their vocal health?", 
         "Regular warm-ups, proper technique, and adequate rest are key to maintaining vocal health."),
        ("What challenges do singers face in the music industry?", 
         "Intense competition, performance pressure, and inconsistent work opportunities are common challenges."),
        ("How do singers connect with their audience?", 
         "They connect through expressive performances and authentic storytelling."),
        ("What role does training play in a singer's career?", 
         "Continuous vocal training and practice are critical for developing and sustaining a successful singing career.")
    ]
}

# Insert sample data into the 'questions' table
for job, qa_list in sample_data.items():
    for question, answer in qa_list:
        cursor.execute("INSERT INTO questions (job, question, answer) VALUES (?, ?, ?)", 
                       (job, question, answer))

conn.commit()
conn.close()

print("jobcards.db created with at least 5 questions per job.")
