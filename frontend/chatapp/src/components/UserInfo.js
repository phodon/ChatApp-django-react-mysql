import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

function UserInfoPage() {
    const [userInfo, setUserInfo] = useState({});
    const [formData, setFormData] = useState({
        address: '',
        phone: '',
        avatar: '',
    });

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSave = async (e) => {
        e.preventDefault();
        try {
            const formDataToSend = new FormData();
            formDataToSend.append('address', formData.address);
            formDataToSend.append('phone', formData.phone);
            console.log({'avatar':formData.avatar})
            if (formData.avatar!='') {
                formDataToSend.append('avatar', formData.avatar);
            }

            const response = await axios.post('/api/user_update/', formDataToSend, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('access_token')}`
                }
            });
            localStorage.setItem('avatar', response.data.avatar);
            fetchUserInfo()
        } catch (error) {
            console.error('Registration error:', error.response.data);
        }
    };

    const handleAvatarChange = (e) => {
        const file = e.target.files[0];
        if (file) {
            setFormData({ ...formData, avatar: file });
        }
    };

    const fetchUserInfo = async () => {
        try {
            const response = await axios.get(`/api/user_info/`, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('access_token')}`
                }
            });
            setUserInfo(response.data);
            console.log(userInfo)
        } catch (error) {
            console.error('Error fetching user info:', error);
        }
    };

    useEffect(() => {
        fetchUserInfo();
    }, []);

    return (
        <div className='signup template d-flex justify-content-center align-items-center vh-100 bg-primary'>
            <div className='form_container p-5 rounded bg-white'>
                <div className="text-center">
                    <img src={userInfo.avatar} alt="Avatar" className="avatar-img" />
                    <h3>{userInfo.username}</h3>
                </div>
                <form onSubmit={handleSave}>

                    <div className='mb-2'>
                        <label htmlFor='address'>Address</label>
                        <input type='text' name='address' placeholder={userInfo.address} className='form-control' onChange={handleChange} value={formData.address} />
                    </div>
                    <div className='mb-2'>
                        <label htmlFor='phone'>Phone</label>
                        <input type='text' name='phone' placeholder={userInfo.phone} className='form-control' onChange={handleChange} value={formData.phone} />
                    </div>
                    <div className='mb-2'>
                        <label htmlFor='avatar'>Avatar</label>
                        <input type='file' name='avatar' className='form-control' onChange={handleAvatarChange} />
                    </div>

                    <div className='d-grid'>
                        <button className='btn btn-primary'>Save</button>
                    </div>
                    <p className='text-end mt-2'>
                        <Link to='/home' className='ms-2'>Back</Link>
                    </p>
                </form>
            </div>
        </div>
    );
}

export default UserInfoPage;
