const passport = require('passport');
const LocalStrategy = require('passport-local').Strategy;
const bcrypt = require('bcrypt');
const getAuthCredentials = require('../models/auth/getAuthCredentials');
const getUserById = require('../models/auth/getUserById');
const createUser = require('../models/auth/createUser');

passport.use(new LocalStrategy(
    {usernameField: 'email', passwordField: 'password'},
    async function verify(username, password, cb) {
    try {        
        const user = await getAuthCredentials(username);
        if(user.length <= 0) {
            return cb(null, false, { message: 'Incorrect username or password' })
        } else {
            bcrypt.compare(password, user[0].password, function (err, check) {
                if(err) {
                    return cb()
                } else if (check) {
                    return cb(null, { userId: user[0].user_id });
                } else {
                    return cb(null, false);
                }
            })
        }
    } catch (err) {
        cb(err);
    }
}));

passport.serializeUser(function(user, done) { 
    done(null, user.userId);
})

passport.deserializeUser(async function(user_id, done) {
    try {
        const user = await getUserById(user_id);
        user.user_id = user_id;
        done(null, user);
    } catch(err) {
        console.log(err);
    }
})

const signinLocal = async (req, res) => {
    try {
        const user = await getUserById(req.user.userId);
        res.status(200).send({message: 'Successfully logged in', data: user });
    } catch (err) {
        res.status(400).send({message: 'Could not find the user details after logging in', data: {}})
    }
    
}

const signupLocal = async (req, res, next) => {
    try {
        const { email, password } = req.body;
        const salt = await bcrypt.genSalt(8);
        const hash = await bcrypt.hash(password, salt);
        const users = await createUser(email, hash);
        req.login({ userId: users[0].user_id }, async (err) => {
            if(err) {
                console.log(err)
            } else {
                //get the user
                const user = await getUserById(users[0].user_id) 
                res.status(201).send({
                    message: 'User created',
                    data: user
                });
            }
        }) 
    } catch(err) {
        res.status(401).send({message: 'Failed to create user', data: {}})
        console.log(err);
    }      
}

const logout = (req, res, next) => {
    req.logout((err) => {
        if(err) {
            next(err)
        } else {
            res.status(200).send({ message: 'User has been logged out', data: {}})
        }
    })
}

module.exports = {
    signupLocal,
    logout,
    signinLocal
}