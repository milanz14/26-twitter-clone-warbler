# Research and Understanding Login Strategy

1. How is the logged in user being kept track of? 
   - the user's ID is being stored in the session as CURR_USER_KEY
  
2. What is Flask's `g` object?
   - Flask's `g` object refers to a global namespace for holding any data during a single app context. This allows passing information, like a logged in user, to other routes and functions. An app context lasts for one request/response cycle, `g` is not approviate for storing data across requests.

3. What is the purpose of `add_user_to_g`?
   - The purpose is to be able to share the user data to be able to share it with any route during each route's req/res cycle. It's based on the user that is stored in session and prevents having to write logic for each route as well as having to pass the user's ID into the URL params for each route.

4. What does `@app.before_request` mean?
   - this decoractor allows a function to run before each req/res cycle. This is ideal for tasks such as opening database connections, loading a user from the session, working with the flask `g` object.