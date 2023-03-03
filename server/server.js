const express = require('express')
const app = express()
const path = require('path')
const morgan = require('morgan')

//routers import
const authRouter = require('./routes/auth');

const passport = require('passport')
const session = require('express-session')
require('dotenv').config({ path: path.resolve(__dirname, '../.env') })
const port = process.env.PORT || 4000
const store = require('./models/store')

const cors = require('cors');
app.use(express.urlencoded({ extended: true }));
app.use(express.static('public'));
app.use(express.static('../client/build'));
app.use(express.json());
app.use(cors({ credentials: true, origin: 'http://localhost:3000' }))
app.use(morgan('dev'));

app.use(session({
    store: store,
    secret: process.env.SESSIONSECRET,
    cookie: {
        maxAge: 172000000,
        httpOnly: process.env.NODE_ENV === 'production' ? true : false,
        sameSite: 'lax'
    },
    saveUninitialized: true,
    resave: false,
    sameSite: 'none',
    secure: process.env.NODE_ENV === 'production' ? true : false
}))

app.use(passport.initialize());
app.use(passport.session());

//routes
app.use('/api/auth', authRouter);

//general path for getting static pages
app.get("/*", (req, res) => {
    if(process.env.NODE_ENV === 'production') {
        res.sendFile(path.join(__dirname, "../client/build", "index.html"), (err) => {
            if(err) {
                console.log('Incorrect path');
                res.status(500).send()
            }
        });
    } else {
        res.redirect('https://localhost:3000/');
    }
})

app.listen(port, () => {
    console.log(`Server is running on port ${port}`)
})