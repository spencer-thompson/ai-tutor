// Connect to admin database and create an admin user
db = db.getSiblingDB("admin");

if (db.system.users.find({ user: "user" }).count() === 0) {
  db.createUser({
    user: "user",
    pwd: "pass",
    roles: [{ role: "userAdminAnyDatabase", db: "admin" }],
  });
  print("Admin user created");
}

// Switch to aitutor database
db = db.getSiblingDB("aitutor");

// Insert users into the users collection
db.users.deleteMany({});

print("Deleted Users");

// Insert a test API key into the keys collection, replacing if it exists
db.keys.updateOne(
  { test_key: "This is the first api key for the AI Tutor project" },
  { $set: { description: "This is a test API key" } },
  { upsert: true },
);
print("Test API key upserted into aitutor database");
