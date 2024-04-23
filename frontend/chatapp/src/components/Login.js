import React, { useEffect, useState } from 'react'
import './style.css'
import { Link } from 'react-router-dom'
import { useNavigate } from 'react-router-dom'
import axios from 'axios';


function Login() {
    const [username, setUserName] = useState('')
    const [password, SetPassword] = useState('')
    const navigate = useNavigate();
    const [error, setError] = useState('');

    useEffect(() => {
        let access_token = localStorage.getItem("access_token")
        if (access_token) {
            navigate('/home');
        }
    }, [])

    const handleLogin = async () => {
        try {
            console.log('111111111111111111')
            const response = await axios.post('http://127.0.0.1:8000/api/login_user/', {
                username: username,
                password: password
            });

            const data = response.data;
            // Kiểm tra xem có access_token trong phản hồi hay không
            if (data && data.access_token) {
                localStorage.setItem('access_token', data.access_token);
                localStorage.setItem('username',data.user_data.username);
                console.log(data.user_data.avatar)
                localStorage.setItem('avatar',data.user_data.avatar);
            } else {
                // Xử lý trường hợp không có access_token trong phản hồi
                setError('Không có access_token trong phản hồi từ máy chủ');
            }
        } catch (error) {
            // Xử lý lỗi nếu có lỗi xảy ra khi gửi yêu cầu
            console.error('Error during login:', error);
            setError('Đã xảy ra lỗi khi đăng nhập');
        }
    };
    

    return (
        <div className='login template d-flex justify-content-center align-items-center vh-100 bg-primary'>
            <div className='form_container p-5 rounded bg-white'>
                <form>
                    <h3 className='text-center'>Sign In</h3>
                    <div className='mb-2'>
                        <label htmlFor='username'>Username</label>
                        <input type='text' placeholder='Enter Username' className='form-control' value={username} onChange={(event) => setUserName(event.target.value)}></input>
                    </div>
                    <div className='mb-2'>
                        <label htmlFor='password'>Password</label>
                        <input type='password' placeholder='Enter Password' className='form-control' value={password} onChange={(event) => SetPassword(event.target.value)}></input>
                    </div>
                    <div>
                        <input type='checkbox' className='custom-control custom-checkbox' id="check" />
                        <label htmlFor='check' className='custom-input-label ms-2'>
                            Remember me
                        </label>
                    </div>
                    <div className='d-grid'>
                        <button className='btn btn-primary' onClick={() => handleLogin()}>Sign in</button>
                    </div>
                    <p className='text-end mt-2'>
                        Forgot <a href=''>Password?</a>
                        <Link to='/signup' className='ms-2'>Sign up</Link>
                    </p>
                </form>
            </div>
        </div>
    )
}

export default Login;
