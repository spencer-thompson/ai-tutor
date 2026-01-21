// This script is run automatically by the mongo container on first-time startup.
// It sets up a dedicated application user and the necessary collections and data for development.

// --- Configuration (Hardcoded for simplicity) ---
// These values should match what the application expects in a development environment.
const appDbName = "aitutor";
const appUser = "user";
const appPass = "pass";
const devApiKey = "XoPYsOSwSf786Ky_P0DlbrxPnW9qmPvwIhhD9tGKooo";

// --- User Creation ---
// The script is run as root before authentication is enabled.
// We switch to the 'admin' database to create the application user.
db = db.getSiblingDB("admin");

const userExists = db.system.users.countDocuments({ user: appUser });

if (userExists === 0) {
  db.createUser({
    user: appUser,
    pwd: appPass,
    // Grant read/write access ONLY to the application's database for security.
    roles: [{ role: "readWrite", db: appDbName }],
  });
  print(`[mongo-init] Created application user '${appUser}'.`);
} else {
  print(
    `[mongo-init] Application user '${appUser}' already exists. Skipping creation.`,
  );
}

// --- Database and Collection Setup ---
// Switch to the application database.
// The MONGO_INITDB_DATABASE env var in docker-compose should be set to this value.
const appDb = db.getSiblingDB(appDbName);

// Ensure all required collections exist.
const requiredCollections = ["catalog", "courses", "keys", "users"];

requiredCollections.forEach((coll) => {
  if (!appDb.getCollectionNames().includes(coll)) {
    appDb.createCollection(coll);
    print(`[mongo-init] Created collection: '${coll}'.`);
  }
});

// --- Development Data Seeding ---
// Clear the users collection for a fresh start in case the volume persists but is being re-initialized.
appDb.users.deleteMany({});
print("[mongo-init] Cleared all documents from 'users' collection.");

// Upsert the development API key used by the browser extension.
// NEVER CHANGE DB WITHOUT CLEAR COMMUNICATION FIRST
appDb.keys.updateOne(
  { key: devApiKey },
  {
    $set: {
      key: devApiKey,
      description: "Development API key for browser extension",
    },
  },
  { upsert: true },
);

devKeyObj = {};
devKeyObj[devApiKey] = "Development API key for browser extension";
appDb.keys.updateOne(
  { key: devApiKey },
  {
    $set: devKeyObj,
  },
  { upsert: true },
);

print("[mongo-init] Upserted development API key into 'keys' collection.");

print(`\n[mongo-init] Database '${appDbName}' is ready for development.`);
print(
  '[mongo-init] Note: To populate the "catalog" collection, run mongoimport as shown in data/README.md.',
);
