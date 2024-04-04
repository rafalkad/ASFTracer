# ASFTracer


This repository contains a Django web application for managing African Swine Fever (ASF) incidents, inspections, quarantines, and additional information related to ASF incidents.
Features

    ASF Incident Management: Users can add new ASF incidents with details such as detection date, location, and infected count.
    Inspection and Quarantine Management: Users can add inspections and quarantines associated with ASF incidents.
    Additional Information: Users can provide additional information related to ASF incidents, including epidemiological reports, preventive measures, breeding farm details, and medical resources.
    Notification to Mailchimp: The application sends notifications about the latest ASF incident to Mailchimp, allowing subscribers to stay informed about the latest developments.
    PDF Generation: Additional information related to ASF incidents can be exported to PDF format for easy sharing and distribution.

Installation

To run this application locally, follow these steps:

    Clone the repository:

bash

git clone https://github.com/example/ASF-Management-App.git
cd ASF-Management-App

    Install dependencies:

bash

pip install -r requirements.txt

    Apply database migrations:

bash

python manage.py migrate

    Start the development server:

bash

python manage.py runserver

    Access the application in your web browser at http://localhost:8000.

Usage

    Visit the homepage to navigate through different sections of the application.
    Use the provided forms to add new ASF incidents, inspections, quarantines, and additional information.
    Ensure that Mailchimp API key and server information are configured properly in the notify_mailchimp_about_asf_incident view to enable notification functionality.
    Additional information related to ASF incidents can be exported to PDF format by providing the necessary details and clicking on the "Generate PDF" button.

Testing

This application includes test cases for verifying the functionality of views using pytest. To run tests, execute:

bash

pytest
