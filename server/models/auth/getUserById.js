const db = require('../db');

module.exports = async (userId) => {
    try {
        const { rows } = await db.query(`SELECT * FROM users WHERE users.user_id = $1;`, [userId]);
        delete rows[0].password;
        return rows[0];
    } catch (err) {
        throw err;
    }
}