# Course 2 Week 2: Batch Data Processing from API

## 📋 Assignment Overview

This assignment focuses on learning how to interact with the Spotify API and extract data in a batch way. You'll explore pagination, API authorization, and building a complete batch data pipeline.

## 🎯 Learning Objectives

- Understand API authentication and token management
- Learn pagination techniques for API requests
- Build a batch data processing pipeline
- Handle token refresh for long-running processes
- Work with Spotify Web API endpoints

## 📁 Project Structure

```
week2/
├── C2_W2_Assignment.ipynb    # Main assignment notebook
├── src/
│   ├── authentication.py     # Token authentication functions
│   ├── endpoint.py           # API endpoint functions (with exercises)
│   ├── main.py               # Main pipeline script (with exercises)
│   └── env                   # Environment variables (CLIENT_ID, CLIENT_SECRET)
├── images/                   # Screenshots and diagrams
└── README.md                 # This file
```

## 🚀 Quick Start

### Prerequisites

1. **Spotify Developer Account**: Create an account at https://developer.spotify.com/
2. **Create Spotify App**:
   - App name: `dec2w2a1-spotify-app`
   - Redirect URIs: `http://127.0.0.1:3000`
   - API: `Web API`
3. **Get Credentials**: Copy `Client ID` and `Client secret` from app settings

### Setup

1. **Configure Environment**:
   ```bash
   cd src
   # Edit env file and add your credentials:
   # CLIENT_ID=your_client_id_here
   # CLIENT_SECRET=your_client_secret_here
   ```

2. **Install Dependencies** (if needed):
   ```bash
   pip install requests python-dotenv
   ```

3. **Run the Pipeline**:
   ```bash
   cd src
   python main.py
   ```

## 📚 Exercises Summary

### Exercise 1: Get New Releases
- Complete `get_new_releases()` function
- Learn basic API GET requests
- Understand response structure

### Exercise 2: Pagination with Offset
- Create `paginated_new_releases()` function
- Implement pagination using offset/limit
- Handle total elements and page iteration

### Exercise 3: Pagination with Next URL
- Create `paginated_with_next_new_releases()` function
- Use `next` field from API response
- Compare with offset-based pagination

### Exercise 4: Token Refresh (✅ Completed)
- Implement token refresh in `get_paginated_new_releases()`
- Handle 401 Unauthorized errors
- Auto-refresh expired tokens

### Exercise 5: Album Tracks Endpoint (✅ Completed)
- Complete `get_paginated_album_tracks()` function
- Build album tracks URL endpoint
- Implement pagination and token refresh

### Exercise 6: Main Pipeline (✅ Completed)
- Complete function call in `main.py`
- Connect all components together
- Run full batch extraction pipeline

### Exercise 7: Spotipy SDK (Optional)
- Use Spotipy SDK for pagination
- Compare SDK vs manual API calls

## 🔧 Key Concepts

### API Authentication
- Client Credentials Flow
- Access tokens (expire after 3600 seconds)
- Authorization headers: `Bearer {token}`

### Pagination
Two methods:
1. **Offset-based**: Manually increment offset by limit
2. **Next URL**: Use `next` field from API response

### Token Refresh
- Monitor for 401 status codes
- Automatically refresh tokens
- Retry failed requests

### Batch Pipeline Flow
```
1. Get access token
2. Fetch all new album releases (paginated)
3. Extract album IDs
4. For each album ID:
   - Fetch all tracks (paginated)
   - Handle token refresh if needed
5. Save results to JSON file
```

## 📖 API Endpoints Used

- **Token**: `https://accounts.spotify.com/api/token`
- **New Releases**: `https://api.spotify.com/v1/browse/new-releases`
- **Album Tracks**: `https://api.spotify.com/v1/albums/{album_id}/tracks`

## 📝 Notes

- Token expires after 3600 seconds (1 hour)
- Rate limits: ~60 requests per minute (rolling 30-second window)
- Default pagination: 20 items per page
- Total new releases: ~100 albums

## ✅ Completed Exercises

The following exercises have been completed in the code:
- ✅ Exercise 4: Token refresh mechanism
- ✅ Exercise 5: Album tracks pagination
- ✅ Exercise 6: Main pipeline integration

## 🔗 Resources

- [Spotify Web API Documentation](https://developer.spotify.com/documentation/web-api)
- [Get New Releases Endpoint](https://developer.spotify.com/documentation/web-api/reference/get-new-releases)
- [Get Album Tracks Endpoint](https://developer.spotify.com/documentation/web-api/reference/get-an-albums-tracks)
- [Spotipy SDK Documentation](https://spotipy.readthedocs.io/)

## 🎓 Next Steps

1. Complete Exercises 1-3 in the notebook
2. Test the completed pipeline (Exercises 4-6)
3. Try the optional Spotipy SDK exercise
4. Experiment with rate limiting and error handling

