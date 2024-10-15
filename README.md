# JUST FORMS AND SONGS (JFAS)

## Description
**Just Forms and Songs** (JFAS) is a fan game inspired by *Just Shapes & Beats* (JSAB), built entirely in Python. While it's still a work in progress and currently in a barely playable state, any form of support or feedback is greatly appreciated to help shape this project and maybe even give me time to continue my other works.

## Roadmap

### Core Features
- [x] **Player Movement**  
- [ ] **Gameplay Mechanics**  
	- Obstacles:
		- [x] Laser
		- [x] Beeg laser
		- [x] Squares
		- [x] Circles
		- [ ] Square particles
		- [ ] Circle particles
		- [ ] Clash squares
		- [ ] Clash circles
		- [ ] Weird squares from *Cheat Codes* (TBD)
		- [ ] Image-based objects (bosses, etc.)
		- [ ] Hollow saws
		- [ ] Full saws
		- [ ] Lunar whale-like obstacles (both groups of 8 and individuals)
		- [ ] **Conveyor Belts**
	- [x] Level loading
	- [ ] Autoscroll™  
- [ ] **Smooth Animations**  
- [ ] **Level Editor**  
- [ ] **In-Game Menu**  
	- Replace the current quick-and-dirty PySide6 loader with a proper in-game menu system.

## How to Build

1. **Clone the Repository:**  
   Download the repository to your machine. *(Real shit sherlock?)*

2. **Install Python:**  
   If you haven't already, install Python and be sure to check the "Add to PATH" option during installation.

3. **Install Requirements:**  
   Open a terminal or command prompt and run the following command to install the necessary packages:
   ```bash
   python -m pip install pyinstaller pygame PySide6
   ```

4. **Build the Project:**  
   Navigate to the folder where the files are located and run the following command:
   ```bash
   pyinstaller JustFormsAndSongs.spec
   ```
   Wait for the build process to complete.

5. **Prepare Assets:**  
   Copy the entire `vanilla` folder (except the `obstacles` folder) into the `dist` directory.

6. **Move Icons:**  
   Copy `icon1.png` and `icon2.png` to the same `dist` directory.

7. **You're Done!**  
   The final build can be found in the `dist` directory. Congratulations, you've successfully built the steaming pile of trash that is this cheap knockoff copy of something better.
