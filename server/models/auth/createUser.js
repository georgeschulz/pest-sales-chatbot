const db = require('../db');

module.exports = async (username, hashedPassword) => {
    try { 
        const users = await db.query(`INSERT INTO users (email, password) VALUES ($1, $2) RETURNING *`, [username, hashedPassword])
        return users.rows
    } catch (err) {
        throw err;
    }
}