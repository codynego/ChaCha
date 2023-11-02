# ChaCha API Documentation

The ChaCha API allows users to connect and have interesting conversations with other bored users. This comprehensive documentation provides detailed information about the available endpoints, authentication, user management, stories, feeds, messaging, secret keys, and token-based authentication.

## Endpoints

### Stories

#### Get a List of Stories

- **Endpoint:** `GET /api/stories/`
- **Description:** Retrieve a list of stories.
- **Authentication:** None required.
- **Request:**
  - None.

#### Create a New Story

- **Endpoint:** `POST /api/story/`
- **Description:** Create a new story.
- **Authentication:** Required.
- **Request:**
  - JSON body:
    ```json
    {
        "content": "Your story content here."
    }
    ```

#### Get Details of a Specific Story

- **Endpoint:** `GET /api/story/<int:pk>/`
- **Description:** Retrieve details of a specific story.
- **Authentication:** None required.
- **Request:**
  - None.

#### Create a New Text Story

- **Endpoint:** `POST /api/story/text/`
- **Description:** Create a new text story.
- **Authentication:** Required.
- **Request:**
  - JSON body:
    ```json
    {
        "text": "This is a sample text story."
    }
    ```

#### Create a New Image Story

- **Endpoint:** `POST /api/story/image/`
- **Description:** Create a new image story.
- **Authentication:** Required.
- **Request:**
  - Multipart form data with an image file.

#### Create a New Video Story

- **Endpoint:** `POST /api/story/video/`
- **Description:** Create a new video story.
- **Authentication:** Required.
- **Request:**
  - Multipart form data with a video file.

#### Get Reactions for a Specific Story

- **Endpoint:** `GET /api/story/reaction/<story_id>/`
- **Description:** Retrieve reactions for a specific story.
- **Authentication:** None required.
- **Request:**
  - None.

#### Create a Reaction for a Story

- **Endpoint:** `POST /api/story/reaction/`
- **Description:** Create a reaction for a story.
- **Authentication:** Required.
- **Request:**
  - JSON body:
    ```json
    {
        "story_id": 1,
        "reaction_type": "like"
    }
    ```

### Feeds

#### Get Interesting Feeds

- **Endpoint:** `GET /api/feeds/`
- **Description:** Get interesting feeds for bored users.
- **Authentication:** Required.
- **Request:**
  - None.

### Messaging

#### Get a List of Messages for a Specific Room

- **Endpoint:** `GET /api/messages/<str:room_id>/`
- **Description:** Retrieve a list of messages for a specific room.
- **Authentication:** Required.
- **Request:**
  - None.

#### Create a New Conversation

- **Endpoint:** `POST /api/conversations/`
- **Description:** Create a new conversation.
- **Authentication:** Required.
- **Request:**
  - JSON body:
    ```json
    {
        "participants": ["user_id1", "user_id2"],
        "subject": "Conversation subject"
    }
    ```

#### Get Details of a Specific Conversation

- **Endpoint:** `GET /api/conversation/<str:pk>/`
- **Description:** Retrieve details of a specific conversation.
- **Authentication:** Required.
- **Request:**
  - None.

### Secret Key

#### Get a Secret Key

- **Endpoint:** `GET /api/secretkey/`
- **Description:** Retrieve a secret key.
- **Authentication:** Required.
- **Request:**
  - None.

### Token-Based Authentication

#### Obtain an Access Token

- **Endpoint:** `POST /api/auth/token/`
- **Description:** Obtain an access token for authentication.
- **Authentication:** None required.
- **Request:**
  - JSON body:
    ```json
    {
        "username": "your_username",
        "password": "your_password"
    }
    ```

#### Refresh an Access Token

- **Endpoint:** `POST /api/auth/token/refresh/`
- **Description:** Refresh an access token.
- **Authentication:** None required.
- **Request:**
  - JSON body:
    ```json
    {
        "refresh": "your_refresh_token"
    }
    ```

#### User Registration and Verification

- **Register a New User:**
  - **Endpoint:** `POST /api/auth/user/register/`
  - **Description:** Register a new user.
  - **Authentication:** None required.
  - **Request:**
    - JSON body:
      ```json
      {
          "username": "new_user",
          "password": "new_password",
          "email": "user@example.com"
      }
      ```

- **Verify User's Email:**
  - **Endpoint:** `POST /api/auth/user/verify-email/`
  - **Description:** Verify the user's email.
  - **Authentication:** None required.
  - **Request:**
    - JSON body:
      ```json
      {
          "token": "your_verification_token"
      }
      ```

- **Resend Email Verification:**
  - **Endpoint:** `POST /api/auth/user/resend-verify-email/`
  - **Description:** Resend email verification.
  - **Authentication:** None required.
  - **Request:**
    - JSON body:
      ```json
      {
          "email": "user@example.com"
      }
      ```

### User Management

#### Get User Profile Information

- **Endpoint:** `GET /api/user/me/`
- **Description:** Get user profile information.
- **Authentication:** Required.
- **Request:**
  - None.

#### Update User Profile Information

- **Endpoint:** `PUT /api/user/me/`
- **Description:** Update user profile information.
- **Authentication:** Required.
- **Request:**
  - JSON body:
    ```json

        {
        "first_name": "New First Name",
        "last_name": "New Last Name",
        "bio": "New Bio",
        "profile_picture": "Updated Profile Picture (Multipart Form Data)",
        "interests": ["interest1", "interest2"]
    }
    ```

#### Follow Another User

- **Endpoint:** `POST /api/user/follow/`
- **Description:** Follow another user.
- **Authentication:** Required.
- **Request:**
  - JSON body:
    ```json
    {
        "user_id": "user_to_follow_id"
    }
    ```

#### Unfollow Another User

- **Endpoint:** `POST /api/user/unfollow/`
- **Description:** Unfollow another user.
- **Authentication:** Required.
- **Request:**
  - JSON body:
    ```json
    {
        "user_id": "user_to_unfollow_id"
    }
    ```

#### Post a Review for a User

- **Endpoint:** `POST /api/user/review/`
- **Description:** Post a review for a user.
- **Authentication:** Required.
- **Request:**
  - JSON body:
    ```json
    {
        "user_id": "user_to_review_id",
        "rating": 5,
        "comment": "A great user!"
    }
    ```

#### Get a List of Followers

- **Endpoint:** `GET /api/user/followers/`
- **Description:** Get a list of followers for the user.
- **Authentication:** Required.
- **Request:**
  - None.

#### Get a List of Users Being Followed

- **Endpoint:** `GET /api/user/following/`
- **Description:** Get a list of users that the user is following.
- **Authentication:** Required.
- **Request:**
  - None.

#### Add or Remove Interests

- **Endpoint:** `POST /api/user/interest/`
- **Description:** Add or remove interests for the user.
- **Authentication:** Required.
- **Request:**
  - JSON body:
    ```json
    {
        "interests": ["new_interest1", "new_interest2"]
    }
    ```

This documentation serves as a comprehensive guide to using the BoredChat API. Make authenticated requests with the obtained tokens and provide necessary data in the request bodies for the respective endpoints.

If you have any questions or need further assistance, please contact our support team.

