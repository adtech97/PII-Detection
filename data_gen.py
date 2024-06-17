import random
import pandas as pd
from faker import Faker
from faker.providers import BaseProvider

# Custom provider for PPSN and Bank Account Number
class CustomProvider(BaseProvider):
    def ppsn(self):
        letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        digits = '0123456789'
        ppsn = ''.join(random.choices(digits, k=7)) + random.choice(letters)
        if random.choice([True, False]):
            ppsn += random.choice(letters)
        return ppsn
    
    def bank_account_number(self):
        digits = '0123456789'
        return ''.join(random.choices(digits, k=10))

fake = Faker()
fake.add_provider(CustomProvider)

# Function to generate a coherent email chain with optional PII
def generate_email_chain(message_id):
    from_email = fake.email()
    to_email = fake.email()
    email_type = random.choice(['financial_inquiry', 'account_update', 'payment_notification', 'general_message'])
    
    # Templates for different types of emails
    if email_type == 'financial_inquiry':
        subject = f"Question about my recent transaction"
        body = (f"Hi,\n\nI have a question regarding a recent transaction on my account. Could you please provide "
                f"more details about the following transaction?\n\nAmount: {fake.pricetag()}\nDate: {fake.date()}\n\n"
                f"Thank you,\n{fake.name()}")
    elif email_type == 'account_update':
        subject = f"Important Account Update"
        body = (f"Dear {fake.first_name()},\n\nWe have updated our terms and conditions. Please review the changes at "
                f"your earliest convenience. Your account details are as follows:\n\nAccount Number: {fake.bank_account_number()}\n"
                f"Update Date: {fake.date()}\n\nBest regards,\n{fake.company()}")
    elif email_type == 'payment_notification':
        subject = f"Payment Confirmation - {fake.pricetag()}"
        body = (f"Hello {fake.first_name()},\n\nWe have received your payment of {fake.pricetag()} on {fake.date()}. "
                f"Thank you for your prompt payment. Your transaction ID is {fake.uuid4()}.\n\nRegards,\n{fake.company()}")
    else:
        subject = f"Meeting Reminder"
        body = (f"Hi {fake.first_name()},\n\nThis is a reminder for our upcoming meeting scheduled on {fake.date()} at "
                f"{fake.time()}. Please let me know if you need to reschedule.\n\nBest,\n{fake.name()}")
    
    # Randomly decide if this email should contain PII
    contains_pii = random.choice([True, False])
    if contains_pii:
        # Expanded list of different PII fields
        pii_fields = [
            f"PPSN: {fake.ppsn()}",
            f"Credit Card: {fake.credit_card_number()}",
            f"Bank Account: {fake.bank_account_number()}",
            f"Address: {fake.address()}",
            f"IBAN: {fake.iban()}",
            f"Phone Number: {fake.phone_number()}",
            f"Tax ID: {fake.itin()}"
        ]
        # Randomly choose how many PII fields to include
        num_pii_fields = random.randint(1, len(pii_fields))
        selected_pii_fields = random.sample(pii_fields, k=num_pii_fields)
        
        # Randomly distribute PII fields between subject and body
        subject_pii_count = random.randint(0, num_pii_fields)
        
        subject += " " + " ".join(selected_pii_fields[:subject_pii_count])
        body += "\n\n" + "\n".join(selected_pii_fields[subject_pii_count:])

    complete_message = f"From: {from_email}\nTo: {to_email}\nSubject: {subject}\n\n{body}"
    
    return {
        "message_id": message_id,
        "text": complete_message
    }

# Generate 20,000 rows of email chains
email_data = [generate_email_chain(i) for i in range(1, 20001)]

# Create a DataFrame
df = pd.DataFrame(email_data)

# Verify the DataFrame content
print(df["text"].iloc[0])

# Save to a CSV file
df.to_csv("Data/pii_emails.csv", index=False, encoding='utf-8')
