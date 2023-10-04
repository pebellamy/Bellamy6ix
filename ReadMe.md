# ReadMe!
### Features I want to add
### A styles.css file
-  I'll put this in the static folder

### Caption Game
- A caption game!
- Will eventually need users. for now, I think the first screen is sign up, then you play as what you typed.
- Caption contests should have the following data structure:
 - Contest
  - id
  - image_url
  - title
  - winner_caption_id
  - *has-many* caption_ids
- Caption
 - id
 - user_id (or name for now)
 - content
 