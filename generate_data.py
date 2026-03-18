import pandas as pd
import random

# Templates for generating data
scam_templates = [
    "URGENT: We are urgently hiring for {job}. Pay is {pay} per month. Contact HR via WhatsApp at {phone} immediately.",
    "Congratulations! You've been selected for a remote {job} position. Please pay a refundable registration fee of {fee} to proceed.",
    "Work from home data entry jobs available. Earn {pay} daily. No experience needed! Click link to register and pay {fee} equipment fee.",
    "Dear applicant, to secure your {job} role and receive your company laptop, kindly transfer {fee} to our vendor.",
    "SHOCKING! {job} making {pay} from home using this one secret trick. Click here to claim your spot.",
    "Exclusive offer: Make {pay} a week doing simple tasks. Must pay {fee} for the training materials first.",
    "Job alert! Immediate start. Must have Telegram and WhatsApp. Message {phone} for details. Unbelievable pay!",
    "Your application was accepted! We need your bank details and social security to set up direct deposit. Send them to this email.",
    "Want to be a {job}? Join our exclusive network. Only {fee} to sign up and start making {pay} daily!"
]

legit_templates = [
    "We are looking for a qualified {job} to join our team. Please apply via our official portal. Salary is commensurate with experience.",
    "Job Opening: {job} at our downtown office. Responsibilities include managing projects and collaborating with the team. Apply on our website.",
    "Our company is hiring a new {job}. Requirements: 3+ years experience, bachelor's degree. Comprehensive benefits package included.",
    "Now hiring full-time {job}. Standard background check required. Please submit your resume to jobs@ourcompany.com.",
    "Exciting opportunity for a {job}. Competitive salary, health insurance, and 401k matching. See our careers page for details.",
    "Internship available in the marketing department. This is a paid position. Submit your application through the university portal.",
    "We are expanding! Seeking a dedicated {job}. Must have excellent communication skills. Apply online.",
    "Software Engineer II required. Python, AWS, and SQL experience needed. Remote work options available."
]

jobs = ["Data Analyst", "Data Entry Clerk", "Software Engineer", "Marketing Assistant", "HR Manager", "Virtual Assistant", "Customer Support Rep", "Freelance Writer"]
pays = ["₹50,000", "$5,000", "₹1,00,000", "$10,000", "$500/day", "₹5000/day", "massive income"]
fees = ["₹499", "$50", "₹999", "$199", "a small fee", "₹1500"]
phones = ["+1-555-0192", "9876543210", "+44-7700-900077", "Telegram @hr_desk"]

dataset = []

# Generate Scams
for _ in range(150):
    template = random.choice(scam_templates)
    text = template.format(
        job=random.choice(jobs), 
        pay=random.choice(pays), 
        fee=random.choice(fees), 
        phone=random.choice(phones)
    )
    dataset.append({"text": text, "label": 1})

# Generate Legit
for _ in range(150):
    template = random.choice(legit_templates)
    text = template.format(job=random.choice(jobs))
    dataset.append({"text": text, "label": 0})

df = pd.DataFrame(dataset)
# Shuffle
df = df.sample(frac=1).reset_index(drop=True)
df.to_csv("data/dataset_large.csv", index=False)
print("Generated data/dataset_large.csv with 300 rows.")
