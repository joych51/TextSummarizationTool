P R I S M

AI-Powered Text Summarization Platform

🎯 Project Overview

An innovative web application that leverages AI to provide efficient text summarization and sentiment analysis, helping users quickly extract key information from extensive documents.

🛠 Tech Stack

Backend (FastAPI)

* Text summarization using Hugging Face's BART-large-CNN model
* Sentiment analysis integration with AWS Comprehend
* RESTful API endpoints development
* Secure cross-origin communication (CORS)

Frontend (React)
* Intuitive user interface for text input and file upload
* Real-time result visualization
* Responsive web design
* Interactive summary display

AWS Infrastructure
S3
* User file storage and management
* Timestamp-based unique file naming
* Efficient content extraction and processing

DynamoDB
* Persistent storage for summarization results
* UUID-based data management
* Comprehensive metadata storage
* Historical data tracking
  
🌟 Key Features
* Text summarization from various input methods
* Sentiment analysis of content
* File upload and processing
* Secure data storage and retrieval
* Real-time processing feedback
  
🎯 Applications
* Academic Research: Streamline research paper analysis
* Business Intelligence: Condense market reports
* Media Monitoring: Summarize news and social media
* Educational Support: Create concise study materials
* Content Management: Efficient content curation

🚀 Future Enhancements

Advanced Features
* Multi-language support
* Customizable summarization parameters
* Topic extraction and categorization
* Document comparison capabilities
  
Technical Improvements
* Real-time collaboration features
* Document management system integration
* Enhanced security protocols
* Third-party API integrations
  
Scalability
* Batch document processing
* Enterprise user management
* Advanced analytics dashboard
* Mobile application development
  
AI/ML Enhancements
* Domain-specific model training
* Context-aware sentiment analysis
* Extended NLP capabilities
* Content quality assessment
  
📝 Getting Started
* Prerequisites
  - python 3.x
  - node.js
  - AWS Account
* Installation
  - Clone the repository - git clone [repository_url]
* Backend setup
  - cd backend pip -r requirements.txt
* Frontend setup
  - cd frontend
  - npm intall
* Configure environment variables
  - AWS_ACCESS_KEY_ID=your_access_key
  - AWS_SECRET_ACCESS_KEY=your_secret_key
  - AWS_REGION=your_region
  - S3_BUCKET_NAME=your_bucket_name
Run the application
* Backend
  - uvicorn app:app --host 0.0.0.0 --port 8000 --reload
* Frontend
  - npm start
    
👥 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.
