"""
Name: Nadine
Email: naestech@proton.me
Description: Main script for the Encore project. Orchestrates the data collection from TikTok and venues, 
and sends an email with the collected information about sold-out shows.
"""

from src.data.tikTokScraper import TikTokScraper
from src.data.venueScraper import VenueScraper
from src.email.emailSender import EmailSender
from src.utils.errorHandler import ErrorHandler
from src.utils.logger import info_logger, error_logger, debug_logger
import sqlite3

def main():
    errorHandler = ErrorHandler()
    tikTokScraper = TikTokScraper()
    venueScraper = VenueScraper()
    emailSender = EmailSender()
    
    try:
        info_logger.info("Starting TikTok data collection...")
        tikTokResults = []
        queries = ["sold out concert", "sold out show"]
        for query in queries:
            info_logger.info(f"Searching TikTok for: {query}")
            results = tikTokScraper.runTikTokExtractor(query)
            if results:
                info_logger.info(f"Found {len(results)} matching videos")
                for videoData in results:
                    tikTokScraper.saveToDatabase(videoData)
                    tikTokResults.append(videoData)

        info_logger.info("Starting venue data collection...")
        venueResults = []
        with open('data/venues.md', 'r') as file:
            venues = file.readlines()
            total_venues = sum(1 for line in venues if 'www.' in line)
            current_venue = 0
            
            for line in venues:
                if 'www.' in line:
                    current_venue += 1
                    url = line.split('(')[1].split(')')[0]
                    info_logger.info(f"Processing venue {current_venue}/{total_venues}: {url}")
                    try:
                        venue_data = venueScraper.scrapeVenueData(url)
                        if venue_data:
                            venueResults.extend(venue_data)
                            venueScraper.save_to_database(venue_data)  # Save to database
                            info_logger.info(f"Found {len(venue_data)} sold out shows")
                        else:
                            info_logger.info("No sold out shows found")
                    except Exception as e:
                        error_logger.error(f"Failed to process venue {url}: {str(e)}")
                        continue

        info_logger.info("Data collection complete.")
        
        # Ask for confirmation to send email
        confirm = input("\nWould you like to send the email now? (y/n): ")
        if confirm.lower() == 'y':
            # Format TikTok data for email
            formatted_tiktok_results = []
            conn = sqlite3.connect('data/tiktokData.db')
            cursor = conn.cursor()
            cursor.execute("SELECT username, post_content, video_url FROM videos ORDER BY post_time DESC LIMIT 5")
            tiktok_data = cursor.fetchall()
            conn.close()

            for username, post_content, video_url in tiktok_data:
                formatted_post = {
                    'username': username,
                    'post_content': post_content,
                    'video_url': video_url
                }
                formatted_tiktok_results.append(formatted_post)
            
            # Generate email body
            body = emailSender.generateEmailBody(venueResults, formatted_tiktok_results)
            
            subject = "The Latest Sold-Out Events & Trending TikToks"
            emailSender.sendEmail(subject, body)
            info_logger.info("Email sent successfully!")
        else:
            info_logger.info("Email sending cancelled. Data has been saved to database.")

    except Exception as e:
        errorHandler.handle_error(e, "Main process")

if __name__ == "__main__":
    main()
