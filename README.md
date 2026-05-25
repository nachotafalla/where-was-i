# Where Was I
My CS50 final project

#### Video Demo: 

#### Description:
Where Was I? is a Flask web application that helps users track television shows they are watching and identify new episodes that have aired since their last watched episode.

## Overview
I made Where Was I? inspired by the last couple of weeks of the CS50 lectures. I found myself getting confused with APIs, HTML, Flask routes, and Jinja templates so I decided to focus on these to challenge myself to build something I could write and understand every single line of code by myself. 

The user can search for a show, add it to their library, save the last season and episode they watched, and check whether new episodes have aired since then. I ended up choosing this idea because I watch a lot of TV shows and end up writing them on my notes app, but then I never get notified when there's a new episode or season. I'm sure there are many other apps and services that accomplish this, but the goal of this project wasn't to create a revolutionary original product but rather a practical idea that would cover all the concepts I found more challenging.

The application is built with Python, Flask, SQLite, HTML, CSS, Jinja templates, and the TVMaze API. It is designed as a simple single-user local web app, so it does not include accounts, social features, or push notifications (mainly because this would overcomplicate everything and end up not even being used). The main goal is to provide a clean and understandable tool for tracking shows and identifying new episodes through in-app updates.

## Features

### Dashboard
The dashboard gives the user an overview of the shows currently being watched, those finished, and those with updates, without having to visit every show individually.

### Search
Search bar allows the user to enter a query, which, when submitted, sends a request to TVMaze to display matching results. Each result includes some short info such as poster, name, status, premiere date, rating, genre, and a button for the details page.

### Show Details
Each show has a details page that contains more information the user might want to see, along with its summary. From here the user can add the show to their library, unless it's already there, in which case it won't let the user add it twice.

### Library
Shows all saved shows from the local SQLite database. Shows are separated into two groups: currently watching and finished. The user can move a show easily between these two categories. From the library the user can open the show's details page, update its current progress through buttons or manual selection, mark it as finished or unfinished and remove it from the library.

### Progress Tracking
The way the progress is tracked is by saving the user's data in the local database. The user can increase or decrease progress by one episode or manually select a season and episode out of the options TVMaze displays. The app also uses TVMaze episode data to understand the latest known season and episode for each show. This allows progress controls to behave more intelligently and helps the app compare the user’s saved progress with real episode data.

### Finished Shows
Shows marked as finished are moved into a separate section of the library. Finished shows are still checked for new aired episodes, so if a new season or episode is released later, the show can appear again on the Updates page.

### Updates
The Updates page compares each saved show’s current progress with the aired episode list from TVMaze. If an episode has already aired and comes after the user’s saved season and episode, it is shown as a new update. Future episodes are ignored so the page only displays episodes the user can actually watch. If a finished show receives new episodes, it can still appear in Updates, and the user can move it back to Watching.

### Responsive Navigation and Styling
I used Bootstrap 5 for layout and responsive navigation and elements. The nav bar links to all pages (dashboard, search, library, and updates), and used CSS for darker styles and small design choices.

## How It Works
The app combines local data storage using SQLite along with external data from the TVMaze API.  The local database stores information about the user and their shows. It doesn't store full episode lists but rather current progress. Episode information is fetched from TVMaze to calculate progress options, latest episodes, or updates.

When a user searches for a show, the app sends the search query to TVMaze and receives a list of possible matches. The app then ranks the results using TVMaze’s score, title matching, and show rating.

When a user saves a show, the app stores basic information in the library table, including its TVMaze ID, name, poster image, status, premiere date, current season, current episode, and whether the show is marked as finished. All of this is saved locally to keep as few requests to TVMaze as possible.

For the update-checking logic, the app fetches the show's episode list from TVMaze (ignoring episodes that haven't come out yet) and compares the new ones against the user's saved progress. If an aired episode comes after the user's saved progress then it's treated as a new update and displayed on the dashboard and updates page.

## Files and Project Structure
The main file is `app.py`, containing the Flask app, routes, and main logic that connects everything together. The routes `/`, `/search`, `/details`, `/library`, `/progress`, `/save`, `/remove`, and `/updates` are defined there.

The `helpers.py` file contains all helper functions I made to assist in logic handling to keep `app.py` organized. Some helper functions work with TVMaze episode data, ranking results, calculating progress related information, etc.

The `templates` folder contains the HTML files to be rendered by Flask. They use Jinja syntax to display dynamic data passed from the routes. The `static` folder contains the CSS file used for custom styling. SQLite database `app.db` stores the user's saved shows and progress, even after the server is stopped and restarted.

## Database Design
The main table is `library`. This table stores each show saved by the user. Each row represents one TV show in the user's library.
The `library` table includes:

- `id`: a local autoincrementing primary key
- `tvmaze_id`: the show's ID from TVMaze
- `name`: the show's name
- `image_url`: the show's poster image
- `status`: the show's status from TVMaze
- `premiered`: the show's premiere date
- `season`: the user's saved season progress
- `episode`: the user's saved episode progress
- `finished`: whether the show is marked as finished

The `tvmaze_id` column is especially important because it connects the local database record to the correct show in the TVMaze API. It is also used to prevent duplicate shows from being added to the library.

I decided not to store every episode in the database. Instead, the app fetches episode data from TVMaze when it needs to calculate progress options or check for updates. This keeps the database smaller and avoids saving a large amount of API data that can be requested again when needed.

## TVMaze API
I use TVMaze API as the external data source because it's free and provides endpoints for searching shows, fetching details, and getting episode lists without needing an API key. I use this API for the search page, details page, and update and progress logic. 

## Design Choices
I decided to keep the app single-user because adding authentication and user accounts would have made the project more complex without helping the main goal.

I also separated shows into Watching and Finished instead of deleting finished shows so that the user can see all shows watched and also easily undo changes. This was important because a show can be “finished” for the user temporarily but still release a new season in the future.

## Future Improvements
Possible future improvements include adding user accounts, reducing repeated API calls by caching episode data, adding a calendar view for upcoming episodes, and improving the search ranking system. I would also like to improve the aesthetics of the app by making it more card-based instead of table-based, as well as improving API efficiency and calls.

## How to Run
To run the project locally:
1. Clone or download the project.
2. Create and activate a virtual environment.
3. Install the required packages with `pip install -r requirements.txt`.
4. Run the Flask application with `flask run`.
5. Open the local server URL shown in the terminal.

The app uses SQLite, so the local database is created automatically when the application starts.
