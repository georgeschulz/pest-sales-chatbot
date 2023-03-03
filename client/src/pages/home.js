import { Link } from 'react-router-dom'

function Home() {
    return (
        <div>
            <h1 className='text-xl font-semibold'>Home</h1>
            <Link to="/login" className='underline'>Login</Link>
        </div>
    )
}

export default Home