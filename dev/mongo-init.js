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
db.users.insertMany([
  { name: "Alice", age: 25, city: "New York" },
  { name: "Bob", age: 30, city: "San Francisco" },
  { name: "Charlie", age: 35, city: "Los Angeles" },
]);

print("Users inserted into aitutor database");

// Insert a test API key into the keys collection, replacing if it exists
db.keys.updateOne(
  { apiKey: "test_key" },
  { $set: { description: "This is a test API key" } },
  { upsert: true },
);
print("Test API key upserted into aitutor database");
