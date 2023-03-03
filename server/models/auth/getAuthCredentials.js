const db = require('../db');

module.exports = async (email) => {
    try {
        const { rows } = await db.query(`SELECT email, password, user_id FROM users WHERE email = $1;`, [email]);
        return rows;
    } catch (err) {
        throw err;
    }
}