var rootDBUser = process.env["MONGO_INITDB_ROOT_USERNAME"];
var rootDBPassword = process.env["MONGO_INITDB_ROOT_PASSWORD"];
var dbPassword = process.env["DBPASSWORD"];
var dbUser = process.env["DBUSER"];
var dbName = process.env["DBNAME"];

db.auth(rootDBUser, rootDBPassword);

db = db.getSiblingDB(dbName);

db.createUser({
  user: dbUser,
  pwd: dbPassword,
  roles: [{ role: "dbOwner", db: dbName }],
});
