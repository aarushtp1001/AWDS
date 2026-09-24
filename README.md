# Astronomical Weather Database System AWDS (nasa-space-pipeline)
## What It Does
This database system uses NASA's APIs to fetch asteroid and solar flare data. Then, it feeds the relevant data into an SQLite database. After creating the tables in the database, the system provides the user with specialized functions and SQL commands that he/she can perform on the database.
## Features
The features of AWDS are:
- **1.** View general space weather statistics.
- **2.** Search asteroids using speed factor.
- **3.** Search asteroids using miss-distance factor.
- **4.** View potentially hazardous asteroids (sorted by miss-distance).
- **5.** Search solar flares according to class/region/location.
- **6.** Find all potentially hazardous asteroids that happened to pass by close to Earth when a dangerous (X-Class or M-Class) solar flare occurred.
