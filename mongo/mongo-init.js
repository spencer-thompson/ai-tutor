db.createUser({
  user: "newuser",
  pwd: "newpassword",
  roles: [
    {
      role: "readWrite",
      db: "yourdatabase",
    },
  ],
});
