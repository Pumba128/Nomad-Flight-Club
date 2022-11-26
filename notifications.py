import smtplib
from secrets import my_email, my_password


class EmailBody:

    def __init__(self, to_email, to_name):
        self.email = my_email
        self.password = my_password
        self.to_email = to_email
        self.to_name = to_name

    def send_email(self, formatted_data: dict):
        email_data = formatted_data
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=self.email, password=self.password)
            connection.sendmail(
                from_addr=self.email,
                to_addrs=self.to_email,
                msg=f"Subject:New flight on the radar!\n\n"
                    f"Hello {self.to_name}, only €{email_data['lowestPrice']} to fly from {email_data['cityFrom']}-{email_data['flyFrom']} "
                    f"to {email_data['cityTo']}-{email_data['flyTo']}, from {email_data['fromDate']} "
                    f"to {email_data['toDate']} ({email_data['nightsInDest']} nights).".encode())
