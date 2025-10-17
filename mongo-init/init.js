db = db.getSiblingDB('appdb');
db.createUser({
  user: 'intanchris',
  pwd: 'sdt25',
  roles: [{ role: 'readWrite', db: 'appdb' }]
});