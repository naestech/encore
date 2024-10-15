# encore

**encore** is an email automation script that spotlights musicians who are selling out their shows. built for warner music group.

## features
### main.py:
- [x] scrape local venue websites for event details.
- [x] create database with sold-out event information.
- [x] send an automated email of sold-out events.
      
### tiktok.py:
- [x] scrape tiktok for posts mentioning sold-out shows.
- [x] create database with posts.

### upcoming:
- [ ] clean tiktok data
- [ ] encorporate tiktok data to email
- [ ] customize email.
- [ ] automated scheduling


## how it works
- **`main.py`**: scrapes html of popular venues across the country for upcoming sold-out events, saves details to `encore.db`, and sends an automated email with details.
  ![output](https://github.com/user-attachments/assets/70446f8f-5887-4dee-ac02-9a69c75e0a5c)
  *sample output*

- **`tiktok.py`**: scrapes tiktok for videos with captions like "sold out shows" or "sold out concerts" and saves details to `tiktok_data.db` 
  ![output](https://github.com/user-attachments/assets/71cf2049-030b-47be-b4bc-c76a08bfe0a9)
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
   python3 main.py
   ```

