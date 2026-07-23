import win32com.client as win32


def send_email_from_application(
    recipients, subject, body, file_link=None, link_text="Otwórz plik", html_content=""
):
    # Create an Outlook application instance
    outlook = win32.Dispatch("Outlook.Application")

    # Create a new mail item
    mail = outlook.CreateItem(0)

    # Set the email parameters
    mail.To = recipients
    mail.Subject = subject

    # Jeśli przekazano link do pliku, doklejamy go na końcu treści HTML
    if file_link:
        attachment_html = (
            f'<br><br><p><b>Załącznik:</b> <a href="{file_link}">{link_text}</a></p>'
        )
        body += attachment_html
        body += "<br>"
        body += html_content

    # Set the HTML body of the email
    mail.HTMLBody = body

    # Display the email in Outlook (opens a new window)
    mail.Display()