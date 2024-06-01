# Autoria Scraping Project

This project is a web scraper designed to extract data from the Autoria website using Scrapy, a powerful Python framework for web crawling and scraping.

**Key Features:**

* **Scrapy:** Efficient and scalable web crawling framework.
* **Scrapy-Selenium:**  Integrates Selenium for dynamic website scraping.
* **Celery:** Distributed task queue for scheduling and managing background tasks.
* **Docker:** Containerization for easy setup and deployment.
* **PostgreSQL:** Database for storing scraped data.
* **Logging:** Comprehensive logging to the `logs` directory for debugging and monitoring.
* **Database Backups:** Automatic database dumps to the `dumps` directory.

## Getting Started

### Prerequisites

* **Docker:** Make sure Docker and Docker Compose are installed on your system.

### Setup

1. **Clone the Repository:**
```bash
   git clone https://github.com/Dh-Kh/123DATA.git
   cd scraper
```

2. **Execute commands:**
```bash
   docker-compose build 
   docker-compose up -d
   docker-compose run scrapy celery -A scraping.scheduler worker -l debug --logfile=logs/celery.log --beat
   ```

3. **Useful commands:**
```bash
    docker-compose run scrapy scrapy crawl scraping_spider
    docker-compose exec pgdb psql -h localhost -U postgres
```
📂 scraper
├── 📁 logs
└── 📁 scraping
    ├── 📁 dumps
    └── 📁 spiders
