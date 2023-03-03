const controllers = require('../controllers/auth');
const router = require('express').Router();
const passport = require('passport');

router.post('/register', controllers.signupLocal);
router.post('/login', passport.authenticate('local'), controllers.signinLocal);
router.post('/logout', controllers.logout);

module.exports = router;