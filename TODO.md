# Backend for Frontend.html with MongoDB Integration

## Plan Summary
- Create a Node.js backend using Express to connect Frontend.html to MongoDB for user details storage.
- Replace Firebase/Firestore with MongoDB for user authentication and data storage.

## Steps to Complete

### 1. Set Up Backend Structure
- [x] Create backend directory
- [x] Create package.json with dependencies (Express, Mongoose, bcrypt, cors, dotenv)
- [x] Create app.js (main Express application)
- [x] Create models/User.js (MongoDB User model)
- [x] Create routes/auth.js (authentication routes)

### 2. Implement Backend Logic
- [x] Set up MongoDB connection in app.js
- [x] Define User schema with name, email, password (hashed)
- [x] Implement /register endpoint (create user, hash password)
- [x] Implement /login endpoint (authenticate user, return token or session)
- [x] Add middleware for authentication if needed

### 3. Modify Frontend
- [ ] Update Frontend.html JavaScript to remove Firebase dependencies for auth
- [ ] Replace signup form submission to call /register endpoint
- [ ] Replace login form submission to call /login endpoint
- [ ] Handle authentication state without Firebase

### 4. Setup and Testing
- [ ] Install Node.js dependencies
- [ ] Set up MongoDB database (local or MongoDB Atlas)
- [ ] Run the backend server
- [ ] Test user registration and login via frontend
- [ ] Verify data storage in MongoDB

## Notes
- Ensure password security with bcrypt hashing
- Handle CORS for frontend-backend communication
- Consider using JWT for session management
- Test thoroughly to ensure seamless integration
