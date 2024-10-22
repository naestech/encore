from src.data.tikTokScraper import TikTokScraper
from src.data.venueScraper import VenueScraper
from src.email.emailSender import EmailSender
from src.utils.errorHandler import ErrorHandler

def main():
    errorHandler = ErrorHandler()
    tikTokScraper = TikTokScraper()
    venueScraper = VenueScraper()
    emailSender = EmailSender()
    
    try:
        # Process TikTok data
        print("\nStarting TikTok data collection...")
        tikTokResults = []
        queries = ["sold out concert", "sold out show"]
        for query in queries:
            print(f"\nSearching TikTok for: {query}")
            results = tikTokScraper.runTikTokExtractor(query)
            if results:
                print(f"Found {len(results)} matching videos")
                for videoData in results:
                    tikTokScraper.saveToDatabase(videoData)
                    tikTokResults.append(videoData)

        # Process venue data
        print("\nStarting venue data collection...")
        venueResults = []
        with open('data/venues.md', 'r') as file:
            venues = file.readlines()
            total_venues = sum(1 for line in venues if 'www.' in line)
            current_venue = 0
            
            for line in venues:
                if 'www.' in line:
                    current_venue += 1
                    url = line.split('(')[1].split(')')[0]
                    print(f"\nProcessing venue {current_venue}/{total_venues}: {url}")
                    try:
                        soldOutShows = venueScraper.scrapeVenueData(url)
                        if soldOutShows:
                            print(f"Found {len(soldOutShows)} sold out shows")
                            venueResults.extend(soldOutShows)
                            for show in soldOutShows:
                                venueScraper.saveToDatabase(show)
                        else:
                            print("No sold out shows found")
                    except Exception as e:
                        errorHandler.logger.warning(f"Failed to process venue {url}: {str(e)}")
                        continue

        # Prepare email data for review
        if venueResults or tikTokResults:
            print("\nData collection complete. Review the following data before sending email:")
            
            if venueResults:
                print("\nVenue Results:")
                for show in venueResults:
                    print(f"\n{show['artist']} at {show['location']} on {show['date']}")
            
            if tikTokResults:
                print("\nTikTok Results:")
                for video in tikTokResults:
                    print(f"\n{video.get('authorMeta', {}).get('name', 'N/A')}: {video.get('text', 'N/A')}")
            
            # Ask for confirmation
            confirm = input("\nWould you like to send the email now? (y/n): ")
            if confirm.lower() == 'y':
                emailSender.sendEmail(subject, body)
                print("Email sent successfully!")
            else:
                print("Email sending cancelled. Data has been saved to database.")

    except Exception as e:
        errorHandler.handle_error(e, "Main process")

if __name__ == "__main__":
    main()
