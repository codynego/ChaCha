# ChaCha API Documentation

The ChaCha API allows users to connect and have interesting conversations with other bored users. 

This README provides an overview of the available endpoints and their functionality.

## Endpoints

The following are the available endpoints for the BoredChat API:

### Stories

- **GET /api/stories/**
  - Get a list of stories.
- **POST /api/story/**
  - Create a new story.
- **GET /api/story/<int:pk>/**
  - Get details of a specific story.
- **POST /api/story/text/**
  - Create a new text story.
- **POST /api/story/image/**
  - Create a new image story.
- **POST /api/story/video/**
  - Create a new video story.
- **GET /api/story/reaction/<story_id>/**
  - Get reactions for a specific story.
- **POST /api/story/reaction/**
  - Create a reaction for a story.

### Feeds

- **GET /api/feeds/**
  - Get interesting feeds for bored users.

### Messaging

- **GET /api/messages/<str:room_id>/**
  - Get a list of messages for a specific room.
- **POST /api/conversations/**
  - Create a new conversation.
- **GET /api/conversation/<str:pk>/**
  - Get details of a specific conversation.

### Secret Key

- **GET /api/secretkey/**
  - Get a secret key.

### Authentication

- **POST /api/auth/token/**
  - Obtain an access token.
- **POST /api/auth/token/refresh/**
  - Refresh an access token.
- **POST /api/auth/user/register/**
  - Register a new user.
- **POST /api/auth/user/verify-email/**
  - Verify the user's email.
- **POST /api/auth/user/resend-verify-email/**
  - Resend email verification.

### User Management

- **GET /api/user/me/**
  - Get user profile information.
- **PUT /api/user/me/**
  - Update user profile information.
- **POST /api/user/follow/**
  - Follow another user.
- **POST /api/user/unfollow/**
  - Unfollow another user.
- **POST /api/user/review/**
  - Post a review for a user.
- **GET /api/user/followers/**
  - Get a list of followers.
- **GET /api/user/following/**
  - Get a list of users being followed.
- **POST /api/user/interest/**
  - Add or remove interests.

## Authentication

- Token-based authentication is used for user access to protected endpoints.
- To obtain an access token, use the `/auth/token/` endpoint.
- To refresh an access token, use the `/auth/token/refresh/` endpoint.
- Include the token in the Authorization header for authenticated requests.

## User Registration and Verification

- Users can register using the `/auth/user/register/` endpoint.
- Email verification is required and can be initiated using `/auth/user/verify-email/`.
- Resend verification emails using `/auth/user/resend-verify-email/`.

## User Management

- Manage user profiles using `/user/me/`.
- Follow or unfollow other users with `/user/follow/` and `/user/unfollow/`.
- Post reviews for users using `/user/review/`.
- Retrieve followers and users being followed with `/user/followers/` and `/user/following/`.
- Add or remove interests using `/user/interest/`.
