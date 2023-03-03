const session = require('express-session'); //creates a session
const path = require('path');
require('dotenv').config({ path: path.resolve(__dirname, '../.env') })

//configure the connect to the database
const conObject = {
    user: process.env.USER,
    host: process.env.HOST,
    database: process.env.DATABASE,
    password: process.env.DATABASEPASSWORD,
    port: process.env.DATABASEPORT,
    //ssl is not run in localhost but is necessary for stripe, so we need to conditionally use it based on environment
    ssl: process.env.NODE_ENV === 'production' ? { rejectUnauthorized: false } : false
}

//create a store object referencing the sessions table in the database. To allows a user's session to persist based on cookie data. Customer id is serialized into the db sessions table with the session id. Then the customer id is deserialized by passport automatically in requests giving direct access to a user's object with their info
const store = new (require('connect-pg-simple')(session))({
    conObject
})

//export the store to be rolled into express sessions middleware implementation in app.js
module.exports = store;