import { useSelector, useDispatch } from "react-redux"
import { useNavigate } from "react-router-dom"
import { selectLoginEmail, selectLoginPassword } from "../redux/slices/userSlice"
import { setLoginEmail, setLoginPassword } from "../redux/slices/userSlice"
import { login } from "../redux/slices/userSlice"
import TextField from '@mui/material/TextField';

function LoginPage() {
    const dispatch = useDispatch()
    const email = useSelector(selectLoginEmail)
    const password = useSelector(selectLoginPassword)
    const navigate = useNavigate()

    const handleSubmit = async (e) => {
        e.preventDefault()
        await dispatch(login({ email, password }))
        navigate("/dashboard")
    }

    //make a basic login form that dispatches the login thunk
    return (
        <div className="flex justify-center pt-60">
            <div>
                <h1 className="text-2xl semibold mb-5 text-center">Login</h1>
                <form onSubmit={handleSubmit} className="flex flex-wrap justify-center gap-y-4">
                    <TextField
                        id="outlined-basic"
                        label="Email"
                        variant="outlined"
                        type="email"
                        value={email}
                        onChange={(e) => dispatch(setLoginEmail(e.target.value))}
                        className="w-full mb-5"
                    />
                    <TextField
                        id="outlined-basic"
                        label="Password"
                        variant="outlined"
                        type="password"
                        value={password}
                        onChange={(e) => dispatch(setLoginPassword(e.target.value))}
                        className="w-full mb-5"
                    />
                    <button
                        type="button"
                        onClick={handleSubmit}
                        className="bg-slate-500 text-white py-2 px-4"
                    >
                        Login
                    </button>

                </form>
            </div>
        </div >
    )
}

export default LoginPage