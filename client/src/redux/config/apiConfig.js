export const endpoint = 
    process.env.NODE_ENV === "production"
        ? "https://gstemplateapp.herokuapp.com/api"
        : "http://localhost:4001/api";