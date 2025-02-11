import os

# Dictionary containing game card details for each career with Markdown formatting
game_cards = {
    "Farmer": """
# **Farmer**

## **Overview**

Farmers are the backbone of our food system. They cultivate crops, tend to livestock, and employ sustainable practices to ensure food security and support rural communities.

## **Pros & Cons**

### ✅ Pros:

- 🌱 **Connection with nature and independence**
- 🍎 **Contributing to community food security**
- ⏳ **Flexibility in work and lifestyle**

### ❌ Cons:

- 🌦 **Financial uncertainty and weather dependency**
- 💪 **Physically demanding work**
- 🌍 **Isolation in remote areas**

## **Dual Impact Highlights**

- *Personal Growth:* Develops resilience, self-reliance, and a deep understanding of natural cycles.
- *Community Impact:* Supports local economies, food supply, and sustainable rural development.

---
""",
    "Doctor": """
# **Doctor**

## **Overview**

Doctors diagnose and treat illnesses, provide essential medical care, and work to improve overall public health. They serve as a critical pillar in the healthcare system.

## **Pros & Cons**

### ✅ Pros:

- ❤️ **High impact on patient lives and community well-being**
- 📚 **Continuous learning and professional development**
- 👩‍⚕️ **Stable and respected career path**

### ❌ Cons:

- ⏳ **Long and irregular working hours**
- 😟 **High levels of stress and emotional strain**
- 🔥 **Risk of burnout and challenging work-life balance**

## **Dual Impact Highlights**

- *Personal Growth:* Enhances problem-solving, empathy, and lifelong learning.
- *Community Impact:* Improves public health and provides critical medical support.

---
""",
    "IAS Officer": """
# **IAS Officer**

## **Overview**

IAS Officers are senior civil servants who administer public policy, manage governmental functions, and drive developmental projects. They play a key role in the functioning of the state.

## **Pros & Cons**

### ✅ Pros:

- 🏅 **Prestigious position with high influence**
- 📜 **Opportunities to implement impactful policies**
- 🎯 **Diverse and challenging responsibilities**

### ❌ Cons:

- 🏛 **Intense public scrutiny and pressure**
- ⚖ **High stress due to political and bureaucratic demands**
- ⏳ **Long working hours and significant responsibilities**

## **Dual Impact Highlights**

- *Personal Growth:* Cultivates leadership, strategic thinking, and resilience.
- *Community Impact:* Facilitates effective governance and societal progress.

---
""",
    "Teacher": """
# **Teacher**

## **Overview**

Teachers educate, inspire, and shape future generations. They create learning environments that foster intellectual growth and personal development.

## **Pros & Cons**

### ✅ Pros:

- 🎓 **Rewarding experience through shaping young minds**
- 🏫 **Creative and dynamic work environment**
- 📈 **Stable career with opportunities for growth**

### ❌ Cons:

- 📝 **Workload including administrative duties**
- 💰 **Sometimes limited resources and support**
- 🎯 **Pressure to meet educational standards**

## **Dual Impact Highlights**

- *Personal Growth:* Encourages continuous learning, creativity, and mentorship.
- *Community Impact:* Empowers individuals and strengthens the fabric of society through education.

---
""",
    "Nurse": """
# **Nurse**

## **Overview**

Nurses provide vital care, support patients, and assist doctors in healthcare settings. They are essential in maintaining patient recovery and overall hospital operations.

## **Pros & Cons**

### ✅ Pros:

- 🏥 **High demand with job security**
- 🎓 **Opportunities for specialization and advancement**
- ❤️ **Fulfilling and impactful work**

### ❌ Cons:

- 💪 **Physically demanding and shift-based work**
- 😢 **Emotional challenges from patient care**
- ⚕ **Exposure to health risks**

## **Dual Impact Highlights**

- *Personal Growth:* Builds empathy, technical expertise, and resilience.
- *Community Impact:* Enhances patient care and supports community health.

---
""",
    "Political Leader": """
# **Political Leader**

## **Overview**

Political leaders guide societies by creating policies, leading governance, and addressing public issues. They shape the future of communities and nations.

## **Pros & Cons**

### ✅ Pros:
- 🏛 **Ability to influence policy and governance**
- 📢 **Opportunity to serve the public and drive change**
- 🌍 **Potential to create a lasting legacy**

### ❌ Cons:

- ⚖ **High public scrutiny and criticism**
- 🔥 **Constant pressure and political challenges**
- 🕰 **Demanding schedule with unpredictable work hours**

## **Dual Impact Highlights**

- *Personal Growth:* Builds leadership, strategic thinking, and resilience.
- *Community Impact:* Shapes policies, improves governance, and drives societal development.

---
""",
    "Police Officer": """
# **Police Officer**

## **Overview**

Police officers maintain law and order, protect citizens, and ensure public safety through crime prevention and enforcement of the law.

## **Pros & Cons**

### ✅ Pros:

- 🚔 **Opportunity to serve and protect society**
- 🛡 **Stable and respected career**
- 🏅 **Exciting and dynamic work environment**

### ❌ Cons:

- ⚠ **Physically and mentally demanding job**
- ⏳ **Long and irregular working hours**
- 🏛 **High-risk situations and exposure to crime**

## **Dual Impact Highlights**

- *Personal Growth:* Enhances discipline, courage, and problem-solving skills.
- *Community Impact:* Maintains public safety, reduces crime, and builds community trust.

---
""",
    "Actor": """
# **Actor**

## **Overview**

Actors bring stories to life through performances in films, theatre, and television. They captivate audiences and contribute to the entertainment industry.

## **Pros & Cons**

### ✅ Pros:

- 🎭 **Creative and expressive career path**
- 🌟 **Potential for fame and financial success**
- 🎬 **Opportunity to influence culture and storytelling**

### ❌ Cons:

- 🎢 **Unstable career with fluctuating income**
- 🔥 **Pressure to perform and maintain public image**
- 🕰 **Demanding schedules with long working hours**

## **Dual Impact Highlights**

- *Personal Growth:* Enhances creativity, confidence, and communication skills.
- *Community Impact:* Provides entertainment, inspiration, and cultural enrichment.

---
""",
    "Singer": """
# **Singer**

## **Overview**

Singers express emotions and stories through music. They perform for live audiences, record albums, and contribute to the music industry.

## **Pros & Cons**

### ✅ Pros:

- 🎤 **Creative freedom and artistic expression**
- 🌍 **Opportunity to connect with audiences globally**
- 🎶 **Potential for financial success and recognition**

### ❌ Cons:

- 🎢 **Competitive industry with uncertain career stability**
- 🔥 **Vocal strain and health challenges**
- 🕰 **Irregular schedules with travel demands**

## **Dual Impact Highlights**

- *Personal Growth:* Develops vocal talent, creativity, and resilience.
- *Community Impact:* Inspires, entertains, and unites people through music.

---
""",
}

# Create the 'jobcards' directory if it doesn't already exist
os.makedirs("jobcards", exist_ok=True)

# Write each game card to its respective Markdown file with formatted text
for job, content in game_cards.items():
    filename = os.path.join("jobcards", f"{job.replace(' ', '_').lower()}.md")
    with open(filename, "w", encoding="utf-8") as file:
        file.write(content)

print("Game cards generated with Markdown formatting and stored in the 'jobcards' directory.")
