from flask import Flask, render_template, request, jsonify
from difflib import get_close_matches
import re

app = Flask(__name__)

# Static course data
course_data = {
    "ug": [
        {"name": "B.Tech. Artificial Intelligence and Data Science", "desc": "Focuses on machine learning, data analytics, and AI technologies."},
        {"name": "B.Tech. Bio-Technology", "desc": "Integrates biology with technology, emphasizing genetics, molecular biology, and biochemical processes."},
        {"name": "B.Tech. Bio-Medical Engineering", "desc": "Combines engineering principles with medical sciences to develop healthcare solutions."},
        {"name": "B.Tech. Chemical Engineering", "desc": "Covers chemical process design, reaction engineering, and materials science."},
        {"name": "B.E. Civil Engineering", "desc": "Involves infrastructure design, structural engineering, geotechnical, and construction planning."},
        {"name": "B.E. Computer and Communication Engineering", "desc": "Blends computer systems with advanced communication technologies."},
        {"name": "B.E. Computer Science and Engineering", "desc": "Covers core CS subjects like programming, OS, algorithms, databases, and software development."},
        {"name": "B.Tech. Computer Science and Business Systems", "desc": "Integrates computer science with business analytics, strategy, and systems."},
        {"name": "B.Tech. Artificial Intelligence and Machine Learning", "desc": "Focuses on automation, robotics, deep learning, and AI-powered applications."},
        {"name": "B.E. Electrical and Electronics Engineering", "desc": "Covers electrical systems, circuits, machines, and control systems."},
        {"name": "B.E. Electronics and Communication Engineering", "desc": "Emphasizes VLSI, embedded systems, communication protocols, and signal processing."},
        {"name": "B.Tech. Information Technology", "desc": "Focuses on software systems, IT infrastructure, networking, and web technologies."},
        {"name": "B.E. Mechanical Engineering", "desc": "Involves design, manufacturing, thermodynamics, and mechanical systems automation."}
    ],
    "pg": [
        {"name": "M.E. Applied Electronics", "desc": "Advanced electronics, circuit simulation, embedded systems, and VLSI design."},
        {"name": "M.E. Computer Science and Engineering", "desc": "Deep study in algorithms, AI, software engineering, and system security."},
        {"name": "M.E. Power Systems Engineering", "desc": "Focus on electrical power generation, smart grids, and high-voltage engineering."}
    ]
}

def normalize_input(user_input):
    return user_input.lower()

def get_ug_courses():
    return "\n\nWe offer 13 Undergraduate (UG) engineering programs:\n\n" + "\n".join(
        f"{i+1}. {course['name']}" for i, course in enumerate(course_data["ug"])
    )

def get_pg_courses():
    return "\n\nWe offer 3 Postgraduate (PG) engineering programs:\n\n" + "\n".join(
        f"{i+1}. {course['name']}" for i, course in enumerate(course_data["pg"])
    )

def get_course_details(name_only):
    for course in course_data["ug"] + course_data["pg"]:
        if course["name"].lower() == name_only:
            return f"📘 {course['name']}\n\n{course['desc']}"
    return None

def get_bot_response(user_input):
    user_input = normalize_input(user_input)

    if ("ug" in user_input and "course" in user_input) or ("undergraduate" in user_input):
        return get_ug_courses()
    elif ("pg" in user_input and "course" in user_input) or ("postgraduate" in user_input):
        return get_pg_courses()
    elif "courses" in user_input or "departments" in user_input:
        return (
            "We offer 13 UG and 3 PG courses in various engineering disciplines.\n"
            "Ask 'What UG courses are offered?' or 'What PG courses are available?' for detailed info."
        )
    elif "admission" in user_input:
        return (
            "Email: vsbec@gmail.com\n"
            "Phone: 9994496212, 8220080832\n"
            "Website: https://vsbec.edu.in"
        )
    elif "chairman" in user_input:
        return "Our Chairman is Mr. V.S. Balsamy, B.Sc., L.L.B., the visionary founder and guiding force behind V.S.B. Engineering College."
    elif "secretary" in user_input:
        return "Our Secretary is Mr. Vijay, who actively oversees the academic and administrative operations of the institution."
    elif "director" in user_input:
        return "Our Director is Mrs. Suganthi, dedicated to ensuring quality education and student success."
    elif "principal" in user_input:
        return "Our respected Principal is Dr. Vennila, an academic leader with a strong vision."
    elif "vice principal" in user_input:
        return "Our Vice Principal is Dr. T. Kirubha Shankar, ensuring smooth academic functioning."
    elif "hostel" in user_input:
        return "Yes! We provide separate hostel facilities for boys and girls with 24/7 security, Wi-Fi, mess, and study halls."
    elif "fees" in user_input and "cse" in user_input:
        return "The fee for the CSE program is approximately ₹85,000 per year. For exact details, contact the admin office."
    elif "address" in user_input or "location" in user_input:
        return "V.S.B Engineering College, Karudayampalayam, Karur-639111, Tamil Nadu, India."
    elif "placement" in user_input:
        return "We have a 90%+ placement record with top recruiters like TCS, Infosys, Zoho, and Wipro."
    elif "library" in user_input:
        return "Our central library has 20,000+ books, e-journals, and digital resources across all disciplines."
    elif "bus" in user_input or "transport" in user_input:
        return "Yes, college buses cover major towns around Karur, Erode, Namakkal, and nearby districts."
    elif "okay" in user_input:
        return "Thaks for visiting and Any help or details for college."
    elif "hi" in user_input or "hai" in user_input:
        return "WELCOME TO V.S.B Engineering college AI Chatbot"

    # Course-specific responses
    elif "csbs" in user_input or "computer science and business systems" in user_input:
        return (
            "B.Tech in Computer Science and Business Systems (CSBS) blends core computer science subjects with business concepts.\n"
            "Topics include software development, data structures, business analytics, finance, and project management.\n"
            "Many CSBS programs, particularly those offered in collaboration with Tata Consultancy Services (TCS), emphasize industry-specific skills and practical experience.\n"
            "Students gain skills in areas like software development, data analysis, project management, and business communication."
        )
    elif "aids" in user_input or "artificial intelligence and data science" in user_input:
        return (
            "B.Tech in Artificial Intelligence and Data Science (AI & DS) is a four-year undergraduate program focused on intelligent systems and large-scale data analysis.\n"
            "Covers machine learning, deep learning, big data, NLP, and tools like Python, R, SQL, TensorFlow, and Tableau."
        )
    elif "aiml" in user_input or "artificial intelligence and machine learning" in user_input:
        return (
            "B.Tech in Artificial Intelligence and Machine Learning (AI & ML) focuses on developing AI-driven software and intelligent systems.\n"
            "Includes ML algorithms, computer vision, natural language processing, and AI applications."
        )
    elif "it" in user_input or "information technology" in user_input:
        return (
            "B.Tech in Information Technology (IT) focuses on the use of computers to store, retrieve, transmit, and manipulate data.\n"
            "Covers programming, databases, networks, cybersecurity, and web development."
        )
    elif "cse" in user_input or "computer science and engineering" in user_input:
        return (
            "B.E. in Computer Science and Engineering (CSE) is a core program covering algorithms, programming, operating systems, and software engineering.\n"
            "Equips students for careers in software development, system architecture, and cloud computing."
        )
    elif "ece" in user_input or "electronics and communication engineering" in user_input:
        return (
            "B.E. in Electronics and Communication Engineering (ECE) covers electronic devices, circuits, communication systems, and VLSI design.\n"
            "Enables careers in embedded systems, telecom, IoT, and robotics."
        )
    elif "eee" in user_input or "electrical and electronics engineering" in user_input:
        return (
            "B.E. in Electrical and Electronics Engineering (EEE) combines electrical engineering fundamentals with electronics.\n"
            "Focus on power systems, control engineering, electrical machines, and automation."
        )
    elif "mech" in user_input or "mechanical engineering" in user_input:
        return (
            "B.E. in Mechanical Engineering focuses on the design, analysis, and manufacturing of mechanical systems.\n"
            "Includes thermodynamics, CAD/CAM, material science, and robotics."
        )
    elif "civil" in user_input or "civil engineering" in user_input:
        return (
            "B.E. in Civil Engineering deals with the planning, design, and construction of infrastructure like buildings, roads, and bridges.\n"
            "Topics include structural analysis, geotechnical engineering, and environmental engineering."
        )
    elif "agri" in user_input or "agriculture engineering" in user_input:
        return (
            "B.E. in Agriculture Engineering integrates engineering principles with agricultural practices.\n"
            "Focuses on farm machinery, irrigation systems, soil conservation, and food processing."
        )
    elif "biotech" in user_input or "bio-technology" in user_input:
        return (
            "B.Tech in Bio-Technology applies biological systems and organisms to develop products.\n"
            "Topics include genetic engineering, microbiology, bioprocess technology, and bioinformatics."
        )
    elif "chemical" in user_input or "chemical engineering" in user_input:
        return (
            "B.Tech in Chemical Engineering involves the design and operation of chemical processes for manufacturing.\n"
            "Subjects include thermodynamics, process control, and chemical reaction engineering."
        )
    elif "bme" in user_input or "biomedical engineering" in user_input:
        return (
            "B.E. in Biomedical Engineering blends medical science with engineering techniques.\n"
            "Focuses on medical devices, imaging systems, biomaterials, and healthcare technologies."
        )

    # Fuzzy match fallback
    all_courses = course_data["ug"] + course_data["pg"]
    course_names = [course["name"].lower() for course in all_courses]

    user_words = re.findall(r"\b\w+\b", user_input)
    for word in user_words:
        matches = get_close_matches(word, course_names, n=1, cutoff=0.7)
        if matches:
            matched_name = matches[0]
            return get_course_details(matched_name)

    return "I'm sorry, I didn't understand that. Please ask about courses, hostel, admission, fees, placement, etc."

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    response = get_bot_response(user_input)
    return jsonify({"reply": response})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
