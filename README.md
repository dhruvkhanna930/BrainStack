# Brainstack

Brainstack is a collaborative communication platform inspired by Discord. It provides users with a seamless environment for interaction, enabling them to create custom rooms, join video channels, edit profiles, share files, and more. This platform caters to a diverse user base, from casual social groups to professional teams, emphasizing user-friendliness and accessibility.

## Features

- Create custom rooms
- Join video channels
- Edit profiles
- Share files
- User-friendly interface

## Project Reports

  ### [Design Report](DesignReport.pdf)

  ### [Feasibility Report](FeasibilityReport.pdf)

  ### [Estimation Report](EstimationReport.pdf)

## Setup

Follow these steps to set up the project locally:

### Prerequisites

- Python 3.x installed
- pip package manager
- virtualenv (optional but recommended)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/brainstack.git
   ```

2. Navigate to the project directory:
   ```bash
   cd brainstack
   ```

3. Create a virtual environment (optional but recommended):
   ```bash
   virtualenv venv
   ```

4. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```bash
     source venv/bin/activate
     ```

5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

6. Set up environment variables:
   Create a `.env` file in the root directory and add the following variables:
   ```
   SECRET_KEY=your_secret_key_here
   DEBUG=True
   ```

   Then run the following command:
   ```bash
   source .env

### Running the Server

1. Ensure you are in the project directory and the virtual environment is activated.

2. Run the following command:
   ```bash
   python manage.py runserver
   ```
   If above command do not work, run this:
   ```bash
   python3 manage.py runserver
   ```
   

4. The development server will start running. Access the application at `http://localhost:8000` in your web browser.

## Screenshots
<div align="center">
    <img src="https://github.com/dhruvkhanna930/BrainStack/blob/main/ScreenShots/01_HomePage.png" alt="Photo 1" width="450"/>
    <img src="https://github.com/dhruvkhanna930/BrainStack/blob/main/ScreenShots/02_UserProfile.png" alt="Photo 2" width="450"/>
    <img src="https://github.com/dhruvkhanna930/BrainStack/blob/main/ScreenShots/03_RoomPage.png" alt="Photo 3" width="450"/>
    <img src="https://github.com/dhruvkhanna930/BrainStack/blob/main/ScreenShots/04_VideoRoom.png" alt="Photo 4" width="450"/>
    <img src="https://github.com/dhruvkhanna930/BrainStack/blob/main/ScreenShots/05_VideoRoomDashboard.png" alt="Photo 5" width="450"/>
    <img src="https://github.com/dhruvkhanna930/BrainStack/blob/main/ScreenShots/06_FIleShareDashboard.png" alt="Photo 6" width="450"/>
    <img src="https://github.com/dhruvkhanna930/BrainStack/blob/main/ScreenShots/07_DownloadFilePage.png" alt="Photo 7" width="450"/>
    <img src="https://github.com/dhruvkhanna930/BrainStack/blob/main/ScreenShots/08_CreateRoom.png" alt="Photo 8" width="450"/>
    <img src="https://github.com/dhruvkhanna930/BrainStack/blob/main/ScreenShots/09_BrowseTopics.png" alt="Photo 9" width="450"/>
    <img src="https://github.com/dhruvkhanna930/BrainStack/blob/main/ScreenShots/10_EditPprofile.png" alt="Photo 10" width="450"/>
</div>


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
