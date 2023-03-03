import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { endpoint }  from '../config/apiConfig';
import axios from 'axios';

const userFromLocalStorage = () => {
    const user = localStorage.getItem('user');
    return user && JSON.parse(user);
}

const userSlice = createSlice({
    name: "user",
    initialState: {
        user: userFromLocalStorage() || null,
        email: '',
        password: ''
    },
    reducers: {
        setUser: (state, action) => {
            state.user = action.payload;
        },
        setLoginEmail: (state, action) => {
            state.email = action.payload;
        },
        setLoginPassword: (state, action) => {
            state.password = action.payload;
        }
    },
    extraReducers: (builder) => {
        builder
            .addCase(login.fulfilled, (state, action) => {
                state.user = action.payload.data;
                localStorage.setItem('user', JSON.stringify(action.payload.data));
            })
            .addCase(logout.fulfilled, (state, action) => {
                localStorage.removeItem('user');
                state.user = null;
            })
    }
});

export const login = createAsyncThunk(
    "user/login",
    async (payload, thunkAPI) => {
        try {
            const { email, password } = payload;
            const response = await axios.post(`${endpoint}/auth/login`, {
                email,
                password
            });
            const user = response.data.data;
            thunkAPI.dispatch(setUser(user));
            return response.data;
        } catch (err) {
            return thunkAPI.rejectWithValue(err.response.data);
        }
    }
);

export const logout = createAsyncThunk(
    "user/logout",
    async (payload, thunkAPI) => {
        try {
            const response = await axios.post(`${endpoint}/auth/logout`);
            thunkAPI.dispatch(setUser(null));
            return response.data;
        } catch (err) {
            return thunkAPI.rejectWithValue(err.response.data);
        }
    }
);

export const { setUser, setLoginEmail, setLoginPassword } = userSlice.actions;
export const selectUser = (state) => state.user.user;
export const selectIsAuth = (state) => state.user.user !== null;
export const selectLoginEmail = (state) => state.user.email;
export const selectLoginPassword = (state) => state.user.password;
export default userSlice.reducer;