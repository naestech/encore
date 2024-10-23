# encore

**encore** is an email automation script that spotlights musicians who are selling out their shows. built for warner music group.

## features
### completed:
- [x] scrape us venue websites for event details. 
- [x] create database with sold-out event information.
- [x] send an automated email of sold-out events.
- [x] scrape tiktok for posts mentioning sold-out shows.
- [x] create database with posts.
- [x] incorporate tiktok data to email.
- [x] set up logging for data collection

### upcoming:
- [ ] add gdpr compliance measures
- [ ] clean tiktok and venue data
- [ ] standardize venue data format
- [ ] create backup system for data
- [ ] add rate limiting for api calls
- [ ] set up crons for daily data collection
- [ ] automate scheduling with alerts
- [ ] implement retry for failed tasks
- [ ] build monitoring system for automations
- [ ] customize email templates

## how it works

  ![output](https://github.com/user-attachments/assets/59d85dab-39dd-4590-8a98-879759aae30a)
  *sample output*

## setup
1. clone the repository:
    ```bash
    git clone https://github.com/naestech/encore
    cd encore
    ```
2. install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. run:
   ```bash
   python3 -m src.main
   ```

